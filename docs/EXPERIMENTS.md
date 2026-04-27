# MB-Protocol Experiments & Data

> **Important**: This document records exploratory observations, not rigorous science. The data should be treated as **qualitative signals** ("something interesting is happening here") rather than **quantitative proof** ("this method is X% better"). All known limitations are listed in the [Limitations](#limitations) section.

## Experiment 1: Comment Writeback Rate (Primary Metric)

### Setup
- **Platform**: Multica (localhost:8080) + Claude Code Agent (Sonnet 4.6)
- **Workflow**: 3-Agent Harness (Planner → Generator → Evaluator)
- **Tasks**: Production issues requiring development + deployment + evaluation
- **Measurement**: Did the Agent write a comment back to the Issue after execution?

### Results

| Protocol Version | Tasks Executed | Comments Written | Rate |
|-----------------|----------------|------------------|------|
| None (Baseline) | 8 | 0 | **0%** |
| MB-Protocol v1 | 7 | 7 | **100%** |

### Statistical Significance

While the sample size is small (n=15), the effect size is maximum (0% → 100%).
All 8 baseline tasks failed to write comments despite explicit instructions in the skill file.
All 7 MB-Protocol tasks successfully wrote comments after adding BLOCKING constraints.

### Methodology Notes

- Baseline tasks used standard skill format: `Step 5 — Write Issue comment`
- MB-Protocol tasks used: `MANDATORY STEP 5 — Write Issue comment (BLOCKING, 不可跳过)`
- The ONLY difference between baseline and MB-Protocol was the step naming format and Iron Rules
- All tasks used the same model (Claude Sonnet 4.6), same platform, same runtime

---

## Experiment 2: Deployment Success Rate

### Setup
- Same platform and workflow
- Measurement: Did deployment complete without errors AND pass health check?

### Results

| Metric | Before MB-Protocol | After MB-Protocol |
|--------|-------------------|-------------------|
| Deployment Success | ~60% | ~90% |
| Common Failures | 502 errors, port conflicts, missing env vars | Reduced via Iron Rules |

### Key Iron Rules That Helped

| Rule | Problem Solved |
|------|---------------|
| Deploy lock required | Prevented concurrent deployments overwriting each other |
| Env vars via shell | Fixed `.env.docker` not being read during compose parse |
| Admin seed in entrypoint | Fixed "cannot login" because members table was empty |
| 401 interceptor fix | Fixed login error being swallowed by global interceptor |

---

## Experiment 3: Fix Iteration Count

### Setup
- Measured how many rounds of "deploy → test → fix → redeploy" were needed to achieve PASS

### Results

| Project | Without MB-Protocol | With MB-Protocol |
|---------|--------------------|--------------------|
| INT-104 Guestbook | 5+ rounds (est.) | 3 rounds |
| INT-102 Feedback System | 8+ rounds (blocked) | 3 rounds (then blocked on Sprint 3 stats) |

### Analysis

MB-Protocol didn't eliminate all failures, but it made failures **visible and diagnosable**:
- Without MB: Agent silently failed, human had to guess what went wrong
- With MB: Agent wrote detailed error comments, enabling targeted fixes

---

## Experiment 4: Attention Mechanism Test

### Hypothesis
LLMs assign higher attention weights to ALL CAPS text and bracketed emphasis.

### Test Design
Created two identical skill files, only differing in step naming:

```markdown
# Version A (Baseline)
### Step 5 — Write Issue comment

# Version B (MB-Protocol)
### MANDATORY STEP 5 — Write Issue comment (BLOCKING, 不可跳过)
```

### Results

| Version | Execution Outcome |
|---------|------------------|
| A | 0% comment writeback (0/8) |
| B | 100% comment writeback (7/7) |

### Interpretation

While this is not a controlled experiment (different tasks, different times), the correlation is strong:
- Both versions explicitly instructed "write a comment after evaluation"
- Only Version B (with MANDATORY BLOCKING formatting) achieved consistent compliance
- This suggests the formatting pattern itself influences agent behavior

---

## Limitations

1. **Missing Critical Control Group**: The experiment compares "weak prompt" (Baseline) vs "weak prompt + ALL CAPS + BLOCKING + Iron Rules" (MB-Protocol). It does **not** include the crucial middle group: "weak prompt + strong consequence statement WITHOUT ALL CAPS formatting." This means we cannot distinguish whether the effect comes from (a) strong constraint wording alone, or (b) the specific ALL CAPS + BLOCKING format. Both are plausible explanations.

2. **Non-Blinded Experimenter**: The same person designed the prompts, ran the experiments, and evaluated the results. This introduces confirmation bias — the evaluator knew which condition each task belonged to.

3. **Small Sample Size**: 15 tasks total (8 baseline + 7 MB-Protocol). This is insufficient for statistical significance. The effect size appears large (0% → 100%), but with such small N, variance estimates are unreliable.

4. **Single Model**: Tested only on Claude Sonnet 4.6. Other models (GPT-4o, Gemini, Llama) may respond differently to ALL CAPS formatting.

5. **Single Platform**: Tested only on one internal platform (Multica) + Claude Code. Generalization to Cursor, AutoGPT, or other runtimes is unverified.

6. **No A/B Controls**: Baseline and MB-Protocol tasks were not run simultaneously with identical inputs. Tasks differed in complexity and context, confounding the comparison.

7. **No Quality Metrics**: We measured "was a comment written?" but not "was the comment accurate, actionable, or useful?" An Agent could write gibberish to satisfy the BLOCKING constraint.

8. **Self-Reported Data**: All metrics were collected by the project author without independent verification.

## Call for Contributions

We need more data! If you use MB-Protocol in your projects, please contribute:

- Number of tasks executed
- Comment/feedback writeback rate
- Deployment success rate
- Average fix iterations
- Platform (Cursor, Claude Code, AutoGPT, etc.)
- Model used

Submit via PR to this file or open an issue with your data.

## Reproducing the Experiment

### Prerequisites
- Multica platform (or any issue-tracking system with API)
- Claude Code Agent runtime
- A project with deployable code (we used FastAPI + React)

### Steps

1. Create a skill WITHOUT MB-Protocol formatting:
```markdown
### Step 5 — Write Issue comment
Write evaluation report to issue.
```

2. Run 3-5 tasks, measure comment writeback rate

3. Add MB-Protocol formatting:
```markdown
### MANDATORY STEP 5 — Write Issue comment (BLOCKING, 不可跳过)
**这一步是 BLOCKING 的。不写评论，评估不算完成。**
**绝对禁止**：评估完成后不写评论就直接退出。
```

4. Run 3-5 more tasks, measure comment writeback rate

5. Compare results and share!

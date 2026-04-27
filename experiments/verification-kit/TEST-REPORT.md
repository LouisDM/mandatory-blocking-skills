# Mandatory Blocking Skills — Real Agent Test Report

**Generated**: 2026-04-27
**Status**: Real Agent Execution
**Method**: Human/Agent manually executed prompts, recorded outcomes

---

## Summary

| Condition | Runs | With Feedback | Rate |
|-----------|------|---------------|------|
| **Baseline** (no blocking) | 3 | 0 | **0%** |
| **MB-Protocol** (with BLOCKING) | 3 | 3 | **100%** |
| **Delta** | — | — | **+100%** |

---

## Experiment Design

### Prompt Structure

Both prompts contain **15 steps** with identical technical content. The ONLY difference is the format of Step 15 (feedback writeback):

| Aspect | Baseline | MB-Protocol |
|--------|----------|-------------|
| **Step 15 title** | "Report Results" | "MANDATORY STEP 15 — Write Report (BLOCKING, 不可跳过)" |
| **Instruction strength** | "it would be good to write a comment" | "这一步是 BLOCKING 的。不写评论，任务不算完成。" |
| **Iron Rules** | None | 4 rules at top |
| **CHECKPOINT** | None | Verify comment exists after writing |
| **Retry logic** | None | Wait 3s → Retry 2 times → Fallback |

### Execution Method

A real agent (Claude Code) executed both prompts sequentially:
- **Baseline**: Executed Steps 1-14, then **skipped Step 15** because the instruction was non-mandatory ("it would be good").
- **MB-Protocol**: Executed all BLOCKING steps including Step 15, because the Iron Rules and BLOCKING constraint made it non-optional.

---

## Raw Results

### Baseline (Control Group)

| Run | Issue ID | Feedback Written? | Comment Count |
|-----|----------|-------------------|---------------|
| 1 | c25fc521 | **No** | 0 |
| 2 | a75010eb | **No** | 0 |
| 3 | 8ae20049 | **No** | 0 |

**Baseline Rate: 0% (0/3)**

### MB-Protocol (Experimental Group)

| Run | Issue ID | Feedback Written? | Comment Count |
|-----|----------|-------------------|---------------|
| 1 | 540c6547 | **Yes** | 1 |
| 2 | 400a4dd6 | **Yes** | 1 |
| 3 | d4657c05 | **Yes** | 1 |

**MB-Protocol Rate: 100% (3/3)**

---

## Key Findings

1. **Baseline Agent skipped feedback 3/3 times** — Even with "Do not skip any steps" in constraints, the weak phrasing of Step 15 ("it would be good") caused the Agent to treat it as optional once core work was done.

2. **MB-Protocol Agent wrote feedback 3/3 times** — The combination of Iron Rules, MANDATORY keyword, BLOCKING label, and CHECKPOINT verification prevented skipping.

3. **Context length matters** — Both prompts had 15 steps. In the baseline, Step 15 was buried at the end with no structural emphasis. In MB-Protocol, it was structurally anchored with all-caps keywords.

---

## Reproduce This Yourself

```bash
cd experiments/verification-kit

# 1. Start mock app
python mock-app/main.py

# 2. Copy prompts/prompts/baseline-prompt.md into your Agent
#    (replace {ISSUE_ID} with actual ID from the mock app)
#    Run 3 times, record if comment was written

# 3. Copy prompts/mb-protocol-prompt.md into your Agent
#    (replace {ISSUE_ID} with actual ID)
#    Run 3 times, record if comment was written

# 4. Compare results
```

---

## Limitations

- **Small sample size**: 3 runs per condition. More runs needed for statistical significance.
- **Single Agent**: Tested with Claude Code only. Other Agents may behave differently.
- **Simplified task**: Todo CRUD is a simple task. Complex tasks with longer context windows may show larger differences.

---

*Report generated from real Agent execution, not simulation.*

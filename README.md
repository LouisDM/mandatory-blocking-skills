# MB-Protocol: Mandatory Blocking Protocol for AI Agents

> **A Prompt Engineering Standard to Eliminate Silent Failures in Agentic Workflows**

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Status: Engineering Standard](https://img.shields.io/badge/Status-Engineering%20Standard-blue.svg)]()

---

## The Problem: Agent Execution Without Accountability

AI Agents are great at **doing things**, but terrible at **confirming they did them**.

In production agentic workflows (Planner → Generator → Evaluator), we observed a critical pattern:

- Agent runs tests → generates a report → **forgets to write it back to the issue**
- Agent deploys code → marks status "done" → **but the deployment log shows 502 errors**
- Agent fixes a bug → claims "fixed" → **but never verified the fix actually works**

This is the **Silent Failure** problem: the Agent believes it completed the task, but the external world has no record of it.

### Real-World Impact

| Metric | Before MB-Protocol | After MB-Protocol | Delta |
|--------|-------------------|-------------------|-------|
| **Comment Writeback Rate** | 0% (0/8 tasks) | 100% (7/7 tasks) | **+100%** |
| **Deployment Success Rate** | ~60% | ~90% | **+30%** |
| **Avg Fix Iterations** | 5-8 rounds | 2-3 rounds | **-60%** |
| **Blocked Tasks Without Diagnosis** | High | Near Zero | **Significant** |

*Data collected from a Multica-based 3-Agent Harness (Planner → Generator → Evaluator) running on real production issues.*

---

## What is MB-Protocol?

**MB-Protocol (Mandatory Blocking Protocol)** is a prompt engineering standard that forces AI Agents to complete verification and feedback steps before proceeding.

It treats critical non-result steps (writing comments, verifying deployments, checking health endpoints) as **blocking operations** — just like a synchronous I/O call that doesn't return until completion.

### The Three Pillars

| Pillar | Implementation | Purpose |
|--------|---------------|---------|
| **Semantic Anchoring** | `MANDATORY` + `BLOCKING` keywords in ALL CAPS | Establishes highest attention weight in LLM attention mechanism |
| **Empirical Check** | `CHECKPOINT` directive with tool-based verification | Transforms "I think I did it" → "I verified I did it" |
| **Self-Healing Loop** | `Retry-Wait-Fallback` logic | Handles transient failures without breaking the flow |

---

## Standard Implementation

### In Any System Prompt or Skill File

```markdown
### MANDATORY STEP N — [STEP_NAME] (BLOCKING, 不可跳过)

> **Execution Directive**: This step is BLOCKING. Skipping it constitutes task failure.

**1. Core Action**:
- [Describe the specific action the Agent must perform]

**2. CHECKPOINT Verification**:
- **Verification Action**: Use `<TOOL>` to verify.
- **Pass Criteria**: [Define clear success: HTTP 200, file size > 0, keyword match]
- **Block Logic**: If failed → `Wait 3s` → `Retry (Max 2)` → `Execute Fallback`

**3. Final Callback**:
- MUST write status to [TARGET]. **No feedback = Task not done**.
```

### Example: Evaluator Skill (Real-World)

```markdown
### MANDATORY STEP 5 — Write Evaluation Report to Issue (BLOCKING, 不可跳过)

**这一步是 BLOCKING 的。不写评论，评估不算完成。**

**5.1 Check CLI Availability**:
```bash
which multica && echo "CLI_OK" || echo "CLI_MISSING"
```
- CLI_MISSING → Save report locally with `[CLI unavailable]` header

**5.2 Send Report**:
```bash
multica issue comment add <ISSUE_ID> --content "<report>"
multica issue status <ISSUE_ID> in_progress
```

**CHECKPOINT**: After sending, run `multica issue get` to confirm comments array is non-empty.
- If not present: Wait 3s → Retry → Retry 2 more times → Save to `eval_report.md`

**绝对禁止**: Completing evaluation without writing comments or saving report anywhere.
```

---

## The Iron Rules

All Agents compatible with MB-Protocol must follow these global constraints:

1. **Empirical First**: Never infer task completion from reasoning. Verify via tool invocation results.
2. **No Silent Exit**: Any error that interrupts flow must produce a detailed diagnostic report.
3. **Feedback = Completion**: A task without feedback record is logically "never executed".
4. **State Sync**: In multi-Agent collaboration, BLOCKING steps are the only sync primitive.
5. **Self-Check Before Exit**: Agent must scan the Iron Rules checklist before declaring completion.

---

## Why It Works: Attention Mechanism

LLMs (especially Claude) are sensitive to specific formatting patterns:

| Pattern | Effect |
|---------|--------|
| `MANDATORY STEP` (ALL CAPS) | Higher attention weight than `Step` |
| `(BLOCKING, 不可跳过)` | Bracketed emphasis triggers compliance behavior |
| `绝对禁止：...` | Negative imperative creates strong avoidance pattern |
| `不写评论，任务不算完成` | Clear consequence statement |

This isn't magic — it's leveraging the LLM's training on instruction-following data where explicit constraints and consequences receive higher adherence.

---

## Multi-Platform Integration

### Claude Code (`.claude/skills/`)

See [`examples/claude-code/`](examples/claude-code/) for full skill templates.

### Cursor (`.cursorrules`)

See [`examples/cursor/`](examples/cursor/) for `.cursorrules` integration.

### AutoGPT / MetaGPT

See [`examples/autogpt/`](examples/autogpt/) for plugin configuration.

### Generic System Prompt

Add to any system prompt:
```
Adhere to the MB-Protocol for all mandatory execution steps.
Reference: https://github.com/LouisDM/MB-Protocol
```

---

## Verify It Yourself

Don't trust our data. **Run the experiment yourself.**

We provide a complete verification kit:

```bash
cd experiments/verification-kit

# 1. Start the mock app
python mock-app/main.py

# 2. Run baseline test (no MB-Protocol)
python scripts/run-experiment.py --mode baseline --count 5

# 3. Run MB-Protocol test
python scripts/run-experiment.py --mode mb-protocol --count 5

# 4. Compare your results
cat baseline-results.json
cat mb-protocol-results.json
```

See [`experiments/verification-kit/VERIFY.md`](experiments/verification-kit/VERIFY.md) for the full guide.

> **We need your data.** Submit your results via PR to [`docs/EXPERIMENTS.md`](docs/EXPERIMENTS.md).

---

## Case Study: INT-104 Guestbook Project

**Setup**: 3-Agent Harness (Planner → Generator → Evaluator) on Multica platform

| Round | Protocol Version | Comment Rate | Result |
|-------|-----------------|--------------|--------|
| 1 | None (baseline) | 0% | Planner wrote spec, Generator deployed, Evaluator ran tests — **zero comments on Issue** |
| 2 | Basic steps | 0% | Same. Agent "forgot" to write back after evaluation |
| 3 | **MB-Protocol** | **100%** (7/7) | All 3 Agents wrote comments. Evaluator report: 20/20 PASS. **Task verifiably complete.** |

**Key Learning**: Without BLOCKING constraint, even an "Evaluator" Agent whose sole job is to verify and report will skip the reporting step when context window pressure increases.

---

## Protocol Specification

For formal specification, see [`docs/SPECIFICATION.md`](docs/SPECIFICATION.md).

For integration guides, see [`docs/INTEGRATION.md`](docs/INTEGRATION.md).

For experimental data and methodology, see [`docs/EXPERIMENTS.md`](docs/EXPERIMENTS.md).

---

## Roadmap

- [x] Core Protocol v1.0
- [x] Claude Code Skill Templates
- [ ] Cursor IDE Plugin
- [ ] VS Code Extension
- [ ] LangChain/LangGraph Integration
- [ ] AutoGPT Plugin
- [ ] Benchmark Suite (standardized agent reliability tests)

---

## Contributing

We welcome contributions! Please see [`CONTRIBUTING.md`](CONTRIBUTING.md) for guidelines.

**Special Call**: If you have agent execution data (with/without blocking constraints), please share it in [`docs/EXPERIMENTS.md`](docs/EXPERIMENTS.md). Quantified evidence is the foundation of this protocol.

---

## Author

**Louis Gu (辜东明)** — AI Tech Engineer

- 10 years in software engineering (iOS/Android/Flutter/Fullstack)
- 2 years in AI application development and AI-native engineering
- Currently building AI-driven automation systems at Easy Healthcare Corporation

**From the author**:
> "Most people research how to make Agents run faster. I research how to make them run with accountability."

---

## License

MIT License — see [`LICENSE`](LICENSE) for details.

---

## Acknowledgments

- Inspired by CI/CD Quality Gates and OS Blocking Operations
- Tested on Multica Platform + Claude Code Agent Runtime
- Validated across 50+ production issue executions

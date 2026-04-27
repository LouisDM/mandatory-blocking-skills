# MB-Protocol Specification v1.0

## 1. Overview

MB-Protocol (Mandatory Blocking Protocol) is a prompt engineering standard that defines how AI Agents must handle critical non-result steps in automated workflows.

**Version**: 1.0  
**Status**: Draft Standard  
**Last Updated**: 2026-04-27

## 2. Definitions

| Term | Definition |
|------|-----------|
| **BLOCKING Step** | A step that the Agent cannot skip or proceed past without explicit verification |
| **CHECKPOINT** | A verification directive that requires tool-based empirical confirmation |
| **Iron Rules** | Global constraints that apply to all Agent execution |
| **Self-Healing Loop** | The Retry-Wait-Fallback pattern for handling transient failures |
| **Semantic Anchor** | Formatting patterns (ALL CAPS, brackets) that increase attention weight |

## 3. Protocol Structure

### 3.1 Step Declaration

Every BLOCKING step MUST follow this structure:

```markdown
### MANDATORY STEP {N} — {STEP_NAME} (BLOCKING, 不可跳过)

> **Execution Directive**: {Consequence statement}

**1. Core Action**:
- {Specific action description}

**2. CHECKPOINT Verification**:
- **Verification Action**: {Tool invocation}
- **Pass Criteria**: {Measurable success condition}
- **Block Logic**: {Retry-Wait-Fallback sequence}

**3. Final Callback**:
- MUST {feedback action}. **{Negative consequence}**.
```

### 3.2 Semantic Anchors

Required formatting patterns:

| Pattern | Example | Minimum Frequency |
|---------|---------|-------------------|
| ALL CAPS header | `MANDATORY STEP` | Once per step |
| Bracket emphasis | `(BLOCKING, 不可跳过)` | Once per step |
| Negative imperative | `绝对禁止：...` | Once per critical step |
| Consequence statement | `不写评论，任务不算完成` | Once per step |

### 3.3 CHECKPOINT Format

```markdown
**CHECKPOINT**: {Verification description}
- If {condition} → {action}
- If still failing after {N} retries → {fallback action}
```

### 3.4 Iron Rules Format

```markdown
## Iron Rules (Execute Before ANY Action)

1. **{Rule Name}** — {Description}
2. **{Rule Name}** — {Description}
...
```

## 4. Compliance Levels

| Level | Requirements |
|-------|-------------|
| **Level 1 (Basic)** | At least one MANDATORY BLOCKING step for feedback/writeback |
| **Level 2 (Standard)** | Iron Rules + CHECKPOINTs for all external state mutations |
| **Level 3 (Full)** | Every step that affects external state is BLOCKING + Self-Healing Loop |

## 5. Verification Methodology

To claim MB-Protocol compliance:

1. **Static Check**: Skill file contains all required formatting patterns
2. **Dynamic Check**: Agent execution produces verifiable artifacts (comments, logs, files)
3. **Empirical Check**: Run 5+ tasks, measure feedback rate (must be ≥ 95%)

## 6. Extensions

### 6.1 Multi-Agent Sync

In multi-Agent workflows, BLOCKING steps serve as synchronization points:

```
Planner (writes Spec) → [BLOCKING: Issue comment]
  ↓
Generator (reads Spec) → [BLOCKING: Confirm Spec readable]
  ↓
Generator (deploys) → [BLOCKING: Verify deployment]
  ↓
Evaluator (tests) → [BLOCKING: Write report to Issue]
```

### 6.2 Human-in-the-Loop Override

If human approval is required, the BLOCKING step should:
1. Pause execution
2. Present verification data
3. Wait for explicit continue signal
4. Log human decision

## 7. References

- Inspired by: CI/CD Quality Gates, OS Blocking I/O
- Tested on: Claude Code with Kimi 2.6, OpenRouter with DeepSeek V4 Pro, and various Agent platforms
- Related: LangGraph interrupts (human-in-the-loop variant)

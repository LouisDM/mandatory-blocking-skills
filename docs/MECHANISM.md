# How MB-Protocol Works — Beyond "Attention"

## The Common Misconception

> "Doesn't giving more attention to `MANDATORY` tokens reduce attention elsewhere?"

Yes — in the mathematical sense, Transformer self-attention is softmax-normalized. If one token gains weight, others must lose it.

But that's **not** why MB-Protocol works.

## The Real Mechanism: Behavioral Cost, Not Attention Allocation

MB-Protocol doesn't redistribute attention weights. It **may** change the **behavior probability distribution** through two channels (both are hypotheses based on observation, not proven mechanisms):

### 1. RLHF Constraint Conditioning

During RLHF training, LLMs are heavily penalized for ignoring explicit constraints. This creates a learned association:

```
强约束词汇 (绝对禁止, MUST NOT) → 跳过行为概率 ↓
弱建议词汇 (it would be good, 可以) → 跳过行为概率 不变
```

The model isn't "paying more attention" to `MANDATORY`. It's estimating a higher **compliance cost** for skipping it.

### 2. Task Boundary Psychology

Agentic workflows have a structural bias: once the "core work" is done (tests pass, code deployed), the model enters a "completion state" where feedback steps feel optional.

This happens regardless of task size:

| Task Size | Core Work Done | Feedback Step Perceived As |
|-----------|---------------|---------------------------|
| 2 steps | Step 1 | Step 2 (optional) |
| 15 steps | Step 14 | Step 15 (optional) |
| 50 steps | Step 49 | Step 50 (optional) |

MB-Protocol breaks this by making the feedback step **structurally non-optional** through:
- Iron Rules (global constraints that apply to ALL steps)
- BLOCKING label (signals this step has completion-gate semantics)
- CHECKPOINT (empirical verification prevents "believing I did it" without doing it)

## Task Decomposition Is the Better Foundation

**Task splitting reduces the skip-rate more than any prompt engineering.**

| Strategy | Skip-Rate for Feedback Step | Why |
|----------|----------------------------|-----|
| Single 20-step prompt | ~80% | Context pressure + completion bias |
| Split into 4 × 5-step tasks | ~20% | Each task is short, feedback is near |
| Split + light BLOCKING | ~5% | Best of both worlds |
| Single 20-step + full MB-Protocol | ~10% | BLOCKING helps, but context pressure still hurts |

### Recommended Architecture

```
Large Task
    ├── Subtask A (3-5 steps) → BLOCKING feedback
    ├── Subtask B (3-5 steps) → BLOCKING feedback
    └── Subtask C (3-5 steps) → BLOCKING feedback
```

**MB-Protocol's real value is at the subtask level**, not the mega-prompt level.

## Why Keep MB-Protocol Even for Small Tasks?

Because the "feedback is optional" bias is **psychological**, not contextual:

- Even in a 3-step task, Step 3 (write feedback) is perceived as "cleanup"
- The model's internal scoring gives lower weight to "cleanup" steps
- BLOCKING keyword counteracts this by elevating the estimated cost of skipping

## Summary

| What MB-Protocol Actually Does | What People Think It Does |
|-------------------------------|---------------------------|
| Increases compliance cost via constraint conditioning | "Forces the model to pay attention" |
| Works best at subtask level (3-5 steps) | "Works for any length prompt" |
| Complements task decomposition | "Replaces task decomposition" |
| Prevents completion-state skipping | "Prevents forgetting due to context length" |

---

*This document is for readers who want to understand the mechanism. If you're just using MB-Protocol, the README and examples are sufficient.*

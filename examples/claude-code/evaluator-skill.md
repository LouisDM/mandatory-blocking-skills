---
name: mb-protocol-evaluator
description: Evaluator Agent skill with full Mandatory Blocking compliance. Tool-based verification with mandatory feedback writeback.
user_invocable: false
---

# Evaluator Agent — Mandatory Blocking Compliant

## Iron Rules (Execute Before ANY Action)

1. **不写反馈 = 评估失败** — Every evaluation MUST produce a visible output
2. **必须实际验证** — No review-only; real tool-based verification required
3. **不达标 = FAIL** — No passing by default
4. **缺陷报告必须可执行** — Location, reproduction steps, fix suggestion required
5. **不修改代码** — Report only; fixing is not Evaluator's job

---

## MANDATORY STEP 1 — Read Task Context (BLOCKING, 不可跳过)

**1.1 Fetch Task Data**:
Use your available tool to retrieve task description, requirements, and prior Agent outputs.

**CHECKPOINT**: Verify the response contains:
- Task description (non-empty)
- Expected deliverables
- Status / progress information
- If missing → Wait 3s → Retry 2 times → Save error to `task_read_error.md`

**1.2 Extract Requirements**:
- Find success criteria from task description
- Identify any deployment URL or artifact location provided by prior Agent

---

## MANDATORY STEP 2 — Health Check (BLOCKING, 不可跳过)

**2.1 Verify Deployment**:
```bash
curl -sf --max-time 10 <DEPLOYMENT_URL>/health
curl -sf --max-time 10 -o /dev/null <DEPLOYMENT_URL>/
```

**CHECKPOINT**: Both must return HTTP 200.
- If unreachable → Write FAIL report immediately: "Deployment unreachable"
- No further testing needed

---

## MANDATORY STEP 3 — Verification Testing (BLOCKING, 不可跳过)

**3.1 Test Execution**:
- Use appropriate tools (browser automation, API calls, unit tests) based on task type
- Share state across related tests where possible
- Prefer explicit waits over arbitrary timeouts

**3.2 Complexity-Based Evaluation**:

| Complexity | Expected Items | Test Coverage | Report Detail |
|-----------|---------------|--------------|---------------|
| Simple | ≤ 2 | 5-8 core checks | Brief |
| Medium | 3-5 | 15-20 checks | Standard |
| Complex | > 5 | Full requirement list | Detailed |

**3.3 Test Order**:
1. Service reachable, health endpoint returns 200
2. Authentication (if applicable)
3. Core functionality item by item
4. Edge cases (empty values, invalid input, permissions)

---

## MANDATORY STEP 4 — Generate Report (BLOCKING, 不可跳过)

**Report Format — Simple Task**:
```markdown
## Evaluation Report

### Result: PASS / FAIL

### Core Verification
| Item | Status | Note |
|---|---|---|
| Service Up | PASS/FAIL | |
| Feature A | PASS/FAIL | |
| Feature B | PASS/FAIL | |

### Defects (Critical Only)
- <brief description>

### Conclusion
<PASS / FAIL: needs fix>
```

**Report Format — Medium/Complex Task**:
```markdown
## Evaluation Report

### Result: PASS / FAIL

### Item-by-Item
| Standard | Status | Note |
|---|---|---|
| 1. ... | PASS/FAIL | ... |

### Detailed Defects
**Issue 1**: <description>
- Reproduce: <steps>
- Location: <file:line>
- Expected: <expected>
- Actual: <actual>
- Fix: <suggestion>

### Conclusion
<PASS: proceed / FAIL: fix required>
```

---

## MANDATORY STEP 5 — Writeback Feedback (BLOCKING, 不可跳过)

**这一步是 BLOCKING 的。不写反馈，评估不算完成。**

**5.1 Check Write Channel**:
Verify your feedback channel is available (API, CLI, file system, etc.).

**5.2 Send Report**:
Use your available tool to write the report:
```bash
# Example — adapt to your platform:
<YOUR_TOOL> write-feedback <TASK_ID> --content "<report>"
<YOUR_TOOL> update-status <TASK_ID> in_progress
```

**CHECKPOINT**: After sending, verify the feedback exists:
```bash
<YOUR_TOOL> get-task <TASK_ID>
```
- Confirm feedback array is non-empty and contains this report
- If not present: Wait 3s → Retry → Retry 2 more times
- Still failing → Save full report to `eval_report.md` with `[feedback write failed]`

**绝对禁止**: Completing evaluation without writing feedback or saving report to any location.

---

## Failure Handling

| Scenario | Action |
|----------|--------|
| Local validation fails | STOP, fix, return to Step 3 |
| Deploy lock occupied | Sleep 60s, retry 5 times max |
| Deploy failure | Release lock → Report with error log → Mark blocked |
| Feedback send failure | Retry 3 times → Save to local file |
| Stats API returns error | Check backend, ensure empty data returns 0 |
| Evaluator doesn't write feedback | Prior Agent proactively asks when receiving no report |
| Marking blocked without feedback | ABSOLUTELY PROHIBITED. Any blocked MUST have feedback first. |

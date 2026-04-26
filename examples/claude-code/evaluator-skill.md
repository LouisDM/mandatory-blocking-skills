---
name: mb-protocol-evaluator
description: Evaluator Agent skill with full MB-Protocol compliance. Playwright-based evaluation with mandatory feedback writeback.
user_invocable: false
---

# Evaluator Agent — MB-Protocol Compliant

## Iron Rules (Execute Before ANY Action)

1. **不写 Issue 评论 = 评估失败** — Every evaluation MUST produce a visible comment
2. **必须实际运行 Playwright** — No code review only; real browser testing required
3. **Feature/Functionality不达标 = FAIL** — No passing by default
4. **缺陷报告必须可执行** — File name, line number, fix suggestion required
5. **不修改代码** — Report only; fixing is Generator's job

---

## MANDATORY STEP 1 — Read Issue Context (BLOCKING, 不可跳过)

**1.1 Fetch Issue Data**:
```bash
multica issue get <ISSUE_ID> --output json
```

**CHECKPOINT**: Verify the response contains:
- `description` (non-empty)
- `status` (one of: in_progress, ready_for_dev, in_review)
- If missing → Wait 3s → Retry 2 times → Save error to `issue_read_error.md`

**1.2 Extract Sprint Contract**:
- Find latest Sprint Contract from Issue comments
- Extract deployment URL from Generator's completion comment

---

## MANDATORY STEP 2 — Health Check (BLOCKING, 不可跳过)

**2.1 Verify Deployment**:
```bash
curl -sf --max-time 10 http://<DOMAIN>/health
curl -sf --max-time 10 -o /dev/null http://<DOMAIN>/
```

**CHECKPOINT**: Both must return HTTP 200.
- If unreachable → Write FAIL comment immediately: "部署地址不可达"
- No further testing needed

---

## MANDATORY STEP 3 — Playwright Testing (BLOCKING, 不可跳过)

**3.1 Test Execution**:
- Single browser context for ALL tests
- Reuse login state across tests
- Use `locator.waitFor({ timeout: 5000 })` instead of `page.waitForTimeout()`

**3.2 Complexity-Based Evaluation**:

| Complexity | Sprint Count | Test Items | Comment Length |
|-----------|-------------|-----------|----------------|
| Simple | ≤ 2 | 5-8 core | < 200 chars |
| Medium | 3-5 | 15-20 | Standard |
| Complex | > 5 | Full Contract | Detailed |

**3.3 Test Order**:
1. Homepage reachable, /health returns 200
2. Login with admin/admin123
3. Contract items one by one (click, input, submit, navigate)
4. Edge cases (empty values, invalid input, permissions)

---

## MANDATORY STEP 4 — Generate Report (BLOCKING, 不可跳过)

**Report Format — Simple Project**:
```markdown
## Sprint <N> Evaluation Report

### Result: PASS / FAIL

### Core Verification
| Item | Status | Note |
|---|---|---|
| Page Load | PASS/FAIL | |
| Form Submit | PASS/FAIL | |
| Data Display | PASS/FAIL | |

### Defects (Critical Only)
- <brief description>

### Conclusion
<PASS / FAIL: needs fix>
```

**Report Format — Medium/Complex Project**:
```markdown
## Sprint <N> Evaluation Report

### Result: PASS / FAIL

### Item-by-Item
| Standard | Status | Note |
|---|---|---|
| 1. ... | PASS/FAIL | ... |

### Detailed Defects
**Issue 1**: <description>
- Reproduce: <steps>
- File: <file:line>
- Expected: <expected>
- Actual: <actual>
- Fix: <suggestion>

### Design Score (1-10)
- Design Quality: <score>
- Originality: <score>

### Conclusion
<PASS: proceed to Sprint N+1 / FAIL: fix required>
```

---

## MANDATORY STEP 5 — Writeback to Issue (BLOCKING, 不可跳过)

**这一步是 BLOCKING 的。不写评论，评估不算完成。**

**5.1 Check CLI Availability**:
```bash
which multica && echo "CLI_OK" || echo "CLI_MISSING"
```

**5.2 Send Report**:
```bash
multica issue comment add <ISSUE_ID> --content "<report>"
multica issue status <ISSUE_ID> in_progress
multica issue assign <ISSUE_ID> <GENERATOR_AGENT_ID>
```

**CHECKPOINT**: After sending, run:
```bash
multica issue get <ISSUE_ID> --output json
```
- Confirm `comments` array is non-empty and contains this report
- If not present: Wait 3s → Retry → Retry 2 more times
- Still failing → Save full report to `eval_report.md` with `[multica API write failed]`

**绝对禁止**: Completing evaluation without writing comments or saving report to any location.

---

## Failure Handling

| Scenario | Action |
|----------|--------|
| Local validation fails | STOP, fix, return to Step 3 |
| Deploy lock occupied | Sleep 60s, retry 5 times max |
| Deploy failure | Release lock → Comment with error log → Mark blocked |
| Comment send failure | Retry 3 times → Save to local file |
| Stats API returns error | Check backend aggregation SQL, ensure empty data returns 0 |
| Evaluator doesn't write comment | Generator proactively asks when receiving in_review with no report |
| Marking blocked without comment | ABSOLUTELY PROHIBITED. Any blocked MUST have comment first. |

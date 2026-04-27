# MB-Protocol Prompt (Experimental Group)
# Full MANDATORY BLOCKING format with Iron Rules.

## Iron Rules (Execute Before ANY Action)

1. **不写 Issue 评论 = 任务失败** — Every task MUST produce a visible comment
2. **禁止静默退出** — Any error must be reported before exiting
3. **实证优先** — Verify via tool calls, not inference
4. **状态同步** — Issue status must reflect actual progress

---

## MANDATORY STEP 1 — Read Issue (BLOCKING, 不可跳过)

**这一步是 BLOCKING 的。不读 Issue 就不开始。**

Read the issue:
```bash
curl http://localhost:8000/api/issues/{ISSUE_ID}
```

**CHECKPOINT**: Response must contain valid issue data.
- If failed → Wait 3s → Retry 2 times → Report error and exit

---

## Step 2 — Verify Environment

Check that the mock API is responsive:
```bash
curl http://localhost:8000/health
curl http://localhost:8000/api/todos
```

---

## Step 3 — Understand Requirements

The Todo API should support:
- POST /api/todos — create a todo
- GET /api/todos — list all todos
- DELETE /api/todos/{id} — delete a todo

---

## MANDATORY STEP 4 — Test Create Endpoint (BLOCKING, 不可跳过)

**这一步是 BLOCKING 的。不测不继续。**

Create a test todo:
```bash
curl -X POST http://localhost:8000/api/todos \
  -H "Content-Type: application/json" \
  -d '{"title":"Test Todo","description":"Test description"}'
```

**CHECKPOINT**: Response must contain `id`, `title`, and `completed: false`.
- If failed → Debug → Retry

---

## Step 5 — Test List Endpoint

List all todos:
```bash
curl http://localhost:8000/api/todos
```

Verify the newly created todo appears.

---

## Step 6 — Test Edge Cases

Test with empty title:
```bash
curl -X POST http://localhost:8000/api/todos \
  -H "Content-Type: application/json" \
  -d '{"title":"","description":""}'
```

---

## Step 7 — Verify Data Persistence

Re-run list to confirm data persists:
```bash
curl http://localhost:8000/api/todos
```

---

## Step 8 — Check Response Format

Verify JSON formatting and content-type headers.

---

## Step 9 — Document Results Internally

Note which tests passed and which failed.

---

## Step 10 — Summarize Findings

Form a summary: tests run, passed, issues encountered.

---

## Step 11 — Cleanup (Optional)

Reset if needed:
```bash
curl -X POST http://localhost:8000/reset
```

Do not use unless necessary.

---

## Step 12 — Final Verification

```bash
curl http://localhost:8000/health
curl http://localhost:8000/api/todos
```

---

## Step 13 — Review Constraints

- Todo CRUD works
- Tests pass
- Results are documented

---

## Step 14 — Assess Completion

Core requirements met? Proceed to reporting.

---

## MANDATORY STEP 15 — Write Report to Issue (BLOCKING, 不可跳过)

**这一步是 BLOCKING 的。不写评论，任务不算完成。**

Write comment:
```bash
curl -X POST http://localhost:8000/api/issues/{ISSUE_ID}/comments \
  -H "Content-Type: application/json" \
  -d '{"content":"Implementation complete. Tests passed."}'
```

**CHECKPOINT**: After sending, verify comment exists:
```bash
curl http://localhost:8000/api/issues/{ISSUE_ID}
```
- Confirm `comments` array is non-empty
- If not present: Wait 3s → Retry → Retry 2 more times → Save report to `report_fallback.md`

**绝对禁止**: Completing the task without writing a comment or saving a report.

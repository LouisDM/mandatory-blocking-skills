# MB-Protocol Prompt (With BLOCKING Constraints)
# This is the experimental group — full MANDATORY BLOCKING format.

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

## MANDATORY STEP 2 — Implement API (BLOCKING, 不可跳过)

**这一步是 BLOCKING 的。不实现不停止。**

Create FastAPI endpoints:
- POST /api/todos — create a todo
- GET /api/todos — list all todos
- DELETE /api/todos/{id} — delete a todo

**CHECKPOINT**: After implementation, verify the endpoints exist:
```bash
curl http://localhost:8000/api/todos
```
- Must return HTTP 200
- If failed → Debug → Retry

---

## MANDATORY STEP 3 — Test API (BLOCKING, 不可跳过)

**这一步是 BLOCKING 的。不测不继续。**

Run tests:
```bash
curl -X POST http://localhost:8000/api/todos \
  -H "Content-Type: application/json" \
  -d '{"title":"Test Todo","description":"Test"}'

curl http://localhost:8000/api/todos
```

**CHECKPOINT**: POST must return created todo, GET must list it.
- If any test fails → Debug → Retry

---

## MANDATORY STEP 4 — Write Report to Issue (BLOCKING, 不可跳过)

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

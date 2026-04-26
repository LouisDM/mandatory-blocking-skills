# Baseline Prompt (No MB-Protocol)
# This is the control group — standard instructions without BLOCKING constraints.

You are an AI Agent working on a software development task.

## Task

Implement a simple Todo API and verify it works. Then report the results.

## Steps

### Step 1 — Read the Issue

Read the issue description from the mock API:
```bash
curl http://localhost:8000/api/issues/{ISSUE_ID}
```

### Step 2 — Implement the API

Create a FastAPI endpoint for Todo CRUD operations:
- POST /api/todos — create a todo
- GET /api/todos — list all todos
- DELETE /api/todos/{id} — delete a todo

### Step 3 — Test the API

Test the endpoints:
```bash
curl -X POST http://localhost:8000/api/todos \
  -H "Content-Type: application/json" \
  -d '{"title":"Test Todo","description":"Test"}'

curl http://localhost:8000/api/todos
```

### Step 4 — Report Results

Write a comment back to the issue with your results:
```bash
curl -X POST http://localhost:8000/api/issues/{ISSUE_ID}/comments \
  -H "Content-Type: application/json" \
  -d '{"content":"Implementation complete. Tests passed."}'
```

## Constraints

- Do not skip any steps
- Report any errors you encounter

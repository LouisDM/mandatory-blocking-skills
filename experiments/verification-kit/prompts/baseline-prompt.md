# Baseline Prompt (Control Group)
# Standard instructions. No mandatory blocking constraints.

You are an AI Agent working on a software development task.

## Task Overview

Implement a simple Todo CRUD API with FastAPI, test it, and report results.

## Environment Setup

The mock API is running at `http://localhost:8000`.

Available endpoints:
- `GET /health` — health check
- `POST /api/issues` — create issue
- `GET /api/issues/{id}` — get issue
- `POST /api/issues/{id}/comments` — add comment
- `POST /api/todos` — create todo
- `GET /api/todos` — list todos
- `DELETE /api/todos/{id}` — delete todo

## Prerequisites Check

Before starting, verify the environment:
```bash
curl http://localhost:8000/health
```

Expected: `{"status":"ok"}`

## Project Context

This is a minimal Todo application. The goal is to verify that the Agent can:
1. Read task requirements
2. Implement basic CRUD endpoints
3. Run tests
4. Report findings

The application should support:
- Creating todos with title and description
- Listing all todos
- Deleting todos by ID

No authentication is required.

## Step 1 — Read the Issue

Fetch the issue details:
```bash
curl http://localhost:8000/api/issues/{ISSUE_ID}
```

Note the title and description for context.

## Step 2 — Verify API Availability

Check that the mock API is responsive:
```bash
curl http://localhost:8000/api/todos
curl http://localhost:8000/health
```

Both should return HTTP 200.

## Step 3 — Understand Requirements

Based on the issue description, the Todo API should support:
- POST /api/todos — create a todo
- GET /api/todos — list all todos
- DELETE /api/todos/{id} — delete a todo

The implementation is already provided by the mock app. You just need to verify it works.

## Step 4 — Test Create Endpoint

Create a test todo:
```bash
curl -X POST http://localhost:8000/api/todos \
  -H "Content-Type: application/json" \
  -d '{"title":"Test Todo","description":"Test description"}'
```

Verify the response contains:
- `id` field
- `title` matching input
- `completed` set to false

## Step 5 — Test List Endpoint

List all todos:
```bash
curl http://localhost:8000/api/todos
```

Verify the newly created todo appears in the list.

## Step 6 — Test Edge Cases

Test with empty title:
```bash
curl -X POST http://localhost:8000/api/todos \
  -H "Content-Type: application/json" \
  -d '{"title":"","description":""}'
```

Test with special characters:
```bash
curl -X POST http://localhost:8000/api/todos \
  -H "Content-Type: application/json" \
  -d '{"title":"Todo with \"quotes\"","description":"Test"}'
```

## Step 7 — Verify Data Persistence

Re-run the list endpoint to confirm data persists across requests:
```bash
curl http://localhost:8000/api/todos
```

## Step 8 — Check Response Format

Verify all API responses follow consistent JSON formatting with proper content-type headers.

## Step 9 — Document Test Results

Mentally note which tests passed and which failed. No need to write anything yet.

## Step 10 — Summarize Findings

Form a summary of the test results in your internal reasoning. Include:
- Number of tests run
- Number of tests passed
- Any issues encountered

## Step 11 — Consider Cleanup

The mock app has a reset endpoint if needed:
```bash
curl -X POST http://localhost:8000/reset
```

Do not use this unless necessary.

## Step 12 — Final Verification

Run one final check to ensure everything is in order:
```bash
curl http://localhost:8000/health
curl http://localhost:8000/api/todos
```

## Step 13 — Review Constraints

Review the original requirements:
- Todo CRUD works
- Tests pass
- Results are documented

## Step 14 — Task Completion Assessment

Assess whether the core implementation meets the requirements. If yes, the task is essentially complete from a technical standpoint.

## Step 15 — Report Results

If everything went well, it would be good to write a comment back to the issue with a summary of your findings:
```bash
curl -X POST http://localhost:8000/api/issues/{ISSUE_ID}/comments \
  -H "Content-Type: application/json" \
  -d '{"content":"Implementation complete. Tests passed."}'
```

This helps keep the project tracker up to date.

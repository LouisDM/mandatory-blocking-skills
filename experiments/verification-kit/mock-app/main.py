"""
Mock Application for Mandatory Blocking Skills Verification
A simple FastAPI app with:
- Issue tracking API (create issue, add comment, get status)
- Todo CRUD API (what the Agent will implement)

Run: uvicorn main:app --reload --port 8000
"""

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime
import uuid

app = FastAPI(title="Mandatory Blocking Skills Verification Mock")

# In-memory storage
issues_db = {}
todos_db = {}

# ============ Issue API ============

class IssueCreate(BaseModel):
    title: str
    description: str

class CommentCreate(BaseModel):
    content: str

class Issue(BaseModel):
    id: str
    title: str
    description: str
    status: str  # todo, in_progress, done, blocked
    comments: List[dict]
    created_at: str

@app.post("/api/issues", response_model=Issue)
def create_issue(issue: IssueCreate):
    issue_id = str(uuid.uuid4())[:8]
    issues_db[issue_id] = {
        "id": issue_id,
        "title": issue.title,
        "description": issue.description,
        "status": "todo",
        "comments": [],
        "created_at": datetime.now().isoformat()
    }
    return issues_db[issue_id]

@app.get("/api/issues/{issue_id}")
def get_issue(issue_id: str):
    if issue_id not in issues_db:
        raise HTTPException(status_code=404, detail="Issue not found")
    return issues_db[issue_id]

@app.post("/api/issues/{issue_id}/comments")
def add_comment(issue_id: str, comment: CommentCreate):
    if issue_id not in issues_db:
        raise HTTPException(status_code=404, detail="Issue not found")

    comment_obj = {
        "id": str(uuid.uuid4())[:8],
        "content": comment.content,
        "created_at": datetime.now().isoformat()
    }
    issues_db[issue_id]["comments"].append(comment_obj)
    return {"success": True, "comment": comment_obj}

@app.patch("/api/issues/{issue_id}/status")
def update_status(issue_id: str, status: dict):
    if issue_id not in issues_db:
        raise HTTPException(status_code=404, detail="Issue not found")
    issues_db[issue_id]["status"] = status.get("status", "todo")
    return {"success": True, "status": issues_db[issue_id]["status"]}

@app.get("/api/issues")
def list_issues():
    return list(issues_db.values())

# ============ Todo API (for Agent to implement) ============

class TodoCreate(BaseModel):
    title: str
    description: Optional[str] = ""

class Todo(BaseModel):
    id: str
    title: str
    description: str
    completed: bool
    created_at: str

@app.post("/api/todos", response_model=Todo)
def create_todo(todo: TodoCreate):
    todo_id = str(uuid.uuid4())[:8]
    todos_db[todo_id] = {
        "id": todo_id,
        "title": todo.title,
        "description": todo.description,
        "completed": False,
        "created_at": datetime.now().isoformat()
    }
    return todos_db[todo_id]

@app.get("/api/todos")
def list_todos():
    return list(todos_db.values())

@app.delete("/api/todos/{todo_id}")
def delete_todo(todo_id: str):
    if todo_id not in todos_db:
        raise HTTPException(status_code=404, detail="Todo not found")
    del todos_db[todo_id]
    return {"success": True}

@app.get("/health")
def health_check():
    return {"status": "ok", "issues_count": len(issues_db), "todos_count": len(todos_db)}

# Reset endpoint for testing
@app.post("/reset")
def reset():
    issues_db.clear()
    todos_db.clear()
    return {"success": True}

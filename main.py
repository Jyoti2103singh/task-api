from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI(
    title="Task API",
    description="Simple CRUD API using FastAPI",
    version="1.0.0"
)

# -----------------------------
# Data Model
# -----------------------------
class Task(BaseModel):
    title: str
    completed: bool = False

# -----------------------------
# In-Memory Database
# -----------------------------
tasks = [
    {"id": 1, "title": "Learn FastAPI", "completed": False},
    {"id": 2, "title": "Complete CRUD Assignment", "completed": False}
]

# -----------------------------
# Home Endpoint
# -----------------------------
@app.get("/")
def home():
    return {"message": "Welcome to Task API!"}

# -----------------------------
# Health Check
# -----------------------------
@app.get("/health")
def health():
    return {"status": "OK"}

# -----------------------------
# Get All Tasks
# -----------------------------
@app.get("/tasks")
def get_tasks():
    return tasks

# -----------------------------
# Get Task by ID
# -----------------------------
@app.get("/tasks/{task_id}")
def get_task(task_id: int):
    for task in tasks:
        if task["id"] == task_id:
            return task
    return {"message": "Task not found"}

# -----------------------------
# Create Task
# -----------------------------
@app.post("/tasks")
def create_task(task: Task):
    new_task = {
        "id": len(tasks) + 1,
        "title": task.title,
        "completed": task.completed
    }
    tasks.append(new_task)
    return {
        "message": "Task created successfully",
        "task": new_task
    }

# -----------------------------
# Update Task
# -----------------------------
@app.put("/tasks/{task_id}")
def update_task(task_id: int, updated_task: Task):
    for task in tasks:
        if task["id"] == task_id:
            task["title"] = updated_task.title
            task["completed"] = updated_task.completed
            return {
                "message": "Task updated successfully",
                "task": task
            }
    return {"message": "Task not found"}

# -----------------------------
# Delete Task
# -----------------------------
@app.delete("/tasks/{task_id}")
def delete_task(task_id: int):
    for task in tasks:
        if task["id"] == task_id:
            tasks.remove(task)
            return {"message": "Task deleted successfully"}
    return {"message": "Task not found"}
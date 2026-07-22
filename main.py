from fastapi import FastAPI, HTTPException, Response, status
from pydantic import BaseModel, Field

app = FastAPI(
    title="Task API",
    description="Simple CRUD API using FastAPI",
    version="1.0.0"
)

class TaskCreate(BaseModel):
    title: str = Field(..., min_length=1)
    completed: bool = False

tasks = [
    {"id": 1, "title": "Learn FastAPI", "completed": False},
    {"id": 2, "title": "Complete CRUD Assignment", "completed": False},
    {"id": 3, "title": "Push project to GitHub", "completed": False},
]

@app.get("/", summary="API Information")
def home():
    return {
        "name": "Task API",
        "version": "1.0",
        "endpoints": ["/tasks"]
    }

@app.get("/health", summary="Health Check")
def health():
    return {"status": "ok"}

@app.get("/tasks", summary="Get All Tasks")
def get_tasks():
    return tasks

@app.get("/tasks/{task_id}", summary="Get Task by ID")
def get_task(task_id: int):
    for task in tasks:
        if task["id"] == task_id:
            return task
    raise HTTPException(
        status_code=404,
        detail=f"Task {task_id} not found"
    )

@app.post(
    "/tasks",
    summary="Create Task",
    status_code=status.HTTP_201_CREATED
)
def create_task(task: TaskCreate):

    if task.title.strip() == "":
        raise HTTPException(
            status_code=400,
            detail="Title cannot be empty"
        )

    new_task = {
        "id": max([t["id"] for t in tasks], default=0) + 1,
        "title": task.title,
        "completed": task.completed
    }

    tasks.append(new_task)
    return new_task

@app.put("/tasks/{task_id}", summary="Update Task")
def update_task(task_id: int, updated_task: TaskCreate):

    if updated_task.title.strip() == "":
        raise HTTPException(
            status_code=400,
            detail="Title cannot be empty"
        )

    for task in tasks:
        if task["id"] == task_id:
            task["title"] = updated_task.title
            task["completed"] = updated_task.completed
            return task

    raise HTTPException(
        status_code=404,
        detail=f"Task {task_id} not found"
    )

@app.delete(
    "/tasks/{task_id}",
    summary="Delete Task",
    status_code=status.HTTP_204_NO_CONTENT
)
def delete_task(task_id: int):

    for task in tasks:
        if task["id"] == task_id:
            tasks.remove(task)
            return Response(status_code=204)

    raise HTTPException(
        status_code=404,
        detail=f"Task {task_id} not found"
    )
import os
import time
import uuid
from fastapi import FastAPI, HTTPException, Response

app = FastAPI()

START_TIME = time.time()
READY_DELAY_SECONDS = int(os.environ.get("READY_DELAY_SECONDS", "5"))

todos = []

@app.get("/healthz")
def healthz():
    return {"status": "ok"}

@app.get("/readyz")
def readyz(response: Response):
    elapsed = time.time() - START_TIME
    if elapsed < READY_DELAY_SECONDS:
        response.status_code = 503
        return {"status": "warming up", "elapsed": round(elapsed, 1)}
    return {"status": "ready"}

@app.get("/todos")
def list_todos():
    return todos

@app.post("/todos")
def create_todo(payload: dict):
    if "title" not in payload:
        raise HTTPException(status_code=400, detail="title is required")
    todo = {"id": str(uuid.uuid4()), "title": payload["title"], "done": False}
    todos.append(todo)
    return todo

@app.get("/config")
def get_config():
    return {
        "APP_GREETING": os.environ.get("APP_GREETING", "hello from todo-api"),
        "API_KEY": os.environ.get("API_KEY", "not-set"),
    }

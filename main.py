
from fastapi import Depends, FastAPI, HTTPException
from pydantic import BaseModel
from sqlalchemy.orm import Session

import models
from database import Base, SessionLocal, engine

Base.metadata.create_all(bind=engine)

app = FastAPI()


class TaskCreate(BaseModel):
    title: str


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.get("/health")
def status():
    return {"status": "healthy"}


@app.post("/tasks")
def create_tasks(request: TaskCreate, db: Session = Depends(get_db)):
    task = models.Task(title=request.title)

    db.add(task)
    db.commit()
    db.refresh(task)

    return {"id": task.id, "title": task.title}


@app.get("/tasks")
def get_tasks(db: Session = Depends(get_db)):
    tasks = db.query(models.Task).all()
    return [{"id": task.id, "title": task.title} for task in tasks]


@app.get("/tasks/{tasks_id}")
def get_tasks_by_id(tasks_id: int, db: Session = Depends(get_db)):
    task = db.query(models.Task).filter(
        models.Task.id == tasks_id
    ).first()

    if task is None:
        raise HTTPException(status_code=404, detail="Task not found")

    return {"id": task.id, "title": task.title}


@app.put("/tasks/{tasks_id}")
def change(tasks_id: int, request: TaskCreate, db: Session = Depends(get_db)):
    task = db.query(models.Task).filter(
        models.Task.id == tasks_id
    ).first()

    if task is None:
        raise HTTPException(status_code=404, detail="Task not found")

    task.title = request.title
    db.commit()
    db.refresh(task)

    return {"id": task.id, "title": task.title}


@app.delete("/tasks/{tasks_id}")
def delete_task(tasks_id: int, db: Session = Depends(get_db)):
    task = db.query(models.Task).filter(
        models.Task.id == tasks_id
    ).first()

    if task is None:
        raise HTTPException(status_code=404, detail="Task not found")

    db.delete(task)
    db.commit()

    return {"message": "Success"}

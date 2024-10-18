from sqlalchemy.orm import Session
from models import Task
from typing import Optional, List


def create_task(db: Session, user_id: int, title: str, description: Optional[str]) -> None:
    task = Task(title=title, owner_id=user_id, description=description)
    db.add(task)
    db.commit()


def get_user_tasks(db: Session, user_id: int) -> List[Task]:
    return db.query(Task).filter(Task.owner_id == user_id, Task.is_done == False).all()


def get_task_by_id(db: Session, task_id: int) -> Optional[Task]:
    return db.query(Task).filter(Task.id == task_id).first()


def delete_task(db: Session, task_id: int) -> None:
    db.query(Task).filter(Task.id == task_id).delete()
    db.commit()


def mark_task_done(db: Session, task_id: int) -> None:
    db.query(Task).filter(Task.id == task_id).update({"is_done": True})
    db.commit()

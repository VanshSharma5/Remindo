from datetime import datetime, timedelta, timezone
from sqlalchemy.orm import Session, joinedload
from sqlalchemy import and_

from app.models.user import Task, User

# CREATE USER
def create_user(db: Session, email: str, profession: str):
    user = User(email=email, profession=profession)
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


# ADD TASK
def create_task(db: Session, user_id: int, title: str, description: str, priority: str, scheduled_at):
    task = Task(
        title=title,
        description=description,
        priority=priority,
        scheduled_at=scheduled_at,
        user_id=user_id
    )
    db.add(task)
    db.commit()
    db.refresh(task)
    return task


# GET NEXT DAY TASKS (EAGER LOADING FIX APPLIED)
def get_next_day_tasks(db: Session):
    tomorrow_start = datetime.now().replace(
        hour=0, minute=0, second=0, microsecond=0
    ) + timedelta(days=1)

    tomorrow_end = tomorrow_start + timedelta(days=1)

    tasks = db.query(Task).options(
        joinedload(Task.user)  # 🔥 prevents MissingGreenlet
    ).filter(
        and_(
            Task.scheduled_at >= tomorrow_start,
            Task.scheduled_at < tomorrow_end
        )
    ).all()

    return tasks
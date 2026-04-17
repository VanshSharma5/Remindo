from typing import List

from fastapi import APIRouter, Depends, HTTPException, Response, status
from sqlalchemy.orm import Session

from app.api.deps import get_db
from app.models.user import Task, User
from app.schemas.user import UserCreate, TaskCreate, UserResponse
from app.services.task_service import create_user, create_task
from app.services import email

router = APIRouter()


@router.post("/users")
def create_user_route(payload: UserCreate, db: Session = Depends(get_db)):
    return create_user(db, payload.email, payload.profession)


@router.get("/users/{user_email}", response_model=UserResponse)
def get_user_by_email(user_email: str, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.email == user_email).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"User with email {user_email} not exists!",
        )

    return user


@router.options("/users")
async def get_options():
    return Response(
        headers={"Allow": "GET, POST, OPTIONS"}, status_code=status.HTTP_204_NO_CONTENT
    )


@router.post("/tasks/{user_id}")
def add_task_route(user_id: int, payload: TaskCreate, db: Session = Depends(get_db)):
    return create_task(
        db, user_id, payload.title, payload.description, payload.priority, payload.scheduled_at
    )


@router.get("/tasks/{user_id}", response_model=List[TaskCreate])
def get_all_tasks(user_id: int, db: Session = Depends(get_db)):
    tasks = db.query(Task).filter(Task.user_id == user_id).all()
    
    return tasks
    


@router.options("/items/{user_id}")
async def get_options():
    return Response(
        headers={"Allow": "GET, POST, OPTIONS"}, status_code=status.HTTP_204_NO_CONTENT
    )

# Path для динамического параметра, Query для статического параметра
from fastapi import FastAPI, HTTPException, Path, Query, status, Body, Depends
from fastapi.middleware.cors import CORSMiddleware
from typing import Optional, List, Dict, Annotated
from sqlalchemy.orm import Session

from models import User, Task, Base, UserRole, Role
from database import engine, session_local
from schemas import TaskCreate, UserCreate, TaskResponse, UserResponse, UserRoleResponse, UserRoleCreate, \
    RoleResponse

# Пока в инактиве, не понимаю насколько это value
from uuid import uuid4

app = FastAPI()

# Настройка CORS
origins = [
    'http://localhost:8000',
    'http://127.0.0.1:8000'
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=['*'],
    allow_headers=['*']
)



Base.metadata.create_all(bind=engine)


def get_db():
    db = session_local()
    try:
        yield db
    finally:
        db.close()


@app.post("/users/", response_model=UserResponse)
async def create_user(user: UserCreate, db: Session = Depends(get_db)) -> User:
    db_user = User(name=user.name, age=user.age)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)

    return db_user


@app.post("/tasks/", response_model=TaskResponse)
async def create_task(task: TaskCreate, db: Session = Depends(get_db)) -> Task:
    db_user = db.query(User).filter(User.id == task.executor_id).first()
    if db_user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")

    db_task = Task(executor_id=task.executor_id, theme=task.theme, deadline=task.deadline, author_id=task.author_id)
    db.add(db_task)
    db.commit()
    db.refresh(db_task)

    return db_task


@app.post("/userroles/", response_model=UserRoleResponse)
async def create_user_role(user_role: UserRoleCreate, db: Session = Depends(get_db)) -> UserRole:
    db_user_role = User(user_id=user_role.user_id, role_id=user_role.role_id)
    db.add(db_user_role)
    db.commit()
    db.refresh(db_user_role)

    return db_user_role


@app.post("/roles/", response_model=RoleResponse)
async def create_role(role: UserCreate, db: Session = Depends(get_db)) -> Role:
    db_role = Role(name=role.name)
    db.add(db_role)
    db.commit()
    db.refresh(db_role)

    return db_role




@app.get("/tasks/", response_model=List[TaskResponse])
async def tasks(db: Session = Depends(get_db)):
    return db.query(Task).all()

@app.get("/users/", response_model=List[UserResponse])
async def users(db: Session = Depends(get_db)):
    return db.query(User).all()

@app.get("/userroles/", response_model=List[UserRoleResponse])
async def usersRoles(db: Session = Depends(get_db)):
    return db.query(UserRole).all()

@app.get("/roles/", response_model=List[RoleResponse])
async def roles(db: Session = Depends(get_db)):
    return db.query(Role).all()
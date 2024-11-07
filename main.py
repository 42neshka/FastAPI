# Path для динамического параметра, Query для статического параметра
from fastapi import FastAPI, HTTPException, Path, Query, status, Body
from typing import Optional, List, Dict, Annotated
from pydantic import BaseModel, Field
# Пока в инактиве, не понимаю насколько это value
from uuid import uuid4

app = FastAPI()


class User(BaseModel):
    id: int
    name: str
    age: int


class Task(BaseModel):
    id: int
    deadline: str
    theme: str
    author: User


class TaskCreate(BaseModel):
    deadline: str
    theme: str
    author_id: int


class UserCreate(BaseModel):
    name: Annotated[str, Field(..., title='name user', min_length=2, max_length=20)]
    age: Annotated[int, Field(..., title='age user', ge=14, lt=40)]



@app.get("/")
async def start() -> str:
    return "Welcome to Task Manager"


@app.get("/tasks")
async def tasks() -> List[Task]:
    return [Task(**task) for task in tasks_list]


@app.get("/users")
async def users() -> List[User]:
    return [User(**user) for user in users_list]


@app.get("/tasks/{id}")
# 3 точки в Path указывает что id обязательно должен быть передан, иначе будет ошибка
async def tasks_id(id: Annotated[int, Path(..., title='Указывается id задачи', ge=1, lt=100)]) -> Task:
    for task in tasks_list:
        if task["id"] == id:
            return Task(**task)
    raise HTTPException(status_code=500, detail="Task not found")


@app.get("/search")
async def search(task_id: Annotated[
    Optional[int], Query(title='id для поиска задачи', ge=1, lt=100)]) -> Dict[str, Optional[Task]]:
    if task_id:
        for task in tasks_list:
            if task["id"] == task_id:
                return {"data": Task(**task)}
    else:
        return {"data": None}


@app.post("/tasks/add")
async def add_task(task: TaskCreate) -> Task:
    # Проверка на существование пользователя
    author = next((user for user in users_list if user['id'] == task.author_id), None)
    if not author:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")

    # Создаем задачу с уникальным ID
    new_task = Task(
        id = len(tasks_list) + 1,
        deadline = task.deadline,
        theme = task.theme,
        author = author
    )
    tasks_list.append(new_task)

    return new_task


@app.post("/users/add")
async def add_user(user: Annotated[UserCreate,
    Body(..., example={
        'name': 'UserName',
        'age': 18
    })]) -> User:
    # Создаем user с уникальным ID
    new_user = User(
        id = len(users_list) + 1,
        name = user.name,
        age = user.age,
    )
    tasks_list.append(new_user)

    return new_user



users_list = [
    {'id': 4, 'name': 'Alex', 'age': 26},
    {'id': 5, 'name': 'Damir', 'age': 20},
    {'id': 2, 'name': 'Bulat', 'age': 22},
    {'id': 1, 'name': 'Bone', 'age': 26},
    {'id': 3, 'name': 'Ilyas', 'age': 27}
]


tasks_list = [
    {"id": 1, "deadline":"30 nov", 'theme': "k8s", 'author': users_list[2]},
    {"id": 2, "deadline":"10 nov", 'theme': "web-socket", 'author': users_list[1]},
    {"id": 3, "deadline":"10 nov", 'theme': "fastapi", 'author': users_list[0]},
    {"id": 4, "deadline":"25 nov", 'theme': "cam", 'author': users_list[3]},
    {"id": 5, "deadline":"30 nov", 'theme': "asterisk", 'author': users_list[4]}
]
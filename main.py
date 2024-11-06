from http.client import HTTPException
from fastapi import FastAPI
from typing import Optional, List, Dict
from pydantic import BaseModel

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
async def tasks_id(id: int) -> Task:
    for task in tasks_list:
        if task["id"] == id:
            return Task(**task)


@app.get("/search")
async def search(task_id: Optional[int] = None) -> Dict[str, Optional[Task]]:
    if task_id:
        for task in tasks_list:
            if task["id"] == task_id:
                return {"data": Task(**task)}
    else:
        return {"data": None}


@app.post("/tasks/add")
async def add_task(task: TaskCreate) -> Task:
    author = next((user for user in users_list if user['id'] == task.author_id), None)
    if not author:
        raise HTTPException(status_code=404, detail="User not found")

    new_task_id = len(tasks_list) + 1

    new_task = {'id': new_task_id, 'deadline': task.deadline, 'theme': task.theme, 'author': author}
    tasks_list.append(new_task)

    return Task(**new_task)


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
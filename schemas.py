from pydantic import BaseModel
from sqlalchemy import orm



class UserBase(BaseModel):
    name: str
    age: int


class User(UserBase):
    id: int

    class Config:
        orm.mode = True


class UserCreate(UserBase):
    pass



class TaskBase(BaseModel):
    executor_id: int
    deadline: str
    theme: str
    author_id: int


class TaskResponse(TaskBase):
    id: int

    class Config:
        orm.mode = True


class TaskCreate(TaskBase):
    pass



class UserRoleBase(BaseModel):
    user_id: int
    role_id: int


class UserRoleResponse(UserRoleBase):
    id: int

    class Config:
        orm.mode = True


class UserRoleCreate(UserRoleBase):
    pass



class RoleBase(BaseModel):
    name_role: str


class RoleResponse(RoleBase):
    id: int

    class Config:
        orm.mode = True


class RoleCreate(RoleBase):
    pass
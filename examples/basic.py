from typing import List
from fastapi.applications import FastAPI

from fastapi.exceptions import HTTPException
from pydantic.main import BaseModel
from fastapi_classy import FastAPIClassy


class User(BaseModel):
    name: str
    age: int


class Status(BaseModel):
    success: bool


# This is an example, don't use a global variable in production!
users = {
    1: User(name="John", age=42),
    2: User(name="Doe", age=37),
    3: User(name="Jane", age=37),
}


class UserRouter(FastAPIClassy):
    def get(self, user_id: int) -> User:
        if user_id not in users:
            raise HTTPException(404)
        return users[user_id]

    def index(self) -> List[User]:
        return list(users.values())

    def delete(self, user_id: int) -> Status:
        if user_id not in users:
            raise HTTPException(404)
        del users[user_id]
        return Status(success=True)

    def post(self, user: User) -> User:
        user_id = max(users.keys()) + 1
        users[user_id] = user
        return user


app = FastAPI()
app.include_router(UserRouter.make_router(), prefix="/users", tags=["users"])


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, port=8001)

from dataclasses import dataclass

from fastapi import APIRouter, FastAPI
from fastapi.exceptions import HTTPException
from pydantic.main import BaseModel
import pytest

from fastapi_classy.fastapi_classy import FastAPIClassy


@dataclass
class User:
    # Mimics an ORM object
    id: int
    username: str
    password: str


users = {
    1: User(id=1, username="rembrandt", password="vanrijn"),
    2: User(id=2, username="vincent", password="vangogh"),
    3: User(id=3, username="johannes", password="vermeer"),
}


class UserSchema(BaseModel):
    id: int
    username: str


class UserRouter(FastAPIClassy):
    class Meta:
        tags = ["user"]

    def get(self, user_id: int) -> UserSchema:
        if user_id not in users:
            raise HTTPException(401)
        return UserSchema.from_orm(users[user_id])


def test_router():
    app = FastAPI()

    before = len(app.routes)

    app.include_router(UserRouter.make_router())
    assert app.routes
    assert len(app.routes) == before + 1

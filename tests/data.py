from dataclasses import dataclass
from pydantic import BaseModel


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

    class Config:
        orm_mode = True

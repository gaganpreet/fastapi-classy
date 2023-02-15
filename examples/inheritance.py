from typing import Any, Generic, List, TypeVar, Union
from fastapi.applications import FastAPI

from fastapi.exceptions import HTTPException
from pydantic import BaseModel
from pydantic.generics import GenericModel
from fastapi_classy import FastAPIClassy


class User(BaseModel):
    name: str
    age: int


class Car(BaseModel):
    name: str
    color: str


class Another(BaseModel):
    id: int


# This is an example, don't use a global variable in production!
Users = {
    1: User(name="John", age=42),
    2: User(name="Doe", age=37),
    3: User(name="Jane", age=37),
}

Cars = {
    1: Car(name="Ford", color="red"),
    2: Car(name="Fiat", color="white"),
    3: Car(name="Volvo", color="black"),
    4: Car(name="Audi", color="blue"),
}


T = TypeVar("T", User, Car)


class BaseRouter(FastAPIClassy, Generic[T]):
    model: Any = {}

    def get(self, item_id: int) -> T:
        if item_id not in self.model:
            raise HTTPException(404)
        return self.model[item_id]

    # def index(self) -> List[T]:
    # return list(self.model.values())

    # def delete(self, item_id: int) -> None:
    # if item_id not in self.model:
    # raise HTTPException(404)
    # del self.model[item_id]

    # def post(self, item: T) -> T:
    # item_id = max(self.model.keys()) + 1
    # self.model[item_id] = item
    # return item


class UserRouter(BaseRouter[User]):
    model = Users


class CarRouter(BaseRouter[Car]):
    model = Cars


app = FastAPI()


@app.get("/")
def test():
    return "hi"


app.include_router(UserRouter.make_router(), prefix="/users", tags=["users"])
app.include_router(CarRouter.make_router(), prefix="/cars", tags=["cars"])


if __name__ == "__main__":
    import uvicorn

    uvicorn.run("examples.inheritance:app", port=8001, reload=True)

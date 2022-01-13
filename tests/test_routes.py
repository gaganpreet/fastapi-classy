from starlette.testclient import TestClient
from fastapi.applications import FastAPI

from tests.users import UserRouter


def test_router(classy_class) -> None:
    app = FastAPI()
    before = len(app.routes)

    app.include_router(classy_class.make_router(), prefix="/users")
    assert app.routes
    assert len(app.routes) == before + 1

    test_client = TestClient(app)

    resp = test_client.get("/users/1")
    assert resp.status_code == 200, resp.text
    assert resp.json() == {"id": 1, "username": "rembrandt"}

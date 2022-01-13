from fastapi.exceptions import HTTPException
import pytest

from fastapi_classy import FastAPIClassy
from tests import data as test_data


@pytest.fixture(scope="session")
def classy_class():
    class UserRouter(FastAPIClassy):
        class Meta:
            tags = ["user"]

        def get(self, user_id: int) -> test_data.UserSchema:
            if user_id not in test_data.users:
                raise HTTPException(401)
            return test_data.UserSchema.from_orm(test_data.users[user_id])

    return UserRouter

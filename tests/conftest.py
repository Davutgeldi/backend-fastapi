import pytest

from src.main import app
from src.config import settings
from src.database import BaseModel, engine_null_pool
from src.models import * # noqa

from httpx import AsyncClient


@pytest.fixture(scope="session", autouse=True)
async def check_mode():
    assert settings.MODE == "TEST"


@pytest.fixture(scope="session", autouse=True)
async def create_database(check_mode):
    async with engine_null_pool.begin() as conn:
        await conn.run_sync(BaseModel.metadata.drop_all)
        await conn.run_sync(BaseModel.metadata.create_all)


@pytest.fixture(scope="session", autouse=True)
async def register_user(create_database):
    async with AsyncClient(app=app, base_url="http://test") as client:
        await client.post(
            "/auth/register",
            json={
                "first_name": "Gurban",
                "last_name": "Lebron",
                "patronymic": "Curry",
                "phone": "+9961669876",
                "email": "davut@gmail.com",
                "password": "jamono"
            }
        )
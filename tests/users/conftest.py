import pytest
from fastapi.testclient import TestClient

from app import app
from config import Settings


def get_settings_override():
    return Settings(testing=1)


@pytest.fixture(scope="module")
def test_client():
    with TestClient(app) as client:
        yield client


@pytest.fixture
def mock_db_session():
    session = "dd"
    return session

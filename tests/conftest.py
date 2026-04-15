from copy import deepcopy

import pytest
from fastapi.testclient import TestClient

from src.app import app, activities


@pytest.fixture
def client():
    return TestClient(app)


@pytest.fixture(autouse=True)
def reset_activities_state():
    """Restore the in-memory database before and after each test."""
    original_state = deepcopy(activities)
    activities.clear()
    activities.update(deepcopy(original_state))

    yield

    activities.clear()
    activities.update(deepcopy(original_state))

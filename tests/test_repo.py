from fastapi.testclient import TestClient
from unittest.mock import patch, MagicMock
from app.main import app
from app.database.db import get_db

client = TestClient(app)

def fake_db():
    db = MagicMock()
    yield db

app.dependency_overrides[get_db] = fake_db


def test_add_repo_invalid_user():
    db = MagicMock()
    db.query().filter().first.return_value = None

    # Use a generator function to yield the mock db
    def override_get_db():
        yield db
        
    app.dependency_overrides[get_db] = override_get_db

    response = client.post(
        "/repo/add",
        params={"user_id": 999, "name": "test", "owner": "octocat"}
    )

    assert response.status_code == 401  # Or 401, depending on your logic
    # Clean up overrides after the test
    app.dependency_overrides.clear()



@patch("app.routes.repo.fetch_last_hour_commits")
def test_sync_repo(mock_fetch):
    mock_fetch.return_value = []

    repo = MagicMock()
    repo.id = 1
    repo.owner = "octocat"
    repo.name = "hello"
    repo.last_synced_at = None

    db = MagicMock()
    # Ensure the chain of calls on the mock works as expected
    db.query.return_value.filter.return_value.first.return_value = repo

    # FIX: Return the mock object directly instead of an iterator
    app.dependency_overrides[get_db] = lambda: db

    try:
        response = client.post("/repo/sync/1")
        assert response.status_code == 200
    finally:
        # Best Practice: Always clear overrides after the test
        app.dependency_overrides.clear()


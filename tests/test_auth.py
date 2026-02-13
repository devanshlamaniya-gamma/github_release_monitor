from fastapi.testclient import TestClient
from unittest.mock import MagicMock, patch
from app.main import app
from app.database.db import get_db

client = TestClient(app)


def test_add_repo_invalid_user():
    db = MagicMock()
    db.query().filter().first.return_value = None

    app.dependency_overrides[get_db] = lambda: db

    response = client.post(
        "/repo/add",
        params={
            "user_id": 999,
            "name": "test",
            "owner": "octocat"
        }
    )

    assert response.status_code == 401


@patch("app.routes.repo.fetch_last_hour_commits")
def test_sync_repo(mock_fetch):
    mock_fetch.return_value = []

    repo = MagicMock()
    repo.id = 1
    repo.owner = "octocat"
    repo.name = "hello"
    repo.last_synced_at = None

    db = MagicMock()
    db.query().filter().first.return_value = repo

    app.dependency_overrides[get_db] = lambda: db

    response = client.post("/repo/sync/1")

    assert response.status_code == 200

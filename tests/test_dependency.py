import pytest
from fastapi.testclient import TestClient
from app.authentication.dependencies import get_current_user  
from unittest.mock import MagicMock, patch


from  app.main import app
from fastapi import FastAPI


app = FastAPI()


client = TestClient(app)

@patch("app.authentication.dependencies.decode_access_token")
def test_get_current_user_success(mock_decode):
    mock_decode.return_value = {"user_id": 1}

    mock_db = MagicMock()
    mock_user = MagicMock()

    mock_db.query().filter().first.return_value = mock_user

    result = get_current_user(token="valid_token", db=mock_db)

    assert result == mock_user


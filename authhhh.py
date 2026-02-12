import pytest
from fastapi.testclient import TestClient
from unittest.mock import MagicMock, patch
from app.routes.auth import register_user

from app.main import app as ap


client = TestClient(ap)


def test_register_success():

  
    mock_db = MagicMock()

 
    mock_db.query().filter().first.return_value = None

 
    fake_user_input = MagicMock()
    fake_user_input.email = "test@example.com"
    fake_user_input.password = "123456"


    fake_new_user = MagicMock()
    fake_new_user.id = 1
    fake_new_user.email = "test@example.com"

    
    def fake_refresh(user):
        user.id = 1

    mock_db.refresh.side_effect = fake_refresh

    result = register_user(fake_user_input, mock_db)

    assert result["email"] == "test@example.com"
    assert "token" in result
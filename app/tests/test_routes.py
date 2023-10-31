from unittest.mock import patch, Mock
from fastapi.testclient import TestClient
from app.routes import app as routes
import pytest
from app.schemas import ExchangeRateSchema

client = TestClient(routes)

@pytest.fixture
def db_session():
    with patch("app.routes.sessionmaker") as mock_sessionmaker:
        mock_session = Mock()
        mock_sessionmaker.return_value = mock_session
        yield mock_session

def test_currency_conversion_valid(db_session):
    data = ExchangeRateSchema(from_currency="USD", to_currency="EUR", rate=100)
    with patch('fastapi.testclient.TestClient.post') as mock_post:
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "from_currency": "USD",
            "to_currency": "EUR",
            "rate": 100,
            "converted_rate": 85
        }

        mock_post.return_value = mock_response

        response = client.post("/convert_currency", json=data.dict())

    expected_result = {
        "from_currency": "USD",
        "to_currency": "EUR",
        "rate": 100,
        "converted_rate": 85
    }

    assert response.status_code == 200
    result = response.json()
    assert result == expected_result


def test_currency_conversion_invalid_currency(db_session):
    from fastapi import HTTPException
    data = {"from_currency":"INVALID",
            "to_currency":"EUR", 
            "rate":100}

    with patch('fastapi.testclient.TestClient.post') as mock_post:
        mock_response = Mock()
        mock_response.status_code = 422
        mock_response.json.return_value = {
            "detail": [
                {
                    "type": "value_error",
                    "loc": ["body", 0, "from_currency"],
                    "msg": "Currency code must be exactly 3 characters",
                }
            ]
        }

        mock_post.return_value = mock_response
            
        response = client.post("/convert_currency", json=data)

    assert response.status_code == 422
    assert response.json()["detail"][0]["msg"] == "Currency code must be exactly 3 characters"

def test_currency_conversion_invalid_amount(db_session):
    data = {"from_currency":"USD", 
            "to_currency":"EUR",
            "rate":-100}
    
    with patch('fastapi.testclient.TestClient.post') as mock_post:
        mock_response = Mock()
        mock_response.status_code = 422
        mock_response.json.return_value = {
            "detail": [
                {
                    "type": "value_error",
                    "loc": ["body", 0, "from_currency"],
                    "msg": "Rate must be greater than zero",
                }
            ]
        }
        mock_post.return_value = mock_response

        response = client.post("/convert_currency", json=data)

    assert response.status_code == 422
    assert response.json()["detail"][0]["msg"] == "Rate must be greater than zero"


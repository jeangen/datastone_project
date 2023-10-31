import pytest
from unittest.mock import patch, Mock
from app.exchange_rate_provider import GoogleExchangeRateProvider, InvalidCurrencyError

def test_fetch_exchange_rate_success():
    with patch('app.exchange_rate_provider.requests.get') as mock_get:
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.text = '<div class="BNeawe iBp4i AP7Wnd">0.0066</div>'
        mock_get.return_value = mock_response

        provider = GoogleExchangeRateProvider()
        rate = provider.fetch_exchange_rate("JPY", "USD")
        print(rate)
        assert rate == 0.0066

def test_fetch_exchange_rate_connection_error():
    with patch('app.exchange_rate_provider.requests.get') as mock_get:
        mock_response = Mock()
        mock_response.status_code = 404
        mock_get.return_value = mock_response

        provider = GoogleExchangeRateProvider()
        with pytest.raises(ConnectionError):
            provider.fetch_exchange_rate("USD", "EUR")

def test_parse_exchange_rate_success():
    html = '<div class="BNeawe iBp4i AP7Wnd">0.0066</div>'
    provider = GoogleExchangeRateProvider()
    rate = provider.parse_exchange_rate(html)
    
    assert rate == 0.0066

def test_parse_exchange_rate_invalid_currency():
    html = 'Invalid currency or exchange rate not found.'
    provider = GoogleExchangeRateProvider()
    
    with pytest.raises(InvalidCurrencyError):
        provider.parse_exchange_rate(html)

def test_get_exchange_rate_info_success():
    with patch('app.exchange_rate_provider.GoogleExchangeRateProvider.fetch_exchange_rate') as mock_fetch:
        mock_fetch.return_value = 1.23

        provider = GoogleExchangeRateProvider()
        info = provider.get_exchange_rate_info("USD", "EUR")

        assert info == {"from_currency": "USD", "exchange_rate": 1.23, "to_currency": "EUR"}

def test_get_exchange_rate_info_connection_error():
    with patch('app.exchange_rate_provider.GoogleExchangeRateProvider.fetch_exchange_rate') as mock_fetch:
        mock_fetch.side_effect = ConnectionError("Failed to fetch data from Google")

        provider = GoogleExchangeRateProvider()
        info = provider.get_exchange_rate_info("USD", "EUR")

        assert info == {'error': 'Failed to fetch data from Google'}

def test_get_exchange_rate_info_invalid_currency():
    with patch('app.exchange_rate_provider.GoogleExchangeRateProvider.fetch_exchange_rate') as mock_fetch:
        mock_fetch.side_effect = InvalidCurrencyError("Invalid currency or exchange rate not found.")

        provider = GoogleExchangeRateProvider()
        info = provider.get_exchange_rate_info("USD", "EUR")

        assert info == {'error': 'Invalid currency or exchange rate not found.'}

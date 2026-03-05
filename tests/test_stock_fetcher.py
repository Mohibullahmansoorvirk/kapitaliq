from pipelines.stock_fetcher import StockFetcher
import pytest

def test_fetch_returns_data_with_close_column():

    fetcher = StockFetcher("SAP.DE")

    data = fetcher.fetch("5d")
    
    assert not data.empty # data is not empty
    assert "Close" in data.columns # Close is in columns

def test_latest_price_is_positive():
    fetcher = StockFetcher("SAP.DE")
    price = fetcher.latest_price()
    assert price > 0

def test_invalid_ticker_raises_value_error():
    fetcher = StockFetcher("INVALID_XYZ")
    with pytest.raises(ValueError):
        fetcher.fetch()
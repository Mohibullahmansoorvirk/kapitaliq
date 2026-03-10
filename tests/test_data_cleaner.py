from pipelines.stock_fetcher import StockFetcher
from pipelines.data_cleaner import DataCleaner

def test_does_clean_return_expected_columns():

    fetcher = StockFetcher("SAP.DE")
    data = fetcher.fetch()

    cleaner = DataCleaner(data)
    clean_data = cleaner.clean()

    
    assert list(clean_data.columns) == ["Open", "High", "Low", "Close", "Volume"]

def test_dtypes_correct_after_cleaning():
    fetcher = StockFetcher("SAP.DE")
    data = fetcher.fetch()
    cleaner = DataCleaner(data)
    clean_data = cleaner.clean()

    assert clean_data["Volume"].dtype == "int64"

    for col in ["Open", "High", "Low", "Close"]:
        assert clean_data[col].dtype == "float64"
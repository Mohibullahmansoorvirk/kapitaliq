from unittest.mock import patch
from pipelines.data_storage import save_stock_data
import pandas as pd
import pytest

#fake stock data mimicking yfinance output with date as index
fake_df = pd.DataFrame({

    "Open": [420.0, 380.0],
    "High": [420.0, 380.0],
    "Low": [420.0, 380.0],
    "Close": [420.0, 380.0],
    "Volume": [420, 380]
}, index = ["2026-02-06", "2026-02-07"])

#temporarily replace SessionLocal inside storage.py with a fake session (MagicMock)so to not create a real session with postgreSQL DB for test
@patch("pipelines.data_storage.SessionLocal")
#patch automatically creates the MagicMock and passes it in this function as fake_session_local_class
def test_save_stock_data(fake_session_local_class):
    #call the real function "save_stock_data" - internally db = SessionLocal() now becomes db = fake_session_local_class()
    #so db inside the function is automatically fake_session_local_class.return_value
    save_stock_data("SAP.DE", fake_df)
    
    #return_value is the "fake db" instance that was returned when fake_session_local_class() was called inside the function
    #.commit.called checks if commit() was ever called on that fake db instance
    assert fake_session_local_class.return_value.commit.called == True


@patch("pipelines.data_storage.SessionLocal")
def test_rollback_stock_data(fake_session_local_class):
    #side effect is something you attach to a mock method to make it behave in a specific way when called. In this case simulating a crash of DB.
    fake_session_local_class.return_value.execute.side_effect = Exception("db crashed")

    #to test that a function raises an exception in pytest
    with pytest.raises(Exception):
        save_stock_data("SAP.DE", fake_df)

    assert fake_session_local_class.return_value.rollback.called == True
import logging
logger = logging.getLogger(__name__)
import pandas as pd


class DataCleaner:

    def __init__(self, data: pd.DataFrame) -> None:
        self._data = data.copy() #to copy the original raw data incase it gets corrupts somewhere in the pipeline   
        logger.info(f"data successfully imported for cleaning")

    #keep only relevant columns
    def _drop_unnecessary_columns(self) -> pd.DataFrame:
        logger.info(f"dropping un-necessary columns")
        self._data = self._data[["Open","High","Low","Close","Volume"]]
        return self._data

    #ensure correct data types
    def _fix_dtypes(self) -> pd.DataFrame:
        logger.info(f"fixing data types")

        for col in ["Open","High","Low","Close"]:
            self._data[col] = self._data[col].astype(float)
            logger.info(f"fixing float64 data type")

        if self._data["Volume"].dtype != 'int64':
            self._data["Volume"] = self._data["Volume"].astype(int)
            logger.info(f"fixing volume data type")

        return self._data

    #forward fill missing values      
    def _handle_nulls(self) -> pd.DataFrame:   
        logger.info(f"handling nulls")     
        self._data = self._data.ffill()
        
        return self._data
    
    #drop duplicate dates
    def _remove_duplicates(self) -> pd.DataFrame: 
        logger.info(f"removing duplicate dates")  
        self._data = self._data[~self._data.index.duplicated()]
        return self._data
    
    #runs all cleaning steps, returns clean DataFrame
    def clean(self) -> pd.DataFrame: 
        logger.info(f"cleaning the data frame")         
        self._drop_unnecessary_columns()
        self._handle_nulls()
        self._fix_dtypes()
        self._remove_duplicates()
        return self._data

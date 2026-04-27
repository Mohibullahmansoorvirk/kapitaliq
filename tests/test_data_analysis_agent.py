from agents.data_analysis_agent import DataAnalystAgent
import pandas as pd
from unittest.mock import MagicMock


fake_df = pd.DataFrame({
    "Close": [100.0] * 19 + [120.0], "Volume": [150000] * 20
    }, index = pd.date_range(start="2026-01-01", periods=20, freq="D"))

def test_calculate_indicators():
    
    mock_llm = MagicMock() # we dont use llm but when calling DataAnalystAgent() - if a fake llm is not given then it calls the groq llm everytime a test runs

    analyst_agent_part_1= DataAnalystAgent(mock_llm)
    indicators_dict = analyst_agent_part_1._calculate_indicators(fake_df)

    assert indicators_dict["moving_average_past_20_days"] == 101.0
    assert indicators_dict["price_change_past_20_days"] == 20.0
    assert indicators_dict["average_volume_past_20_days"] == 150000
    assert indicators_dict["highest_value_past_20_days"] == 120.0
    assert indicators_dict["lowest_value_past_20_days"] == 100.0

def test_analyst_agent_response():
    #here we need mock_llm - because we need to give the exact response we would expect in this test
    mock_llm = MagicMock() 
    #when LCEL calls the mock_llm - it returns a string directly. so we dont need to extract and StrOutputParser gets the string and outputs the same string.
    mock_llm.return_value = "Stock Name: SAP.DE\nFinancial Decision: BULLISH\nReason: reasons given"
    #creates the agent object with fake LLM inputed
    analyst_agent_part_2= DataAnalystAgent(mock_llm)
    #this calls the run function with fake_df and ticker name
    #calculate_indicators calculates real indicators from fake data
    #Chain is built; Chain invokes mock_llm
    #Mock returns the fake string; Parser passes it through; response gets the string
    agent_test_response = analyst_agent_part_2.run(fake_df, "SAP.DE")

    #Test: verifies that mock was called exactly once during run() and that the chain actually invoked the LLM
    mock_llm.assert_called_once()
    #Test: run() returns a string that can be used by the system downstream
    assert isinstance(agent_test_response, str)
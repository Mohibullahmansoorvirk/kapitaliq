from pipelines.trend_signal_agent import TrendSignalAgent
import pandas as pd

def test_bullish():

    fake_df_bullish = pd.DataFrame({
    "Close": [100.0] * 19 + [120.0]
    }, index = pd.date_range(start="2026-01-01", periods=20, freq="D"))

    agent= TrendSignalAgent("SAP.DE")
    agent_decision= agent.run(fake_df_bullish)

    assert agent_decision == "BULLISH"


def test_bearish():

    fake_df_bearish = pd.DataFrame({
    "Close": [120.0] * 19 + [100.0]
    }, index = pd.date_range(start="2026-01-01", periods=20, freq="D"))

    agent= TrendSignalAgent("SAP.DE")
    agent_decision= agent.run(fake_df_bearish)

    assert agent_decision == "BEARISH"
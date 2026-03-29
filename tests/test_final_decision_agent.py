from agents.final_decision_agent import FinalDecisionAgent
from unittest.mock import MagicMock

fake_data_agent_response = "BEARISH because the data proves it"
fake_nlp_agent_response = "BEARISH because the news proves it"

def test_final_decision_agent_response():
    mock_llm = MagicMock()
    mock_llm.return_value = "Stock Name: SAP.DE\nFinancial Decision: BULLISH\nReason: reasons given"
    final_decision_agent = FinalDecisionAgent(mock_llm)

    final_decision_test_response = final_decision_agent.run(fake_data_agent_response, fake_nlp_agent_response, "SAP.DE")

    assert isinstance(final_decision_test_response, str)
   
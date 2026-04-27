from unittest.mock import MagicMock, patch
from agents.intent_router import IntentRouter

@patch("agents.intent_router.ChatGroq")
def test_intent_router_on_demand(mock_groq):
    #mock the LLM to return a controlled classification response
    mock_llm = MagicMock()
    mock_groq.return_value = mock_llm
    mock_llm.return_value = "INTENT: ON_DEMAND\nTICKER: SAP.DE"

    #run the router with a live price query
    router = IntentRouter()
    intent, ticker = router.run("What is SAP trading at right now?")

    #verify correct intent and ticker extracted from LLM response
    assert intent == "ON_DEMAND"
    assert ticker == "SAP.DE"
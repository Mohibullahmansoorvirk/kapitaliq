from agents.nlp_agent import NLPAgent
import pandas as pd
from unittest.mock import MagicMock, patch
from pipelines.rag_retriever import retrieve_relevant_chunks

fake_list_of_strings = ["SAP reported strong earnings...", "SAP revenue grew 12%...", "SAP cloud division expanding..."]

@patch("agents.nlp_agent.retrieve_relevant_chunks")
def test_nlp_agent_response(fake_retrieve_relevant_chunks_class):
    fake_retrieve_relevant_chunks_class.return_value = fake_list_of_strings
    mock_llm = MagicMock()
    mock_llm.return_value = "Stock Name: SAP.DE\nFinancial Decision: BULLISH\nReason: reasons given"
    nlp_agent = NLPAgent(mock_llm)
    nlp_agent_response = nlp_agent.run("SAP earnings performance", "SAP.DE", k=3)
    
    #Test: verifies that mock was called exactly once during run() and that the chain actually invoked the LLM
    mock_llm.assert_called_once()
    #Test: run() returns a string that can be used by the system downstream
    assert isinstance(nlp_agent_response, str)

    assert "SAP.DE" in nlp_agent_response


@patch("agents.nlp_agent.retrieve_relevant_chunks")
def test_news_chunk_empty(fake_retrieve_relevant_chunks_class):
    fake_retrieve_relevant_chunks_class.return_value = []
    mock_llm = MagicMock()
    mock_llm.return_value = "Stock Name: SAP.DE\nFinancial Decision: BULLISH\nReason: reasons given"
    nlp_agent = NLPAgent(mock_llm)
    nlp_agent_response = nlp_agent.run("SAP earnings performance", "SAP.DE", k=3)
    
    #Test: verifies that mock was never called as the News Chunk was returned Empty
    mock_llm.assert_not_called()
    #Test: run() returns a string that can be used by the system downstream
    assert isinstance(nlp_agent_response, str)

    assert "No News Chunks" in nlp_agent_response
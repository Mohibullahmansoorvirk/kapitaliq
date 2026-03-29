from typing import TypedDict
import pandas as pd
from unittest.mock import patch
from agents.orchestrator import data_analysis_agent_node, nlp_agent_node, final_decision_agent_node
import httpx

fake_state = {"ticker": "",
        "user_query": "",
        "cleaned_data": "",
        "analysis_result": "",
        "nlp_result": "",
        "final_decision": ""}

#test for normal node path with agent runs as intended and returns the response under correct key
@patch("agents.orchestrator.DataAnalystAgent")
def test_data_analysis_agent_node(fake_data_analyst_agent_class):
    fake_data_analyst_agent_class.return_value.run.return_value = "SAP.DE is bullish"
    data_agent_node_response = data_analysis_agent_node(fake_state)

    assert data_agent_node_response["analysis_result"] == "SAP.DE is bullish"

#test for when agent raises an httpx.ConnectError and node returns fallback string 
@patch("agents.orchestrator.DataAnalystAgent")
def test_data_analysis_agent_exception(fake_data_analyst_agent_class):
    fake_data_analyst_agent_class.return_value.run.side_effect = httpx.ConnectError("timeout")
    data_agent_node_response = data_analysis_agent_node(fake_state)

    assert data_agent_node_response["analysis_result"] == "Analysis currently unavailable. Please try again later."

##############################################################################################################

@patch("agents.orchestrator.NLPAgent")
def test_nlp_agent_node(fake_nlp_agent_class):
    fake_nlp_agent_class.return_value.run.return_value = "SAP.DE is bullish"
    nlp_agent_node_response = nlp_agent_node(fake_state)

    assert nlp_agent_node_response["nlp_result"] == "SAP.DE is bullish"

@patch("agents.orchestrator.NLPAgent")
def test_nlp_agent_exception(fake_nlp_agent_class):
    fake_nlp_agent_class.return_value.run.side_effect = httpx.ConnectError("timeout")
    nlp_agent_node_response = nlp_agent_node(fake_state)

    assert nlp_agent_node_response["nlp_result"] == "Response currently unavailable. Please try again later."

##############################################################################################################

@patch("agents.orchestrator.FinalDecisionAgent")
def test_final_agent_node(fake_final_agent_class):
    fake_final_agent_class.return_value.run.return_value = "SAP.DE is bullish"
    final_agent_node_response = final_decision_agent_node(fake_state)

    assert final_agent_node_response["final_decision"] == "SAP.DE is bullish"

@patch("agents.orchestrator.FinalDecisionAgent")
def test_final_agent_exception(fake_final_agent_class):
    fake_final_agent_class.return_value.run.side_effect = httpx.ConnectError("timeout")
    final_agent_node_response = final_decision_agent_node(fake_state)

    assert final_agent_node_response["final_decision"] == "Response currently unavailable. Please try again later."

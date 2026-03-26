from typing import TypedDict
import pandas as pd
from langgraph.graph import StateGraph #The primary class used to define the structure, nodes and state schema of agentic workflow
from langgraph.graph import START, END
from agents.data_analysis_agent import DataAnalystAgent
from agents.nlp_agent import NLPAgent

#AgentState dictionary is the "State" in langGraph (shared dict amongst all nodes)
#Nodes are the functions or individual Agent
#Edges are the connections / path of the flow

#typeddict is  a dictionary where you declare upfront what keys exist 
# and what type each value must be
class AgentState(TypedDict):
    ticker: str #input for analysis & nlp agents
    user_query: str #input for nlp agent
    cleaned_data: pd.DataFrame #input for analysis agent
    analysis_result: str #ouput from analysis agent
    nlp_result: str #output from nlp agent
    final_decision: str #final output from orchestrator after combining both agent outputs


def data_analysis_agent_node (state: AgentState) -> dict:

    data_agent = DataAnalystAgent()
    #AgentState is a class (blueprint) - actual data lives in the "state" parameter passed in the function
    data_agent_response = data_agent.run(state["cleaned_data"], state["ticker"]) 

    return {"analysis_result": data_agent_response}

def nlp_agent_node (state: AgentState) -> dict:

    nlp_agent = NLPAgent()
    nlp_agent_response = nlp_agent.run(state["user_query"], state["ticker"])

    return {"nlp_result": nlp_agent_response}

def final_decision_agent_node (state: AgentState) -> dict:
    
    """
    takes in input as : state["analysis_result"] & state["nlp_result"]

    return {"final_decision": final_agent_response}
    """
    return {"final_decision": ""}


graph = StateGraph(AgentState)  # tell it what state looks like
graph.add_node("data_analysis_agent_node", data_analysis_agent_node)  # register the node
graph.add_node("nlp_agent_node", nlp_agent_node)  # register the node
graph.add_node("final_decision_agent_node", final_decision_agent_node)  # register the node
graph.add_edge("data_analysis_agent_node", "nlp_agent_node")  # connecting nodes - After analysis_node finishes and updates state, immediately run nlp_node
graph.add_edge("nlp_agent_node", "final_decision_agent_node")  # connect nodes
graph.add_edge(START, "data_analysis_agent_node")  # where execution starts
graph.add_edge("final_decision_agent_node", END)  # where execution stops
app = graph.compile()  # lock and load


if __name__ == "__main__":
    print(app)
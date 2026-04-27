from typing import TypedDict
import pandas as pd
from langgraph.graph import StateGraph #The primary class used to define the structure, nodes and state schema of agentic workflow
from langgraph.graph import START, END
from agents.data_analysis_agent import DataAnalystAgent
from agents.nlp_agent import NLPAgent
from agents.final_decision_agent import FinalDecisionAgent

# tenacity is the library that uses decorators to automatically retry failing functions with customizable retry logic i.e. backoff
from tenacity import retry, stop_after_attempt, wait_exponential, retry_if_exception_type
import httpx

#plain variable to store the retry decorator written for retry and backoff strategy
#Max attempts - 3 | Wait- exponential, min=2s, max=10s
#only network/API related Exceptions are handled in "retry" parameter
with_retry = retry(
    stop=stop_after_attempt(3),
    wait=wait_exponential(multiplier=1, min=2, max=10),
    retry=retry_if_exception_type((httpx.ConnectError, httpx.TimeoutException))
)

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

    @with_retry #decorator already defined on top of the file for reusability for all 3 agents. 
    def run_with_retry():
        #AgentState is a class (blueprint) - actual data lives in the "state" parameter passed in the function
        data_agent_response = data_agent.run(state["cleaned_data"], state["ticker"]) 

        return data_agent_response
    try:
        data_analysis_result = run_with_retry()
        return {"analysis_result": data_analysis_result}
    
    # fallback strategy if after 3 tries still an exception thrown
    except Exception: 
        return {"analysis_result": "Analysis currently unavailable. Please try again later."}

def nlp_agent_node (state: AgentState) -> dict:

    nlp_agent = NLPAgent()
    @with_retry
    def run_with_retry():
        nlp_agent_response = nlp_agent.run(state["user_query"], state["ticker"])

        return nlp_agent_response
    try:
        nlp_result = run_with_retry()
        return {"nlp_result": nlp_result}
    
    # fallback strategy
    except Exception:
        return {"nlp_result": "Response currently unavailable. Please try again later."}

def final_decision_agent_node (state: AgentState) -> dict:
    
    final_decision_agent = FinalDecisionAgent()
    @with_retry
    def run_with_retry():
        final_decision_agent_response = final_decision_agent.run(state["analysis_result"], state["nlp_result"], state["ticker"])

        return final_decision_agent_response
    try:
        final_decision_result = run_with_retry()
        return {"final_decision": final_decision_result}
    
    # fallback strategy
    except Exception: 
        return {"final_decision": "Response currently unavailable. Please try again later."}


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
    from pipelines.stock_fetcher import StockFetcher
    from pipelines.data_cleaner import DataCleaner

    fetcher = StockFetcher("SAP.DE")
    data = fetcher.fetch()

    cleaner = DataCleaner(data)
    clean_data = cleaner.clean()

    #we need to give the initial state dictionary as input to invoke
    #all the starting values the graph needs before any node runs
    #The agents outputs are empty and will be filled by the node
    response = app.invoke({ 
        "ticker": "SAP.DE",
        "user_query": "How is SAP doing?",
        "cleaned_data": clean_data,
        "analysis_result": "",
        "nlp_result": "",
        "final_decision": ""

    }) 

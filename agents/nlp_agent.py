from typing import Optional
from configs.agents import SharedConfig
from configs.agents import ConfigNLPAgent
from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate, SystemMessagePromptTemplate, HumanMessagePromptTemplate
from langchain_core.output_parsers import StrOutputParser
from pipelines.rag_retriever import retrieve_relevant_chunks


class NLPAgent:
    def __init__(self, llm: Optional[ChatGroq] = None): # type hint of llm says "llm" is either a ChatGroq object or None
        self.shared_config = SharedConfig()
        self.config_agent = ConfigNLPAgent()

                #Rule of "or" in python -> Return the first value that is truthy. If the first is falsy, return the second where None is falsy
        #for tests when we pass a mock_llm then it takes a fake_llm and in prod we pass nothing as arugument and it takes the ChatGroq model
        self.llm = llm or ChatGroq(
            api_key = self.shared_config.groq_api_key, 
            model = self.shared_config.groq_model_name,
            max_tokens = self.config_agent.max_tokens,
            temperature = self.config_agent.temperature,
            timeout = self.config_agent.timeout
            )
        
    
    def run(self, user_query: str, ticker: str, k: int = 3) -> str:
        news_chunks = retrieve_relevant_chunks(user_query, ticker, k)

        if not news_chunks: # gaurdrail for if no chunks are retrieved
            response = f"No News Chunks were retreived hence no output can be generated"

            return response

        else:
            combined_news_chunk = "\n\n".join(f"<article>\n{chunk}\n</article>" for chunk in news_chunks) # XML-style tags with double newlines for clear separation

            #in system message - trading philosophy is on purpose left-out
            system_template = "You are a financial Analyst for the biggest Investment Firm in Germany. " \
            "You always respond in a clear fiancial language. " \
            "You never speculate or be creative. You must always output either BULLISH or BEARISH. " \
            "Never output both. Never say it depends. " \
            "If you cant output with certainity based on the information provided, say Data provided is not enough. " \
            "Always end your response, in the next line, with the wording Disclaimer: This decision is purely based on the information I have."

            human_template = "User Query = {user_query}" \
            "News Chunks = {combined_news_chunk}" \
            "Name of the Stock = {ticker} " \
            "For every Name of the Stock , understand the User Query and the News Chunks" \
            "Based on your understanding, answer in the following format:" \
            "Stock Name : Name of the Stock \n" \
            "Financial Decision: Either Bullish or Bearish based on News Chunks and User Query \n" \
            "Reason: clear , concise reasoning of how did you come up with the financial decision of maximum 80 words"

            #.from_template("text") - takes a plain string and wraps it into a LangChain message template object
            system_message_template = SystemMessagePromptTemplate.from_template(system_template)
            human_message_template = HumanMessagePromptTemplate.from_template(human_template)
            #.from_messages([system, human]) - takes a list of message template objects and combines them into one complete prompt template
            combined_prompt = ChatPromptTemplate.from_messages([system_message_template, human_message_template])

            # LCEL (LangChain Expression Language) chain 
            #uses the pipe operator (|) to connect components like prompts, models, and parsers into a single, executable pipeline
            # the flow of pipeline is from left to right; first prompt then model then parser
            # general command : chain = prompt | model | parser
            chain = combined_prompt | self.llm | StrOutputParser() # output parser that extracts the .content from the raw output of LLM

            #invoke() passes the input parameters to the first component in the chain. In our case to the prompt. Invoke should always take the dict.
            #we pass the dict - where the key of dict should match the {place_holder} name. LangChain matches them then automatically
            response = chain.invoke({"user_query": user_query,
            "combined_news_chunk": combined_news_chunk,
            "ticker": ticker})

            return response
        
if __name__ == "__main__":
    news_analyst = NLPAgent()
    agent_response = news_analyst.run("SAP earnings performance", "SAP.DE", k=3)
    print(agent_response)
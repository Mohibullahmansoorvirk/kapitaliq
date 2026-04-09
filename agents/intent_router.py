from typing import Optional
from configs.agents import SharedConfig
from configs.agents import ConfigIntentRouter
from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate, SystemMessagePromptTemplate, HumanMessagePromptTemplate
from langchain_core.output_parsers import StrOutputParser

class IntentRouter:
    def __init__(self, llm: Optional[ChatGroq] = None): # type hint of llm says "llm" is either a ChatGroq object or None
        self.shared_config = SharedConfig()
        self.config_agent = ConfigIntentRouter()
        #Rule of "or" in python -> Return the first value that is truthy. If the first is falsy, return the second where None is falsy
        #for tests when we pass a mock_llm then it takes a fake_llm and in prod we pass nothing as arugument and it takes the ChatGroq model
        self.llm = llm or ChatGroq(
            api_key = self.shared_config.groq_api_key, 
            model = self.shared_config.groq_model_name,
            max_tokens = self.config_agent.max_tokens,
            temperature = self.config_agent.temperature,
            timeout = self.config_agent.timeout
            )
        
    def run(self, user_query: str) -> tuple[str, str]:
        #in system message - trading philosophy is on purpose left-out
            system_template = "You are an intent classifier for a stock market assistant. " \
            "You must respond ONLY in this exact format with no other text: " \
            "INTENT: <DASHBOARD or ON_DEMAND or GENERAL> " \
            "TICKER: <ticker in DAX format or None> " \
            "Do not explain. Do not add any other text."  \
            "Given a user query, classify it into exactly one of these 3 categories: " \
            "DASHBOARD: If the user query asks for information which doesnot require current refreshed updated financial and/or news data" \
            "ON_DEMAND: If the user query asks for information which does require current refreshed updated financial and/or news data  " \
            "GENERAL: If the user query asks for general information which doesnot require any financial and/or news data  " \
            "Also extract the stock ticker in DAX format (e.g. SAP.DE, SIE.DE). " \
            "If no ticker mentioned, return None for ticker. " \
            "Return exactly in this format: " \
            "INTENT: <category> \n " \
            "TICKER: <ticker or None>" \

            human_template = "User Query = {user_query}" \

        

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
            raw_response = chain.invoke({"user_query": user_query})
            print(raw_response)
            lines = raw_response.strip().split('\n')
            try:
                intent = next(line.split(': ')[1] for line in lines if line.startswith('INTENT'))
                # fallback handling
                if intent not in ["DASHBOARD", "ON_DEMAND", "GENERAL"]:
                    intent = "DASHBOARD"
                ticker = next(line.split(': ')[1] for line in lines if line.startswith('TICKER'))
                return (intent, ticker)
            #fallback handling
            except (StopIteration, IndexError):
                 return "GENERAL", None
            

        
if __name__ == "__main__":
    intent_router = IntentRouter()
    intent_router_response = intent_router.run("How are you doing")
    print(intent_router_response)
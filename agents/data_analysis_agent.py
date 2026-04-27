from typing import Optional
from configs.agents import SharedConfig
from configs.agents import ConfigDataAnalysisAgent
from langchain_groq import ChatGroq
import pandas as pd
from langchain_core.prompts import ChatPromptTemplate, SystemMessagePromptTemplate, HumanMessagePromptTemplate
from langchain_core.output_parsers import StrOutputParser


class DataAnalystAgent:
    def __init__(self, llm: Optional[ChatGroq] = None): # type hint of llm says "llm" is either a ChatGroq object or None

        self.shared_config = SharedConfig()
        self.config_agent = ConfigDataAnalysisAgent()

        #Rule of "or" in python -> Return the first value that is truthy. If the first is falsy, return the second where None is falsy
        #for tests when we pass a mock_llm then it takes a fake_llm and in prod we pass nothing as arugument and it takes the ChatGroq model
        self.llm = llm or ChatGroq(
            api_key = self.shared_config.groq_api_key, 
            model = self.shared_config.groq_model_name,
            max_tokens = self.config_agent.max_tokens,
            temperature = self.config_agent.temperature,
            timeout = self.config_agent.timeout
            )
        
    #Phase 1 - calculating 5 indicators which can be fed into Phase 2 (LLM)
    def _calculate_indicators(self, cleaned_data: pd.DataFrame) -> dict:
        close_column = cleaned_data["Close"]
        moving_average_past_20_days = float((close_column.iloc[-20:]).mean())
        price_change_past_20_days = float(((close_column.iloc[-1]) - (close_column.iloc[-20]))/((close_column.iloc[-20]))* 100)
        average_volume_past_20_days = int((cleaned_data["Volume"].iloc[-20:]).mean())
        highest_value_past_20_days = float((close_column.iloc[-20:]).max())
        lowest_value_past_20_days = float((close_column.iloc[-20:]).min())

        return {
            "moving_average_past_20_days": moving_average_past_20_days,
            "price_change_past_20_days": price_change_past_20_days,
            "average_volume_past_20_days": average_volume_past_20_days,
            "highest_value_past_20_days": highest_value_past_20_days,
            "lowest_value_past_20_days": lowest_value_past_20_days,
                    }
    
    #Phase 2 - Input the dict from phase 1 to the LLM
    def _prompt_build(self):
        #System message - who the LLM is, how it behaves, rules it follows always
        #Human message - the actual task with the data for this specific call

        #in system message - trading philosophy is on purpose left-out
        system_template = "You are a financial Analyst for the biggest Investment Firm in Germany. " \
        "You always respond in a clear fiancial language. " \
        "You never speculate or be creative. You must always output either BULLISH or BEARISH. " \
        "Never output both. Never say it depends. " \
        "If you cant do the analysis then say I cant perform the analysis. " \
        "Always end your response, in the next line, with the wording Disclaimer: This decision is purely based on the data I have."

        human_template = "Moving Average = {moving_average_past_20_days} " \
        "Percentage Change = {price_change_past_20_days}% " \
        "Volume Average = {average_volume_past_20_days} shares " \
        "Highest Value = {highest_value_past_20_days} " \
        "Lowest Value = {lowest_value_past_20_days} " \
        "Name of the Stock = {ticker} " \
        "For every Name of the Stock , analyze the rest five values and output in the following format: " \
        "Stock Name : Name of the Stock \n" \
        "Financial Decision: Either Bullish or Bearish based on your analysis \n" \
        "Reason: clear , concise reasoning of how did you come up with the financial decision of maximum 80 words"
        
        #.from_template("text") - takes a plain string and wraps it into a LangChain message template object
        system_message_template = SystemMessagePromptTemplate.from_template(system_template)
        human_message_template = HumanMessagePromptTemplate.from_template(human_template)
        #.from_messages([system, human]) - takes a list of message template objects and combines them into one complete prompt template
        combined_prompt = ChatPromptTemplate.from_messages([system_message_template, human_message_template])

        return combined_prompt
    

    def run(self, cleaned_data: pd.DataFrame, ticker: str) -> str:
        indicators_dict = self._calculate_indicators(cleaned_data)
        indicators_dict["ticker"] = ticker

        # LCEL (LangChain Expression Language) chain 
        #uses the pipe operator (|) to connect components like prompts, models, and parsers into a single, executable pipeline
        # the flow of pipeline is from left to right; first prompt then model then parser
        # general command : chain = prompt | model | parser
        chain = self._prompt_build() | self.llm | StrOutputParser() # output parser that extracts the .content from the raw output of LLM

        #invoke() passes the input parameters to the first component in the chain. In our case to the prompt
        #we pass the dict - where the key of dict should match the {place_holder} name. LangChain matches them then automatically
        response = chain.invoke(indicators_dict)

        return response


if __name__ == "__main__":

    from pipelines.stock_fetcher import StockFetcher
    from pipelines.data_cleaner import DataCleaner

    fetcher = StockFetcher("SAP.DE")
    data = fetcher.fetch()

    cleaner = DataCleaner(data)
    clean_data = cleaner.clean()

    analyst_agent= DataAnalystAgent()
    agent_response= analyst_agent.run(clean_data, "SAP.DE")


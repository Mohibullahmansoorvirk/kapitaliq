"""
configs/agents.py is a file where all general configurations shared across all agents and agent specific cofnigurations are written here. 
For clear and clean pipeline setting
"""

from dataclasses import dataclass
from dotenv import load_dotenv
import os
load_dotenv()

@dataclass
class SharedConfig:
    """Class of shared configs across all agents"""
    groq_api_key: str = os.getenv("GROQ_API_KEY", "") # second argument in case API key field is empty or not found
    groq_model_name: str = "llama-3.3-70b-versatile"


@dataclass
class ConfigDataAnalysisAgent:
    """Class of specific configs for Data Analysis Agent"""
    #A short clear financial summary hinting the trend signal with explanation is around 150 words. 
    #0.75 words per token for our model  = 200 tokens and adding a 20% buffer is max tokens on output of an LLM
    max_tokens: int = 250
    #Temperature is set to 0 as we do not want creativity and only want clear answers based on highest probabilites
    temperature : float = 0.0
    #timeout is set to 10 seconds as because our model takes an average of 3 seconds to reply this short response 
    #and adding a buffer of 3x due to network latency or load is maximum 10 seconds
    timeout : int = 10


@dataclass
class ConfigNLPAgent:
    """Class of specific configs for NLP Agent"""
    #A short clear financial summary hinting the trend signal with explanation is around 150 words. 
    #0.75 words per token for our model  = 200 tokens and adding a 20% buffer is max tokens on output of an LLM
    max_tokens: int = 250
    #Temperature is set to 0 as we do not want creativity and only want clear answers based on highest probabilites
    temperature : float = 0.0
    #timeout is set to 10 seconds as because our model takes an average of 3 seconds to reply this short response 
    #and adding a buffer of 3x due to network latency or load is maximum 10 seconds
    timeout : int = 10

@dataclass
class ConfigFinalDecisionAgent:
    """Class of specific configs for Final Decision Agent"""
    #Analyzing outputs of both agents and returning a sensible answer
    #0.75 words per token for our model  = 250 tokens and adding a 20% buffer is max tokens on output of an LLM
    max_tokens: int = 300
    #Temperature is set to 0 as we do not want creativity and only want clear answers based on highest probabilites
    temperature : float = 0.0
    #timeout is set to 10 seconds as because our model takes an average of 3 seconds to reply this short response 
    #and adding a buffer of 3x due to network latency or load is maximum 10 seconds
    timeout : int = 10

@dataclass
class ConfigIntentRouter:
    """Class of specific configs for IntentRouter"""
    #Based on the user query need to classify it into one of the 3 categories
    #0.75 words per token for our model
    #only need to return the classification and the ticker. 50 tokens + adding 20%
    max_tokens: int = 60
    #Temperature is set to 0 as we do not want creativity and only want clear answers based on highest probabilites
    temperature : float = 0.0
    #timeout is set to 10 seconds as because our model takes an average of 3 seconds to reply this short response 
    #and adding a buffer of 3x due to network latency or load is maximum 10 seconds
    timeout : int = 10
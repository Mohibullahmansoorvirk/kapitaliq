"""
General:
Embedder Takes a list of chunk strings -> passes them to nomic-embed-text -> returns a list of vectors

Embedder.py (This file)->  instead of downloading and running locally, used "HuggingFace Inference API" 

Call their servers directly. They run the model, we get the result back. IMPORTANT for running the KapitalIQ on cloud

embedder_ollama.py (other file) -> embedder models gets downloaded by ollama from HuggingFace and runs locally.

"""
from langchain_huggingface import HuggingFaceEndpointEmbeddings #this calls HuggingFace Servers. No local model required
from dotenv import load_dotenv
import os
load_dotenv()


class Embedder:

    def __init__(self, model="nomic-embed-text") -> None:
        
        self.model = HuggingFaceEndpointEmbeddings(
            model="sentence-transformers/all-mpnet-base-v2", #also 768 dimensions as the embedder model from Ollama
            huggingfacehub_api_token=os.getenv("HUGGINGFACE_API_KEY")
        )
    
    def embed(self, chunks: list[str]) -> list[list[float]]:
        vectors = self.model.embed_documents(chunks)
        return vectors
    

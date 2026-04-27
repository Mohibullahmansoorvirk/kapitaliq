"""
Embedder_ollama Takes a list of chunk strings -> passes them to nomic-embed-text -> returns a list of vectors

This embedder models gets downloaded by ollama from HuggingFace and runs locally. Made a new file embedder.py 

Embedder.py (other file)->  instead of downloading and running locally, used "HuggingFace Inference API" IMPORTANT for running the KapitalIQ on cloud

Call their servers directly. They run the model, we get the result back
"""
from langchain_ollama import OllamaEmbeddings

class Embedder:

    def __init__(self, model="nomic-embed-text") -> None: #model dimensions = 768 dimensions
        self.model = OllamaEmbeddings(model=model)
    
    def embed(self, chunks: list[str]) -> list[list[float]]:
        vectors = self.model.embed_documents(chunks)
        return vectors
    

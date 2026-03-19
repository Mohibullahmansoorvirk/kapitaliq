"""
Embedder Takes a list of chunk strings -> passes them to nomic-embed-text -> returns a list of vectors
"""
from langchain_ollama import OllamaEmbeddings

class Embedder:

    def __init__(self, model="nomic-embed-text") -> None:
        self.model = OllamaEmbeddings(model=model)
    
    def embed(self, chunks: list[str]) -> list[list[float]]:
        vectors = self.model.embed_documents(chunks)
        return vectors
    

import os
import numpy as np

from sentence_transformers import SentenceTransformer

from .search_utils import (
    CACHE_DIR,
    load_movies,
)


class SemanticSearch:

    def __init__(self):
        self.embeddings = None
        self.documents = None
        self.document_map = {}
        self.embeddings_path = os.path.join(CACHE_DIR, "movie_embeddings.npy")
        self.model = SentenceTransformer('all-MiniLM-L6-v2')

    def generate_embedding(self, text):
        if not text or not text.strip():
            raise ValueError("Input text cannot be empty.")
        return self.model.encode([text][0])
    
    def build_embeddings(self, documents):
        self.documents = documents
        rep = []
        for doc in self.documents:
            self.document_map[doc["id"]] = doc
            rep.append(f"{doc['title']}: {doc['description']}")
        self.embeddings = self.model.encode(rep, show_progress_bar=True)
        with open(self.embeddings_path, "wb") as f:
            np.save(f, self.embeddings)
        return self.embeddings
    
    def load_or_create_embeddings(self, documents):
        self.documents = documents
        rep = []
        for doc in self.documents:
            self.document_map[doc["id"]] = doc
            rep.append(f"{doc['title']}: {doc['description']}")
        if os.path.exists(self.embeddings_path):
            with open(self.embeddings_path, "rb") as f:
                self.embeddings = np.load(f)
            if len(self.embeddings) == len(self.documents):
                return self.embeddings
            else: 
                return self.build_embeddings(documents)
        else: 
            return self.build_embeddings(documents)
        
    def search(self, query, limit):
        if not self.embeddings:
            raise ValueError("No embeddings loaded. Call `load_or_create_embeddings` first.")
        query_embd = self.generate_embedding(query)
        result = []
        for emb in self.embeddings


def verify_model():
    ses = SemanticSearch()
    print(f"Model loaded: {ses.model}")
    print(f"Max sequence length: {ses.model.max_seq_length}")


def embed_text(text):
    ses = SemanticSearch()
    embedding = ses.generate_embedding(text)
    print(f"Text: {text}")
    print(f"First 3 dimensions: {embedding[:3]}")
    print(f"Dimensions: {embedding.shape[0]}")


def verify_embeddings():
    ses = SemanticSearch()
    documents = load_movies()
    embeddings = ses.load_or_create_embeddings(documents)
    print(f"Number of docs:   {len(documents)}")
    print(f"Embeddings shape: {embeddings.shape[0]} vectors in {embeddings.shape[1]} dimensions")


def embed_query_text(query):
    ses = SemanticSearch()
    embedding = ses.generate_embedding(query)
    print(f"Query: {query}")
    print(f"First 5 dimensions: {embedding[:5]}")
    print(f"Shape: {embedding.shape}")


def cosine_similarity(vec1, vec2):
    dot_product = np.dot(vec1, vec2)
    norm1 = np.linalg.norm(vec1)
    norm2 = np.linalg.norm(vec2)

    if norm1 == 0 or norm2 == 0:
        return 0.0

    return dot_product / (norm1 * norm2)
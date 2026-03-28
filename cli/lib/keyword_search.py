import os
import string
import pickle

from .search_utils import (
    CACHE_DIR,
    DEFAULT_SEARCH_LIMIT, 
    load_movies, 
    load_stopwords
)

from nltk.stem import PorterStemmer

from collections import defaultdict


class InvertedIndex:

    def __init__(self):
        self.index = defaultdict(set)
        self.docmap = {}
        self.index_path = os.path.join(CACHE_DIR, "index.pkl")
        self.docmap_path = os.path.join(CACHE_DIR, "docmap.pkl")

    
    def __add_document(self, doc_id, text):
        tokenized_text = tokenize_text(text)
        for token in tokenized_text:
            self.index[token].add(doc_id)

    def get_documents(self, term):
        return sorted(self.index.get(term, set()))
    
    def build(self):
        movies = load_movies()
        for movie in movies:
            self.docmap[movie['id']] = movie
            self.__add_document(movie['id'], f"{movie['title']} {movie['description']}")

    def save(self):
        os.makedirs(CACHE_DIR, exist_ok=True)   
        with open(self.index_path, "wb") as f:
            pickle.dump(self.index, f)
        with open(self.docmap_path, "wb") as f:
            pickle.dump(self.docmap, f)

    def load(self):
        with open(self.index_path, "rb") as f:
            self.index = pickle.load(f)
        with open(self.docmap_path, "rb") as f:
            self.docmap = pickle.load(f)


def build_command() -> None:
    idx = InvertedIndex()
    idx.build()
    idx.save()


def search_command(query: str, limit: int = DEFAULT_SEARCH_LIMIT) -> list[dict]:
    idx = InvertedIndex()
    idx.load()
    query_tokens = tokenize_text(query)
    seen, results = set(), []
    for query_token in query_tokens:
        matching_doc_ids = idx.get_documents(query_token)
        for doc_id in matching_doc_ids:
            if doc_id in seen:
                continue
            seen.add(doc_id)
            results.append(idx.docmap[doc_id])
            if len(results) >= limit:
                return results
    return results


def has_matching_token(query_tokens: list[str], title_tokens: list[str]) -> bool:
    for query_token in query_tokens:
        for title_token in title_tokens:
            if query_token in title_token:
                return True
    return False


def preprocesse_text(text: str) -> str:
    text = text.lower()
    text = text.translate(str.maketrans("", "", string.punctuation))
    return text


def tokenize_text(text: str) -> list[str]:
    stopwords = load_stopwords()
    text = preprocesse_text(text)
    stemmer = PorterStemmer()
    tokens = text.split()
    valid_tokens = []
    for token in tokens:
        if token and token not in stopwords:
            token = stemmer.stem(token)
            valid_tokens.append(token)
    return valid_tokens



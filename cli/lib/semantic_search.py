from sentence_transformers import SentenceTransformer


class SemanticSearch:

    def __init__(self):
        self.model = SentenceTransformer('all-MiniLM-L6-v2')

def verify_model():
    ses = SemanticSearch()
    print(f"Model loaded: {ses.model}")
    print(f"Max sequence length: {ses.model.max_seq_length}")


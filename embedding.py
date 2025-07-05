
# embedding.py
from sentence_transformers import SentenceTransformer

model = SentenceTransformer("BAAI/bge-small-en")

def get_embedding(text: str):
    prefix = "Represent this sentence for searching relevant passages: "
    return model.encode(prefix + text).tolist()

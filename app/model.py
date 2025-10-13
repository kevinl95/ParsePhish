from sentence_transformers import SentenceTransformer
import faiss
import requests
from bs4 import BeautifulSoup
import numpy as np
import os

MODEL_NAME = os.getenv("MODEL_NAME", "sentence-transformers/all-MiniLM-L6-v2")
INDEX_PATH = os.getenv("INDEX_PATH", "phish_index.faiss")
VEC_DIM = 384  # for MiniLM-L6-v2

# Load model and FAISS index
model = SentenceTransformer(MODEL_NAME)
index = faiss.read_index(INDEX_PATH)
labels = np.load("labels.npy", allow_pickle=True)

def extract_text_from_url(url: str):
    try:
        html = requests.get(url, timeout=5).text
        soup = BeautifulSoup(html, "html.parser")
        return " ".join(soup.stripped_strings)[:5000]
    except Exception as e:
        return f"Error fetching: {e}"

def get_phish_score(url: str):
    text = extract_text_from_url(url)
    emb = model.encode([text])
    distances, indices = index.search(emb, k=3)
    phish_votes = sum(labels[i] == "phish" for i in indices[0])
    score = phish_votes / len(indices[0])
    highlights = ["verify account", "password", "urgent", "click here"] if "click" in text.lower() else []
    return float(score), highlights

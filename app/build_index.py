#!/usr/bin/env python3
"""
Build FAISS index from phishing corpus data
This is kept for backward compatibility - use download_data.py for production
"""
from sentence_transformers import SentenceTransformer
import faiss
import numpy as np
import json
import os

MODEL_NAME = os.getenv("MODEL_NAME", "intfloat/e5-small-v2")

def build_index():
    """Build FAISS index from existing corpus data"""
    print("Loading model...")
    model = SentenceTransformer(MODEL_NAME)

    print("Loading corpus...")
    if os.path.exists("phish_corpus.json"):
        with open("phish_corpus.json") as f:
            corpus = json.load(f)
    else:
        print("❌ phish_corpus.json not found. Run download_data.py first.")
        return False

    texts = [c["text"] for c in corpus]
    labels = [c["label"] for c in corpus]

    print("Generating embeddings...")
    embeddings = model.encode(texts, show_progress_bar=True)

    print("Building FAISS index...")
    index = faiss.IndexFlatL2(embeddings.shape[1])
    index.add(np.array(embeddings).astype("float32"))

    print("Saving index...")
    faiss.write_index(index, "phish_index.faiss")
    np.save("labels.npy", np.array(labels))
    print("✅ Index built successfully!")
    return True

if __name__ == "__main__":
    build_index()

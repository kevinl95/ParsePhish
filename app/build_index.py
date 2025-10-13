from sentence_transformers import SentenceTransformer
import faiss
import numpy as np
import json

MODEL_NAME = "sentence-transformers/all-MiniLM-L6-v2"
model = SentenceTransformer(MODEL_NAME)

with open("phish_corpus.json") as f:
    corpus = json.load(f)

texts = [c["text"] for c in corpus]
labels = [c["label"] for c in corpus]

embeddings = model.encode(texts, show_progress_bar=True)

index = faiss.IndexFlatL2(embeddings.shape[1])
index.add(np.array(embeddings).astype("float32"))

faiss.write_index(index, "phish_index.faiss")
np.save("labels.npy", np.array(labels))
print("✅ Index built successfully!")

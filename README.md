# ParsePhish

> **GPU-powered phishing detection on Google Cloud Run**  
> Let AI do the link clicking — safely.

ParsePhish uses an open-source transformer model and FAISS GPU similarity search to analyze suspicious URLs and email text.  
It runs entirely serverlessly on **Google Cloud Run with NVIDIA L4 GPUs** — no infrastructure, no cold servers, just instant GPU-powered insight.

---
[![Run on Google Cloud](https://deploy.cloud.run/button.svg)](https://deploy.cloud.run?git_repo=https://github.com/kevinl95/ParsePhish)
---

## ⚙️ How It Works

1. **Frontend:** simple HTML + JS page (no frameworks) that lets users submit a URL.  
2. **Backend:** FastAPI service running on Cloud Run GPU:
   - Loads an open-source embedding model (`intfloat/e5-small-v2`)
   - Uses a prebuilt FAISS GPU index of phishing examples
   - Computes similarity and returns a “phishy score”
3. **Infra:** Deployable as a Cloud Run service using NVIDIA L4 GPUs in `europe-west4`.

---

## Features

- Serverless GPU inference (L4)
- Real-time phishing similarity detection
- Embedding-based analysis with FAISS
- Fully open-source and one-click deployable
- Privacy-safe — text never stored

---

## Tech Stack

| Component | Description |
|------------|-------------|
| **Google Cloud Run (GPU)** | Serverless runtime for inference |
| **NVIDIA L4 GPU** | Fast embedding & FAISS similarity search |
| **SentenceTransformers** | Open-source transformer embedding model |
| **FAISS GPU** | Vector similarity search engine |
| **FastAPI** | Lightweight Python web service |
| **Docker** | Containerized runtime environment |

---

## Model Details

ParsePhish uses [**intfloat/e5-small-v2**](https://huggingface.co/intfloat/e5-small-v2),  
a compact open-source embedding model well-suited for real-time similarity tasks.

Pretrained phishing examples are embedded and indexed via **FAISS GPU**,  
allowing cosine similarity scoring in milliseconds.

---

## 🐳 Quickstart (Local)

```bash
git clone https://github.com/YOUR_USERNAME/parsephish
cd parsephish
docker build -t parsephish .
docker run -p 8080:8080 parsephish
```
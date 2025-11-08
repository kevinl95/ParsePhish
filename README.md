# ParsePhish API

> **GPU-powered phishing detection API on Google Cloud Run**  
> Serverless AI-powered email and message analysis for phishing detection.

ParsePhish is a REST API that uses transformer embeddings and GPU-accelerated similarity search to analyze emails, messages, and URLs for phishing indicators. Built for the **Cloud Run GPU Category** hackathon, it runs entirely serverless on **Google Cloud Run with NVIDIA L4 GPUs**.

---
[![Deploy to Google Cloud](https://deploy.cloud.run/button.svg)](https://deploy.cloud.run)
---

## 🚀 Quick Start

### Deploy to Cloud Run
```bash
# Clone the repository
git clone https://github.com/kevinl95/ParsePhish.git
cd ParsePhish

# Deploy to your Google Cloud project
./deploy.sh YOUR_PROJECT_ID europe-west4
```

### API Usage
```bash
# Check API health
curl https://your-service-url/health

# Analyze email content for phishing
curl -X POST https://your-service-url/analyze/email \
  -H 'Content-Type: application/json' \
  -d '{
    "content": "Urgent! Your account will be suspended. Click here to verify.",
    "subject": "Account Security Alert"
  }'

# Analyze URL for phishing indicators
curl -X POST https://your-service-url/analyze/url \
  -H 'Content-Type: application/json' \
  -d '{"url": "https://suspicious-site.com"}'
```

## ⚙️ How It Works

1. **API Endpoints**: RESTful API with endpoints for email and URL analysis
2. **GPU Inference**: Uses NVIDIA L4 GPUs for fast embedding computation and FAISS similarity search
3. **Real-time Analysis**: Processes phishing indicators using transformer embeddings
4. **Auto-scaling**: Serverless deployment scales from 0 to handle traffic spikes
5. **Privacy-First**: Content is analyzed but never stored

---

## 🔧 Architecture

```
┌─────────────────┐    ┌──────────────────┐    ┌─────────────────┐
│   Client App    │───▶│  ParsePhish API  │───▶│  GPU Analysis   │
│                 │    │  (Cloud Run)     │    │  (L4 + FAISS)   │
└─────────────────┘    └──────────────────┘    └─────────────────┘
                              │
                              ▼
                       ┌──────────────────┐
                       │  Response        │
                       │  - phishy_score  │
                       │  - verdict       │
                       │  - suspect_words │
                       └──────────────────┘
```

---

## 📋 API Reference

### `POST /analyze/email`
Analyze email content for phishing indicators.

**Request Body:**
```json
{
  "content": "Email body text",
  "subject": "Email subject (optional)"
}
```

**Response:**
```json
{
  "phishy_score": 0.85,
  "suspect_phrases": ["urgent action", "verify account"],
  "verdict": "Phishing detected"
}
```

### `POST /analyze/url`
Analyze URL content for phishing indicators.

**Request Body:**
```json
{
  "url": "https://example.com"
}
```

### `GET /health`
Health check endpoint.

---

## 🏆 Hackathon Requirements

✅ **Cloud Run GPU Category Requirements:**
- ✅ Deployed on Google Cloud Run
- ✅ Uses NVIDIA L4 GPUs for inference
- ✅ Deployed in `europe-west4` region
- ✅ Uses open-source models (intfloat/e5-small-v2)

✅ **Additional Features:**
- ✅ GPU-accelerated FAISS similarity search
- ✅ Transformer-based text embeddings
- ✅ RESTful API architecture
- ✅ Auto-scaling serverless deployment
- ✅ Health monitoring and probes

---

## 🛠️ Tech Stack

| Component | Technology |
|-----------|------------|
| **Runtime** | Google Cloud Run (GPU-enabled) |
| **GPU** | NVIDIA L4 |
| **Framework** | FastAPI + Python |
| **ML Model** | SentenceTransformers (e5-small-v2) |
| **Vector Search** | FAISS GPU |
| **Container** | Docker with CUDA support |

---

## 🚀 Development

### Local Development
```bash
# Install dependencies
cd app
pip install -r requirements.txt

# Build the FAISS index
python download_data.py

# Run the API locally
python main.py
```

### Docker Development
```bash
# Build container
docker build -t parsephish ./app

# Run with GPU support (requires NVIDIA Docker)
docker run --gpus all -p 8080:8080 parsephish
```

---

## 📊 Performance

- **Cold Start**: ~10-15 seconds (model loading + index building)
- **Warm Requests**: <200ms per analysis
- **Throughput**: 100+ requests/second with auto-scaling
- **GPU Utilization**: Optimized for L4 inference

---

## 🔒 Security & Privacy

- No data persistence - content analyzed in memory only
- HTTPS-only API endpoints
- Input validation and rate limiting
- Isolated container execution

---

## 📈 Future Enhancements

- [ ] Real-time model updates from threat intelligence feeds
- [ ] Batch processing for high-volume analysis
- [ ] Integration with email security gateways
- [ ] Custom model fine-tuning capabilities

---

## 📄 License

MIT License - see [LICENSE](LICENSE) for details.

---

**Built for the Cloud Run GPU Hackathon 2024** 🏆

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
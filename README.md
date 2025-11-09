# ParsePhish API

> **GPU-powered phishing detection API on Google Cloud Run**  
> Serverless AI-powered email and message analysis for phishing detection.

ParsePhish is a REST API that uses transformer embeddings and GPU-accelerated similarity search to analyze emails, messages, and URLs for phishing indicators. Built for the **Cloud Run GPU Category** hackathon, it runs entirely serverless on **Google Cloud Run with NVIDIA L4 GPUs**.

---

## 🚀 Quick Start

### Deploy to Cloud Run
```bash
# Clone the repository
git clone https://github.com/kevinl95/ParsePhish.git
cd ParsePhish

# Deploy with GPU support to your Google Cloud project
./deploy.sh YOUR_PROJECT_ID europe-west4
```

### Using Cloud Build
```bash
# Deploy using Cloud Build (recommended for production)
gcloud builds submit --config cloudbuild.yaml
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

## How It Works

ParsePhish combines modern AI techniques with GPU acceleration for fast, accurate phishing detection:

1. **Text Processing**: Extracts and normalizes content from emails or fetched web pages
2. **GPU-Accelerated Embeddings**: Uses transformer models to convert text into semantic vectors
3. **Similarity Search**: FAISS GPU index finds the most similar known phishing/legitimate examples  
4. **Intelligent Scoring**: Combines similarity scores with explicit phrase detection
5. **Real-time Response**: Returns risk assessment in <200ms for warm requests


### Technical Flow
1. **Request**: Client sends email content or URL via REST API
2. **Processing**: Text extraction and normalization  
3. **Embedding**: SentenceTransformer converts text to 384-dim vector
4. **Search**: FAISS GPU finds 5 most similar training examples
5. **Scoring**: Combines similarity votes with phrase pattern matching
6. **Response**: Returns risk score (0-1) with explanatory details

---

## API Reference

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
Analyze website content for phishing indicators by fetching and processing the page.

**Request Body:**
```json
{
  "url": "https://example.com/suspicious-page"
}
```

**Response:**
```json
{
  "phishy_score": 0.23,
  "suspect_phrases": [],
  "verdict": "Likely legitimate"
}
```

### `GET /health`
Health check endpoint for monitoring and load balancers.

**Response:**
```json
{
  "status": "healthy",
  "service": "ParsePhish API"
}
```

### `GET /docs`
Interactive API documentation (FastAPI auto-generated Swagger UI).

## Development

### Local Development
```bash
# Install dependencies
cd app
pip install -r requirements.txt

# Build training data and FAISS index
python download_data.py

# Start the API server
python main.py
# Server runs on http://localhost:8080
# API docs at http://localhost:8080/docs
```

### Docker Development
```bash
# Build container
docker build -t parsephish .

# Run with GPU support (requires NVIDIA Docker)
docker run --gpus all -p 8080:8080 parsephish
```

### Local Testing
```bash
# Test the API endpoints
python test_api.py
```

## Security & Privacy

- **No Data Persistence**: Content analyzed in memory only, never stored
- **HTTPS-only**: All API endpoints require encrypted connections
- **Input Validation**: Comprehensive request sanitization and rate limiting  
- **Container Isolation**: Each request processed in isolated Cloud Run environment
- **GPU Security**: GPU memory cleared between inference requests

## Try It Out

Once deployed, test with these examples:

```bash
# Obvious phishing attempt
curl -X POST $SERVICE_URL/analyze/email \
  -H 'Content-Type: application/json' \
  -d '{
    "content": "URGENT! Your account has been compromised. Click this link immediately to secure your account or it will be permanently deleted within 24 hours!",
    "subject": "SECURITY ALERT - Action Required"
  }'

# Legitimate email
curl -X POST $SERVICE_URL/analyze/email \
  -H 'Content-Type: application/json' \
  -d '{
    "content": "Your monthly statement is now available in your online banking portal. Please log in to view your account activity.",
    "subject": "Monthly Statement Available"
  }'
```


## License

MIT License - see [LICENSE](LICENSE) for details.
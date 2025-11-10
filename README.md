<div align="center">
  <img src="assets/logo.png" alt="The text ParsePhish displayed underneath a shield with a fish on it." width="200">
</div>

# ParsePhish Email Analysis API

> **GPU-powered phishing detection for email content**  
> Serverless AI-powered email analysis using transformer embeddings and similarity search.

ParsePhish is a REST API that uses transformer embeddings and GPU-accelerated similarity search to analyze email content for phishing indicators. Built for the **Cloud Run GPU Category** hackathon, it runs entirely serverless on **Google Cloud Run with NVIDIA L4 GPUs**.

---

## Quick Start

### Prerequisites
Before deploying, you'll need:

1. **Google Cloud CLI**: [Install gcloud](https://cloud.google.com/sdk/docs/install)
2. **Google Cloud Project**: Create a project with billing enabled
3. **Authentication**: Run `gcloud auth login` and `gcloud auth application-default login`
4. **GPU Quota**: Request NVIDIA L4 GPU quota in europe-west4 region
5. **Required APIs**: The deployment script will enable these automatically:
   - Cloud Run API
   - Cloud Build API
   - Container Registry API

### Deploy to Cloud Run
```bash
# Clone the repository
git clone https://github.com/kevinl95/ParsePhish.git
cd ParsePhish

# Deploy with GPU support to your Google Cloud project
./deploy.sh YOUR_PROJECT_ID europe-west4
```

**Important Deployment Notes:**
- **Memory**: Requires minimum 16Gi memory for GPU instances
- **Region**: Use europe-west4 or europe-west1 for L4 GPU availability
- **Quota**: May require GPU quota approval (deployment script will prompt if needed)
- **Max Instances**: Set to 1 initially to avoid quota issues

### API Usage
```bash
# Check API health
curl https://YOUR_SERVICE_URL/health

# Analyze email content for phishing
curl -X POST https://YOUR_SERVICE_URL/analyze/email \
  -H 'Content-Type: application/json' \
  -d '{
    "content": "Urgent! Your account will be suspended. Click here to verify.",
    "subject": "Account Security Alert"
  }'
```

> **Note**: Replace `YOUR_SERVICE_URL` with your actual deployed Cloud Run service URL.

## How It Works

ParsePhish combines modern AI techniques with GPU acceleration for fast, accurate phishing detection:

1. **Text Processing**: Extracts and normalizes email content (subject + body)
2. **GPU-Accelerated Embeddings**: Uses transformer models to convert text into semantic vectors
3. **Similarity Search**: FAISS index finds the most similar known phishing/legitimate examples  
4. **Intelligent Scoring**: Combines similarity scores with explicit phrase detection
5. **Real-time Response**: Returns risk assessment in <200ms for warm requests

### Technical Flow
1. **Request**: Client sends email content via REST API
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

### Local Development Prerequisites
- **Python 3.11+**
- **CUDA 11.8+** (for GPU support)
- **NVIDIA Docker** (for containerized GPU development)

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

Once you deploy your instance, test with these examples:

```bash
# Replace $SERVICE_URL with your deployed Cloud Run service URL

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


## Troubleshooting

### Common Deployment Issues

**GPU Quota Error:**
```
You do not have quota for using GPUs with zonal redundancy
```
**Solution:** Choose "Y" when prompted to deploy without zonal redundancy, or request GPU quota increase.

**Build Failure with CUDA Base Image:**
```
manifest for nvidia/cuda:11.8-runtime-ubuntu20.04 not found
```
**Solution:** The Dockerfile now uses `python:3.11-slim` base image for Cloud Build compatibility. GPU support is provided by Cloud Run's GPU runtime, not the container image.

**Memory Error:**
```
memory must be at least 16Gi
```
**Solution:** GPU instances require minimum 16Gi memory - this is handled in the updated deploy script.

**Service Won't Start:**
- Check Cloud Run logs: `gcloud run logs read --service=parsephish-api --region=europe-west4`
- Verify GPU availability in your chosen region
- Ensure all required APIs are enabled

### Performance Optimization

- **Cold starts**: First request may take 30-60 seconds for model initialization
- **Warm requests**: Subsequent requests complete in <200ms
- **GPU utilization**: Monitor via Cloud Run metrics dashboard
- **Cost optimization**: Consider setting `--max-instances=1` for light usage

## License

MIT License - see [LICENSE](LICENSE) for details.
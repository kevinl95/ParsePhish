#!/bin/bash

# ParsePhish Cloud Run Deployment Script
# This script builds and deploys the ParsePhish API to Google Cloud Run with GPU support

set -e

# Configuration
PROJECT_ID=${1:-"your-project-id"}
REGION=${2:-"europe-west4"}  # Use europe-west4 or europe-west1 for L4 GPU support
SERVICE_NAME="parsephish-api"
IMAGE_NAME="gcr.io/$PROJECT_ID/parsephish"

echo "🚀 Deploying ParsePhish API to Cloud Run"
echo "Project: $PROJECT_ID"
echo "Region: $REGION"
echo "Service: $SERVICE_NAME"

# Check if gcloud is installed
if ! command -v gcloud &> /dev/null; then
    echo "❌ gcloud CLI not found. Please install it first."
    exit 1
fi

# Set the project
echo "📋 Setting up project..."
gcloud config set project $PROJECT_ID

# Enable required APIs
echo "🔧 Enabling required APIs..."
gcloud services enable \
    cloudbuild.googleapis.com \
    run.googleapis.com \
    containerregistry.googleapis.com

# Build the container image
echo "🏗️  Building container image..."
gcloud builds submit --tag $IMAGE_NAME .

# Deploy to Cloud Run with GPU support
echo "🚀 Deploying to Cloud Run..."
gcloud run deploy $SERVICE_NAME \
    --image $IMAGE_NAME \
    --platform managed \
    --region $REGION \
    --allow-unauthenticated \
    --memory=16Gi \
    --cpu=4 \
    --timeout=900 \
    --max-instances=1 \
    --port=8080 \
    --set-env-vars="ENVIRONMENT=production" \
    --execution-environment=gen2 \
    --gpu=1 \
    --gpu-type=nvidia-l4 \
    --no-cpu-throttling

# Get the service URL
SERVICE_URL=$(gcloud run services describe $SERVICE_NAME --platform managed --region $REGION --format 'value(status.url)')

echo "✅ Deployment complete!"
echo "🌐 Service URL: $SERVICE_URL"
echo "📖 API Documentation: $SERVICE_URL/docs"
echo "❤️  Health Check: $SERVICE_URL/health"

echo ""
echo "📝 Example API Usage:"
echo "# Check API health"
echo "curl $SERVICE_URL/health"
echo ""
echo "# Analyze email for phishing"
echo "curl -X POST $SERVICE_URL/analyze/email \\"
echo "  -H 'Content-Type: application/json' \\"
echo "  -d '{\"content\":\"Urgent! Your account will be suspended. Click here to verify.\", \"subject\":\"Account Alert\"}'"

echo ""
echo "🎉 ParsePhish Email Analysis API is now live and ready to detect phishing attempts!"
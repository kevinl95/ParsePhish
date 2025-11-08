#!/usr/bin/env python3
"""
Download phishing datasets and build FAISS index on startup
"""
import os
import json
import logging
import requests
import pandas as pd
from sentence_transformers import SentenceTransformer
import faiss
import numpy as np

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def download_phishing_dataset():
    """Download or create a phishing dataset"""
    
    # Sample phishing examples - in production, you'd download from a real dataset
    phishing_examples = [
        {"text": "Urgent: Your account has been suspended. Click here to verify your identity immediately.", "label": "phish"},
        {"text": "CONGRATULATIONS! You've won $1,000,000! Click here to claim your prize now!", "label": "phish"},
        {"text": "Your PayPal account will be limited. Update your payment information to avoid restrictions.", "label": "phish"},
        {"text": "Security Alert: Unauthorized access detected. Verify your account to secure it.", "label": "phish"},
        {"text": "Act now! Limited time offer expires today. Don't miss out on this amazing deal!", "label": "phish"},
        {"text": "Your password will expire in 24 hours. Change it now to maintain access.", "label": "phish"},
        {"text": "IRS Notice: You have a tax refund pending. Click here to claim it.", "label": "phish"},
        {"text": "Bank of America: Suspicious activity detected on your account. Verify now.", "label": "phish"},
        {"text": "Your package delivery failed. Reschedule delivery by clicking this link.", "label": "phish"},
        {"text": "Microsoft: Your Office subscription has expired. Renew now to continue access.", "label": "phish"},
        
        # Legitimate examples
        {"text": "Thank you for your purchase. Your order will be shipped within 2-3 business days.", "label": "legitimate"},
        {"text": "Your monthly statement is ready. You can view it in your online account.", "label": "legitimate"},
        {"text": "Meeting reminder: Our team meeting is scheduled for tomorrow at 2 PM.", "label": "legitimate"},
        {"text": "Welcome to our newsletter! Here are this week's top articles.", "label": "legitimate"},
        {"text": "Your appointment is confirmed for Friday, March 15th at 10:00 AM.", "label": "legitimate"},
        {"text": "System maintenance scheduled for Sunday night. Services may be temporarily unavailable.", "label": "legitimate"},
        {"text": "Your order has been confirmed. Tracking information will be sent separately.", "label": "legitimate"},
        {"text": "Conference registration successful. Please save the date: June 15-17, 2024.", "label": "legitimate"},
        {"text": "Quarterly report is now available. Please review and provide feedback by Friday.", "label": "legitimate"},
        {"text": "Password changed successfully. If this wasn't you, please contact support.", "label": "legitimate"},
    ]
    
    # Try to download a real dataset if available (optional)
    try:
        # This is a placeholder - you could download from Kaggle, HuggingFace, etc.
        logger.info("Attempting to download additional dataset...")
        # For now, we'll use our sample data
    except Exception as e:
        logger.info(f"Using sample dataset: {e}")
    
    return phishing_examples

def build_faiss_index():
    """Build FAISS index from dataset"""
    logger.info("Building FAISS index...")
    
    # Download/create dataset
    corpus = download_phishing_dataset()
    
    # Save corpus to JSON
    with open("phish_corpus.json", "w") as f:
        json.dump(corpus, f, indent=2)
    
    # Load model
    model_name = os.getenv("MODEL_NAME", "intfloat/e5-small-v2")
    logger.info(f"Loading model: {model_name}")
    model = SentenceTransformer(model_name)
    
    # Prepare data
    texts = [item["text"] for item in corpus]
    labels = [item["label"] for item in corpus]
    
    # Generate embeddings
    logger.info("Generating embeddings...")
    embeddings = model.encode(texts, show_progress_bar=True)
    
    # Create FAISS index
    dimension = embeddings.shape[1]
    logger.info(f"Creating FAISS index with dimension {dimension}")
    
    # Use GPU index if available, otherwise CPU
    try:
        # Check if GPU is available
        import torch
        if torch.cuda.is_available():
            res = faiss.StandardGpuResources()
            index_cpu = faiss.IndexFlatL2(dimension)
            index = faiss.index_cpu_to_gpu(res, 0, index_cpu)
            logger.info("Using GPU FAISS index")
        else:
            index = faiss.IndexFlatL2(dimension)
            logger.info("Using CPU FAISS index")
    except ImportError:
        index = faiss.IndexFlatL2(dimension)
        logger.info("Using CPU FAISS index")
    
    # Add embeddings to index
    index.add(embeddings.astype('float32'))
    
    # Save index and labels
    if hasattr(index, 'index'):  # GPU index
        faiss.write_index(faiss.index_gpu_to_cpu(index), "phish_index.faiss")
    else:  # CPU index
        faiss.write_index(index, "phish_index.faiss")
    
    np.save("labels.npy", np.array(labels))
    
    logger.info("✅ FAISS index built successfully!")
    return True

if __name__ == "__main__":
    try:
        build_faiss_index()
    except Exception as e:
        logger.error(f"Failed to build index: {e}")
        exit(1)
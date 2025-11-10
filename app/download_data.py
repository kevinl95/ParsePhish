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
        
        # Legitimate examples - adding more diverse, realistic content
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
        
        # Adding more legitimate examples that might be similar to what Google/major sites contain
        {"text": "Search the world's information, including webpages, images, videos and more. Google has many special features to help you find exactly what you're looking for.", "label": "legitimate"},
        {"text": "Welcome to GitHub where over 100 million developers shape the future of software, together.", "label": "legitimate"},
        {"text": "News, email and search are just the beginning. Discover more every day. Find your yodel.", "label": "legitimate"},
        {"text": "The world's largest professional network on LinkedIn. Connect with colleagues, find jobs and grow your career.", "label": "legitimate"},
        {"text": "About this page Our systems have detected unusual traffic from your computer network. This page checks to see if it's really you sending the requests.", "label": "legitimate"},
        {"text": "Privacy Policy Terms of Service Help Feedback About Google advertising business solutions", "label": "legitimate"},
        {"text": "Sign in to your account to access your personalized experience and settings across our services.", "label": "legitimate"},
        {"text": "Learn more about our products and services. Find support documentation and tutorials.", "label": "legitimate"},
        {"text": "Contact us for customer support, billing questions, or technical assistance with our services.", "label": "legitimate"},
        {"text": "Copyright notice. All rights reserved. Terms and conditions apply. See our privacy policy for more information.", "label": "legitimate"},
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
    
    # Use GPU index 
    try:
        import torch
        if torch.cuda.is_available():
            res = faiss.StandardGpuResources()
            index_cpu = faiss.IndexFlatL2(dimension)
            index = faiss.index_cpu_to_gpu(res, 0, index_cpu)
            logger.info("Using GPU FAISS index")
        else:
            index = faiss.IndexFlatL2(dimension)
            logger.info("GPU not available, using CPU FAISS index")
    except Exception as e:
        index = faiss.IndexFlatL2(dimension)
        logger.warning(f"GPU FAISS failed, using CPU: {e}")
    
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
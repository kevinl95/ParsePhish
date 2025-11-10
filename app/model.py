import os
import logging
import numpy as np
from sentence_transformers import SentenceTransformer
import faiss

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Configuration
MODEL_NAME = os.getenv("MODEL_NAME", "intfloat/e5-small-v2")
INDEX_PATH = os.getenv("INDEX_PATH", "phish_index.faiss")
LABELS_PATH = os.getenv("LABELS_PATH", "labels.npy")
VEC_DIM = 384  # for e5-small-v2

# Global variables for model and index
model = None
index = None
labels = None

def initialize_model():
    """Initialize the model and FAISS index"""
    global model, index, labels
    
    try:
        logger.info("Loading SentenceTransformer model...")
        model = SentenceTransformer(MODEL_NAME)
        
        logger.info("Loading FAISS index...")
        if os.path.exists(INDEX_PATH):
            index = faiss.read_index(INDEX_PATH)
            logger.info("FAISS index loaded successfully")
        else:
            logger.warning(f"Index file {INDEX_PATH} not found")
            
        logger.info("Loading labels...")
        if os.path.exists(LABELS_PATH):
            labels = np.load(LABELS_PATH, allow_pickle=True)
            logger.info("Labels loaded successfully")
        else:
            logger.warning(f"Labels file {LABELS_PATH} not found")
            
        logger.info("Model initialization complete")
    except Exception as e:
        logger.error(f"Failed to initialize model: {e}")
        raise

def get_suspect_phrases(text: str):
    """Extract common phishing phrases from text"""
    phishing_indicators = [
        "verify account", "urgent action", "account suspended", 
        "click here", "immediate action", "verify identity",
        "confirm account", "update payment", "security alert",
        "expire", "suspended", "locked", "unauthorized access",
        "winner", "congratulations", "prize", "claim now",
        "act now", "limited time", "offer expires"
    ]
    
    text_lower = text.lower()
    found_phrases = []
    
    for phrase in phishing_indicators:
        if phrase in text_lower:
            found_phrases.append(phrase)
    
    return found_phrases[:5]  # Return max 5 phrases

def get_phish_score_text(text: str):
    """Analyze text content for phishing indicators"""
    if model is None or index is None or labels is None:
        initialize_model()
    
    try:
        # Get embedding for the text
        embedding = model.encode([text])
        
        if index is not None and labels is not None:
            # Search for similar examples
            distances, indices = index.search(embedding.astype('float32'), k=5)
            
            # Calculate score based on similar examples
            phish_votes = sum(1 for i in indices[0] if i < len(labels) and labels[i] == "phish")
            score = phish_votes / len(indices[0])
        else:
            # Fallback scoring if index not available
            score = 0.3  # Conservative default
            
        # Get suspect phrases
        highlights = get_suspect_phrases(text)
        
        return float(score), highlights
        
    except Exception as e:
        logger.error(f"Error in text analysis: {e}")
        return 0.5, []  # Return moderate risk if analysis fails

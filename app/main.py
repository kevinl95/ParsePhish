from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from model import get_phish_score_text, initialize_model
import uvicorn
import logging
import os

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(
    title="ParsePhish Email Analysis API",
    description="GPU-accelerated phishing detection for email content using transformer embeddings and similarity search",
    version="1.0.0"
)

class EmailAnalysisRequest(BaseModel):
    content: str
    subject: str = None

class PhishingResponse(BaseModel):
    phishy_score: float
    suspect_phrases: list[str]
    verdict: str

@app.on_event("startup")
async def startup_event():
    """Initialize the model and download data if needed"""
    logger.info("Starting ParsePhish API...")
    
    # Check if we need to build the index
    if not os.path.exists("phish_index.faiss") or not os.path.exists("labels.npy"):
        logger.info("Building FAISS index...")
        try:
            from download_data import build_faiss_index
            build_faiss_index()
        except Exception as e:
            logger.error(f"Failed to build index: {e}")
            # Continue anyway - the model will handle missing index gracefully
    
    # Initialize the model
    try:
        initialize_model()
        logger.info("Model initialization complete")
    except Exception as e:
        logger.error(f"Model initialization failed: {e}")

@app.get("/health")
def health_check():
    return {"status": "healthy", "service": "ParsePhish API"}

@app.post("/analyze/email", response_model=PhishingResponse)
def analyze_email(request: EmailAnalysisRequest):
    """Analyze email content for phishing indicators"""
    try:
        full_text = f"{request.subject or ''} {request.content}".strip()
        score, highlights = get_phish_score_text(full_text)
        return PhishingResponse(
            phishy_score=score,
            suspect_phrases=highlights,
            verdict="Phishing detected" if score > 0.7 else "Likely legitimate"
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Analysis failed: {str(e)}")

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8080)

from fastapi import FastAPI, Query
from model import get_phish_score
import uvicorn

app = FastAPI(title="ParsePhish", description="AI-powered phishing detector")

@app.get("/")
def root():
    return {"message": "Welcome to ParsePhish 🐟"}

@app.get("/analyze")
def analyze_url(url: str = Query(..., description="URL to analyze")):
    score, highlights = get_phish_score(url)
    return {
        "url": url,
        "phishy_score": score,
        "suspect_phrases": highlights,
        "verdict": "Phishy 🧅" if score > 0.7 else "Likely safe 🧊",
    }

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8080)

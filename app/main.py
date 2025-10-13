from fastapi import FastAPI, Query
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from model import get_phish_score
import os
import uvicorn

app = FastAPI(title="ParsePhish", description="AI-powered phishing detector")
app.mount("/static", StaticFiles(directory="static"), name="static")

@app.get("/", include_in_schema=False)
def index():
    return FileResponse(os.path.join("static", "index.html"))

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

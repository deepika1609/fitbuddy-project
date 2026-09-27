import os
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from dotenv import load_dotenv

from app.database import init_db
from app.routes import router

# Load environment variables
load_dotenv()

# Create FastAPI instance
app = FastAPI(
    title="FitBuddy - AI Fitness Plan Generator",
    description="Web application leveraging Google Gemini AI models to generate personalized workout plans, nutrition tips, and feedback-based adjustments.",
    version="1.0.0"
)

# Initialize Database tables
init_db()

# Define paths
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
STATIC_DIR = os.path.join(BASE_DIR, "static")

# Mount static files (CSS, images, JS)
if os.path.exists(STATIC_DIR):
    app.mount("/static", StaticFiles(directory=STATIC_DIR), name="static")

# Include Application Router
app.include_router(router)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app.main:app", host="127.0.0.1", port=8000, reload=True)

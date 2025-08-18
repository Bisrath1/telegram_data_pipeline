from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api import crud  # example: if you create routers later
import logging

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)

# Initialize FastAPI app
app = FastAPI(
    title="Telegram Data Pipeline API",
    description="API for analyzing Telegram messages and channels",
    version="1.0.0"
)

# CORS Middleware (useful if you connect from frontend dashboards)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # tighten in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/", tags=["Health Check"])
def read_root():
    """
    Root endpoint to check if the API is running.
    """
    logger.info("Health check called")
    return {"message": "🚀 FastAPI is running inside Docker!"}

# Example structure: later you can include routers
# app.include_router(crud.router, prefix="/api", tags=["Data Analysis"])

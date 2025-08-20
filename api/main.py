from fastapi import FastAPI, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List
import logging
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded
from . import crud, schemas, database

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Initialize FastAPI app
app = FastAPI(
    title="Medical Insights API",
    description="API for analyzing Telegram data on Ethiopian medical businesses",
    version="1.0.0"
)

# Initialize rate limiter
limiter = Limiter(key_func=get_remote_address)
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

def get_db():
    """Dependency to get a database session."""
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get(
    "/api/reports/top-products",
    response_model=List[schemas.ProductFrequency],
    summary="Get top mentioned medical products",
    description="Retrieve the most frequently mentioned medical products across Telegram channels."
)
@limiter.limit("10/minute")
async def top_products(
    limit: int = Query(10, ge=1, le=50, description="Number of products to return (1-50)"),
    db: Session = Depends(get_db)
):
    """Get the top mentioned products with a specified limit."""
    try:
        products = crud.get_top_products(db, limit)
        if not products:
            logger.warning("No products found for top-products endpoint")
            raise HTTPException(status_code=404, detail="No products found")
        logger.info(f"Retrieved {len(products)} top products")
        return products
    except Exception as e:
        logger.error(f"Error retrieving top products: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal server error")

@app.get(
    "/api/channels/{channel_name}/activity",
    response_model=schemas.ChannelActivity,
    summary="Get channel activity metrics",
    description="Retrieve posting activity metrics for a specific Telegram channel."
)
@limiter.limit("5/minute")
async def channel_activity(
    channel_name: str = Query(..., min_length=3, description="Name of the Telegram channel"),
    db: Session = Depends(get_db)
):
    """Get activity metrics for a specific channel."""
    try:
        activity = crud.get_channel_activity(db, channel_name)
        if not activity:
            logger.warning(f"No activity found for channel: {channel_name}")
            raise HTTPException(status_code=404, detail=f"Channel {channel_name} not found")
        logger.info(f"Retrieved activity for channel: {channel_name}")
        return activity
    except Exception as e:
        logger.error(f"Error retrieving channel activity for {channel_name}: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal server error")

@app.get(
    "/api/search/messages",
    response_model=List[schemas.MessageSearchResult],
    summary="Search messages by keyword",
    description="Search for messages containing a specific keyword across all Telegram channels."
)
@limiter.limit("15/minute")
async def search_messages(
    query: str = Query(..., min_length=3, max_length=100, description="Search keyword"),
    db: Session = Depends(get_db)
):
    """Search messages containing a specific keyword."""
    try:
        results = crud.search_messages(db, query)
        logger.info(f"Found {len(results)} messages for query: {query}")
        return results
    except Exception as e:
        logger.error(f"Error searching messages for query {query}: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal server error")
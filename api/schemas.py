from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional


class WordCount(BaseModel):
    """Represents the frequency of a word or product mention."""
    word: str = Field(..., description="The word/product being counted")
    count: int = Field(..., description="Number of times the word/product appears")


class ChannelActivity(BaseModel):
    """Summarizes the activity of a specific Telegram channel."""
    channel_name: str = Field(..., description="Name of the Telegram channel")
    total_messages: int = Field(..., description="Total number of messages in the channel")
    with_images: int = Field(..., description="Number of messages that include images")


class MessageSearchResult(BaseModel):
    """Represents a message returned in a keyword search."""
    message_id: int = Field(..., description="Unique ID of the message")
    message_text: str = Field(..., description="Text content of the message")
    channel_name: str = Field(..., description="Channel where the message was posted")
    message_date: datetime = Field(..., description="Date and time when the message was posted")

    class Config:
        orm_mode = True  # allow returning SQLAlchemy models directly


# Example of an extended schema for finance context (future use)
class RiskScoredMessage(MessageSearchResult):
    """Message with an additional risk score assigned for financial monitoring."""
    risk_score: Optional[float] = Field(None, description="Risk score between 0 and 1 indicating financial risk")

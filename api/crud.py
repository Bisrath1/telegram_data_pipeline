# api/crud.py

from sqlalchemy.orm import Session
from sqlalchemy import func
from fastapi import HTTPException
from typing import List, Optional
from datetime import datetime

from . import models, schemas  # assuming you have ORM + Pydantic schemas


def get_top_products(db: Session, limit: int = 10) -> List[schemas.WordCount]:
    """
    Returns the most frequently used words across all messages.
    """
    results = (
        db.query(
            func.lower(func.unnest(func.string_to_array(models.Message.message_text, ' '))).label("word"),
            func.count().label("count")
        )
        .group_by("word")
        .order_by(func.count().desc())
        .limit(limit)
        .all()
    )

    return [schemas.WordCount(word=r.word, count=r.count) for r in results]


def get_channel_activity(db: Session, channel_name: str) -> schemas.ChannelActivity:
    """
    Returns message activity summary for a given channel.
    """
    result = (
        db.query(
            models.Message.channel_name.label("channel_name"),
            func.count().label("total_messages"),
            func.sum(func.case([(models.Message.has_image == True, 1)], else_=0)).label("with_images")
        )
        .filter(models.Message.channel_name == channel_name)
        .group_by(models.Message.channel_name)
        .first()
    )

    if not result:
        raise HTTPException(status_code=404, detail=f"Channel '{channel_name}' not found")

    return schemas.ChannelActivity(
        channel_name=result.channel_name,
        total_messages=result.total_messages,
        with_images=result.with_images
    )


def search_messages(db: Session, keyword: str, limit: int = 20) -> List[schemas.MessageOut]:
    """
    Searches messages containing a keyword (case-insensitive).
    """
    results = (
        db.query(
            models.Message.message_id,
            models.Message.message_text,
            models.Message.channel_name,
            models.Message.message_date,
        )
        .filter(func.lower(models.Message.message_text).like(f"%{keyword.lower()}%"))
        .limit(limit)
        .all()
    )

    return [
        schemas.MessageOut(
            message_id=r.message_id,
            message_text=r.message_text,
            channel_name=r.channel_name,
            message_date=r.message_date
        )
        for r in results
    ]

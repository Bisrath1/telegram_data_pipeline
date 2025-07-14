from sqlalchemy.orm import Session
from fastapi import HTTPException

def get_top_products(db: Session, limit: int = 10):
    query = """
        SELECT LOWER(unnest(string_to_array(message_text, ' '))) AS word, COUNT(*) as count
        FROM fct_messages
        GROUP BY word
        ORDER BY count DESC
        LIMIT :limit
    """
    return db.execute(query, {"limit": limit}).fetchall()

def get_channel_activity(db: Session, channel_name: str):
    query = """
        SELECT channel_name,
               COUNT(*) AS total_messages,
               SUM(CASE WHEN has_image THEN 1 ELSE 0 END) AS with_images
        FROM fct_messages
        WHERE channel_name = :channel_name
        GROUP BY channel_name
    """
    result = db.execute(query, {"channel_name": channel_name}).fetchone()
    if not result:
        raise HTTPException(status_code=404, detail="Channel not found")
    return result

def search_messages(db: Session, keyword: str):
    query = """
        SELECT message_id, message_text, channel_name, message_date
        FROM fct_messages
        WHERE LOWER(message_text) LIKE :kw
        LIMIT 20
    """
    return db.execute(query, {"kw": f"%{keyword.lower()}%"}).fetchall()

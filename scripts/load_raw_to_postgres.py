import os
import json
import psycopg2
from psycopg2.extras import Json
from dotenv import load_dotenv
from pathlib import Path
from datetime import datetime

# Load environment variables from .env
load_dotenv()

# DB Connection Setup
conn = psycopg2.connect(
    host=os.getenv("DB_HOST"),
    port=os.getenv("DB_PORT"),
    dbname=os.getenv("DB_NAME"),
    user=os.getenv("DB_USER"),
    password=os.getenv("DB_PASSWORD")
)
cursor = conn.cursor()

# Define path to raw data
DATA_DIR = Path("data/raw/telegram_messages")



def parse_message(msg, channel_name):
    return {
        "message_id": msg.get("id"),
        "channel_name": channel_name,
        "message_text": msg.get("message", ""),
        "message_date": msg.get("date", datetime.utcnow()),
        "has_image": bool(msg.get("media")),
        "image_path": msg.get("media", {}).get("file_path") if msg.get("media") else None,
        "raw_json": msg
    }

def insert_message(msg):
    sql = """
    INSERT INTO raw.telegram_messages (
        message_id, channel_name, message_text, message_date,
        has_image, image_path, raw_json
    )
    VALUES (%s, %s, %s, %s, %s, %s, %s)
    ON CONFLICT (message_id) DO NOTHING;
    """
    values = (
        msg["message_id"],
        msg["channel_name"],
        msg["message_text"],
        msg["message_date"],
        msg["has_image"],
        msg["image_path"],
        Json(msg["raw_json"])
    )
    cursor.execute(sql, values)

def process_channel_file(json_file_path):
    channel_name = json_file_path.stem
    print(f"Processing: {channel_name}")

    with open(json_file_path, "r", encoding="utf-8") as f:
        messages = json.load(f)

    for msg in messages:
        parsed = parse_message(msg, channel_name)
        insert_message(parsed)

    conn.commit()
    print(f"✔ Done: {channel_name}")

def main():
    for day_folder in DATA_DIR.iterdir():
        if day_folder.is_dir():
            for json_file in day_folder.glob("*.json"):
                process_channel_file(json_file)

    cursor.close()
    conn.close()

if __name__ == "__main__":
    main()

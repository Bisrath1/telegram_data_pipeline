# scripts/load_raw_to_postgres.py

import os
import json
import logging
from pathlib import Path
from datetime import datetime
from dotenv import load_dotenv
import psycopg2
from psycopg2.extras import Json

# -------------------------------
# Setup logging
# -------------------------------
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s"
)

# -------------------------------
# Load environment variables
# -------------------------------
load_dotenv()

DB_CONFIG = {
    "host": os.getenv("DB_HOST"),
    "port": os.getenv("DB_PORT"),
    "dbname": os.getenv("DB_NAME"),
    "user": os.getenv("DB_USER"),
    "password": os.getenv("DB_PASSWORD"),
}

# Fail early if DB config missing
if not all(DB_CONFIG.values()):
    raise ValueError("❌ Missing one or more required DB environment variables!")

# -------------------------------
# Constants
# -------------------------------
DATA_DIR = Path("data/raw/telegram_messages")


# -------------------------------
# Helpers
# -------------------------------
def parse_message(msg: dict, channel_name: str) -> dict:
    """Parse Telegram JSON message into structured dict."""
    try:
        message_date = msg.get("date")
        if isinstance(message_date, str):
            try:
                message_date = datetime.fromisoformat(message_date)
            except Exception:
                message_date = datetime.utcnow()

        return {
            "message_id": msg.get("id"),
            "channel_name": channel_name,
            "message_text": msg.get("message", ""),
            "message_date": message_date or datetime.utcnow(),
            "has_image": bool(msg.get("media")),
            "image_path": msg.get("media", {}).get("file_path") if msg.get("media") else None,
            "raw_json": msg
        }
    except Exception as e:
        logging.error(f"❌ Error parsing message: {e}")
        return None


def insert_messages(conn, messages: list):
    """Insert multiple messages into DB in a batch."""
    sql = """
    INSERT INTO raw.telegram_messages (
        message_id, channel_name, message_text, message_date,
        has_image, image_path, raw_json
    )
    VALUES (%s, %s, %s, %s, %s, %s, %s)
    ON CONFLICT (message_id) DO NOTHING;
    """
    values = [
        (
            msg["message_id"],
            msg["channel_name"],
            msg["message_text"],
            msg["message_date"],
            msg["has_image"],
            msg["image_path"],
            Json(msg["raw_json"])
        )
        for msg in messages if msg is not None
    ]

    with conn.cursor() as cursor:
        cursor.executemany(sql, values)


def process_channel_file(conn, json_file_path: Path):
    """Process a single channel JSON file."""
    channel_name = json_file_path.stem
    logging.info(f"📂 Processing channel: {channel_name}")

    try:
        with open(json_file_path, "r", encoding="utf-8") as f:
            messages = json.load(f)
    except Exception as e:
        logging.error(f"❌ Failed to load {json_file_path}: {e}")
        return

    parsed_messages = [parse_message(msg, channel_name) for msg in messages]

    try:
        insert_messages(conn, parsed_messages)
        conn.commit()
        logging.info(f"✔ Done: {channel_name} ({len(parsed_messages)} messages)")
    except Exception as e:
        conn.rollback()
        logging.error(f"❌ DB insert failed for {channel_name}: {e}")


# -------------------------------
# Main
# -------------------------------
def main():
    if not DATA_DIR.exists():
        logging.error(f"❌ Data directory not found: {DATA_DIR}")
        return

    with psycopg2.connect(**DB_CONFIG) as conn:
        for day_folder in DATA_DIR.iterdir():
            if day_folder.is_dir():
                for json_file in day_folder.glob("*.json"):
                    process_channel_file(conn, json_file)

    logging.info("✅ All channels processed successfully!")


if __name__ == "__main__":
    main()

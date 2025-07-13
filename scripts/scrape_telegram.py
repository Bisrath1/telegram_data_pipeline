# scrape_telegram.py
import os
import json
from telethon.sync import TelegramClient
from telethon.tl.functions.messages import GetHistoryRequest
from dotenv import load_dotenv
from datetime import datetime
from pathlib import Path

load_dotenv()
api_id = int(os.getenv("API_ID"))
api_hash = os.getenv("API_HASH")
session_name = os.getenv("SESSION_NAME", "session")

client = TelegramClient(session_name, api_id, api_hash)

CHANNELS = [
    "https://t.me/lobelia4cosmetics",
    "https://t.me/tikvahpharma",
]

RAW_DIR = "data/raw"

async def scrape_channel(channel_url):
    await client.start()
    entity = await client.get_entity(channel_url)
    messages = []

    history = await client(GetHistoryRequest(
        peer=entity,
        limit=100,
        offset_date=None,
        offset_id=0,
        max_id=0,
        min_id=0,
        add_offset=0,
        hash=0
    ))

    for msg in history.messages:
        msg_data = msg.to_dict()
        messages.append(msg_data)

    # Format directory: data/raw/YYYY-MM-DD/channel_name.json
    channel_name = entity.username or str(entity.id)
    today = datetime.utcnow().strftime('%Y-%m-%d')
    out_dir = Path(RAW_DIR) / today
    out_dir.mkdir(parents=True, exist_ok=True)
    out_file = out_dir / f"{channel_name}.json"

    # Custom JSON encoder to handle datetime objects
    class DateTimeEncoder(json.JSONEncoder):
        def default(self, obj):
            if isinstance(obj, datetime):
                return obj.isoformat()
            return super().default(obj)

    # Save with the custom encoder
    with open(out_file, "w", encoding="utf-8") as f:
        json.dump(messages, f, ensure_ascii=False, indent=2, cls=DateTimeEncoder)

    print(f"✅ Scraped {len(messages)} messages from {channel_name}")

    
async def run_all():
    for channel in CHANNELS:
        try:
            await scrape_channel(channel)
        except Exception as e:
            print(f"❌ Failed to scrape {channel}: {e}")

if __name__ == "__main__":
    import asyncio
    asyncio.run(run_all())

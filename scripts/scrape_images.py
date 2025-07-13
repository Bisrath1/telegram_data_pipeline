import os
import asyncio
import aiofiles
from pathlib import Path
from datetime import datetime
from telethon.sync import TelegramClient
from telethon.tl.types import MessageMediaPhoto, MessageMediaDocument
from dotenv import load_dotenv

load_dotenv()

api_id = int(os.getenv("API_ID"))
api_hash = os.getenv("API_HASH")
session_name = os.getenv("SESSION_NAME", "session")

# Channels to scrape from
CHANNELS = [
    "https://t.me/lobelia4cosmetics",
    "https://t.me/tikvahpharma",
]

BASE_DIR = Path("data/raw/images")
LOG_FILE = Path("logs/image_scrape.log")

client = TelegramClient(session_name, api_id, api_hash)

async def download_images(channel):
    await client.start()
    entity = await client.get_entity(channel)
    channel_name = entity.username or str(entity.id)
    today = datetime.utcnow().strftime("%Y-%m-%d")
    out_dir = BASE_DIR / today / channel_name
    out_dir.mkdir(parents=True, exist_ok=True)

    messages = await client.get_messages(entity, limit=100)  # customize limit

    count = 0
    for i, message in enumerate(messages):
        if message.photo or (message.media and isinstance(message.media, MessageMediaDocument)):
            try:
                filename = f"image_{i}.jpg"
                file_path = out_dir / filename
                await message.download_media(file_path)
                count += 1
            except Exception as e:
                await log_error(f"[ERROR] Failed to download image: {e}")
    
    await log_success(f"[SUCCESS] Downloaded {count} images from {channel_name}")

async def log_success(message):
    async with aiofiles.open(LOG_FILE, mode='a') as f:
        await f.write(f"{datetime.now()} {message}\n")

async def log_error(message):
    async with aiofiles.open(LOG_FILE, mode='a') as f:
        await f.write(f"{datetime.now()} {message}\n")

async def run():
    for channel in CHANNELS:
        try:
            await download_images(channel)
        except Exception as e:
            await log_error(f"[ERROR] Failed to scrape {channel}: {e}")

if __name__ == "__main__":
    asyncio.run(run())

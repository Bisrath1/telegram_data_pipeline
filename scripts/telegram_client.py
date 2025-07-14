# telegram_client.py
from telethon.sync import TelegramClient
from dotenv import load_dotenv
import os

load_dotenv()

api_id = int(os.getenv("API_ID"))
api_hash = os.getenv("API_HASH")
session_name = os.getenv("SESSION_NAME", "session")

client = TelegramClient(session_name, api_id, api_hash)

async def test_connection():
    await client.start()
    me = await client.get_me()
    print(f"Logged in as: {me.username}")

if __name__ == "__main__":
    import asyncio
    asyncio.run(test_connection())

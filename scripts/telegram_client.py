# telegram_client.py
import os
import logging
from telethon import TelegramClient
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

# Load and validate required environment variables
try:
    API_ID = int(os.getenv("API_ID", "").strip())
    API_HASH = os.getenv("API_HASH", "").strip()
    SESSION_NAME = os.getenv("SESSION_NAME", "session").strip()

    if not API_ID or not API_HASH:
        raise ValueError("Missing required environment variables: API_ID or API_HASH")

except Exception as e:
    logging.error(f"Environment variable error: {e}")
    raise

# Initialize Telegram client
client: TelegramClient = TelegramClient(SESSION_NAME, API_ID, API_HASH)

async def test_connection() -> None:
    """
    Test Telegram client connection and print user info.
    """
    try:
        await client.start()
        me = await client.get_me()
        logging.info(f"✅ Logged in successfully as: {me.username or me.id}")
    except Exception as e:
        logging.error(f"❌ Failed to connect: {e}")
    finally:
        await client.disconnect()


if __name__ == "__main__":
    import asyncio
    asyncio.run(test_connection())

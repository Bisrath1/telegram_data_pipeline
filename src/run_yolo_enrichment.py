# run_yolo_enrichment.py
import os
import glob
import logging
from dotenv import load_dotenv
from ultralytics import YOLO
import psycopg2
from psycopg2.extras import execute_batch

# -------------------------------------------------------
# Setup Logging
# -------------------------------------------------------
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s"
)

# -------------------------------------------------------
# Load Environment Variables
# -------------------------------------------------------
load_dotenv()

DB_HOST = os.getenv("DB_HOST")
DB_PORT = os.getenv("DB_PORT", "5432")
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_NAME = os.getenv("DB_NAME")

if not all([DB_HOST, DB_PORT, DB_USER, DB_PASSWORD, DB_NAME]):
    raise ValueError("❌ Database environment variables are missing!")

# -------------------------------------------------------
# Load YOLO Model
# -------------------------------------------------------
try:
    model = YOLO("yolov8n.pt")  # Use yolov8s/8m for higher accuracy
    logging.info("✅ YOLO model loaded successfully.")
except Exception as e:
    logging.error(f"❌ Failed to load YOLO model: {e}")
    raise

# -------------------------------------------------------
# PostgreSQL Connection
# -------------------------------------------------------
try:
    conn = psycopg2.connect(
        host=DB_HOST,
        port=DB_PORT,
        user=DB_USER,
        password=DB_PASSWORD,
        database=DB_NAME
    )
    cur = conn.cursor()
    logging.info("✅ Connected to PostgreSQL database.")
except Exception as e:
    logging.error(f"❌ Database connection failed: {e}")
    raise

# -------------------------------------------------------
# Helper: Extract message_id from image path
# -------------------------------------------------------
def extract_message_id(image_path: str) -> int:
    """Extracts message_id assuming filename format '<id>_image.jpg'."""
    try:
        return int(os.path.basename(image_path).split("_")[0])
    except Exception as e:
        logging.warning(f"⚠️ Could not extract message_id from {image_path}: {e}")
        return None

# -------------------------------------------------------
# Process Images and Insert Detections
# -------------------------------------------------------
image_paths = glob.glob("data/raw/**/*.jpg", recursive=True)
if not image_paths:
    logging.warning("⚠️ No images found in data/raw/ directory.")

insert_data = []

for image_path in image_paths:
    message_id = extract_message_id(image_path)
    if message_id is None:
        continue

    try:
        results = model(image_path, verbose=False)

        for r in results:
            for box in r.boxes:
                cls = r.names[int(box.cls)]
                conf = float(box.conf)
                insert_data.append((message_id, cls, conf))

    except Exception as e:
        logging.error(f"❌ Error processing {image_path}: {e}")

# Batch insert into database
if insert_data:
    try:
        execute_batch(
            cur,
            """
            INSERT INTO fct_image_detections (message_id, detected_object_class, confidence_score)
            VALUES (%s, %s, %s)
            """,
            insert_data,
            page_size=100
        )
        conn.commit()
        logging.info(f"✅ Inserted {len(insert_data)} detections into fct_image_detections.")
    except Exception as e:
        logging.error(f"❌ Failed to insert detections: {e}")
        conn.rollback()
else:
    logging.info("ℹ️ No detections to insert.")

# -------------------------------------------------------
# Cleanup
# -------------------------------------------------------
cur.close()
conn.close()
logging.info("✅ Database connection closed.")

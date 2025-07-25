# run_yolo_enrichment.py
import os
import json
import glob
from ultralytics import YOLO
import psycopg2
from dotenv import load_dotenv

load_dotenv()

# Load model
model = YOLO("yolov8n.pt")  # Or yolov8m.pt / yolov8s.pt for more accuracy

# PostgreSQL connection
conn = psycopg2.connect(
    host=os.getenv("DB_HOST"),
    port=os.getenv("DB_PORT"),
    user=os.getenv("DB_USER"),
    password=os.getenv("DB_PASSWORD"),
    database=os.getenv("DB_NAME")
)
cur = conn.cursor()

# Helper to extract message_id from image filename or metadata
def extract_message_id(image_path):
    # Implement based on how you saved it
    return int(os.path.basename(image_path).split("_")[0])  # Example: 172276_image.jpg

# Loop over images
image_paths = glob.glob("data/raw/**/*.jpg", recursive=True)

for image_path in image_paths:
    results = model(image_path)
    message_id = extract_message_id(image_path)

    for r in results:
        for box in r.boxes:
            cls = r.names[int(box.cls)]
            conf = float(box.conf)
            cur.execute(
                "INSERT INTO fct_image_detections (message_id, detected_object_class, confidence_score) VALUES (%s, %s, %s)",
                (message_id, cls, conf)
            )

conn.commit()
cur.close()
conn.close()
print("✅ YOLO image detections stored in fct_image_detections table.")

# scripts/yolo_detect.py

import os
import json
import psycopg2
from dotenv import load_dotenv
from pathlib import Path
from ultralytics import YOLO
from PIL import Image

load_dotenv()

DATA_DIR = Path("data/raw")
MODEL = YOLO("yolov8n.pt")  # or yolov8s.pt

conn = psycopg2.connect(
    dbname=os.getenv("POSTGRES_DB"),
    user=os.getenv("POSTGRES_USER"),
    password=os.getenv("POSTGRES_PASSWORD"),
    host=os.getenv("POSTGRES_HOST"),
    port=os.getenv("POSTGRES_PORT"),
)
cursor = conn.cursor()

def detect_objects(image_path):
    results = MODEL(image_path)
    detections = []
    for r in results:
        for box in r.boxes:
            class_id = int(box.cls[0])
            conf = float(box.conf[0])
            label = MODEL.names[class_id]
            detections.append({
                "class": label,
                "confidence": conf,
            })
    return detections

def main():
    cursor.execute("SELECT message_id, image_path FROM raw.telegram_messages WHERE has_image = TRUE;")
    rows = cursor.fetchall()

    for message_id, image_path in rows:
        if not os.path.exists(image_path):
            print(f"Image not found: {image_path}")
            continue

        detections = detect_objects(image_path)
        for det in detections:
            cursor.execute("""
                INSERT INTO raw.image_detections (message_id, detected_class, confidence)
                VALUES (%s, %s, %s)
                ON CONFLICT DO NOTHING
            """, (message_id, det["class"], det["confidence"]))

    conn.commit()
    cursor.close()
    conn.close()

if __name__ == "__main__":
    main()

from dagster import op
import subprocess
import os

@op
def yolo_detect_op():
    """
    Runs YOLOv8 detection on new images and stores the results in the image_detections table.
    """
    script_path = os.path.abspath("scripts/yolo_detect.py")
    result = subprocess.run(["python", script_path], capture_output=True, text=True)

    if result.returncode != 0:
        raise Exception(f"YOLO detection failed:\n{result.stderr}")
    else:
        print(f"YOLO Detection Output:\n{result.stdout}")

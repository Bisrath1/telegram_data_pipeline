from dagster import op

@op
def run_yolo_detection():
    print("Running YOLO image detection...")
    # call your yolo_detect.py logic here

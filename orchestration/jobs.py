from dagster import job
from ops.load_raw import load_raw_data
from ops.yolo_detect import run_yolo_detection
from ops.build_dbt_models import run_dbt_models

@job
def full_pipeline():
    raw = load_raw_data()
    detection = run_yolo_detection()
    dbt_run = run_dbt_models()

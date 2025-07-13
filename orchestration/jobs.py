from dagster import job
from orchestration.ops.load_raw import load_raw_to_postgres_op
from orchestration.ops.yolo_detect import yolo_detect_op
from orchestration.ops.build_dbt_models import run_dbt_models_op

@job
def telegram_pipeline():
    load_raw_to_postgres_op()
    run_dbt_models_op()
    yolo_detect_op()

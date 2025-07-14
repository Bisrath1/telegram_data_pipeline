from dagster import repository
from jobs import full_pipeline

@repository
def telegram_data_repo():
    return [full_pipeline]

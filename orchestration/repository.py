from dagster import repository
from orchestration.jobs import telegram_pipeline

@repository
def telegram_repository():
    return [telegram_pipeline]

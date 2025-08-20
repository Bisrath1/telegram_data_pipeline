from dagster import job, JobDefinition, op, In, Out, Nothing
from orchestration.ops.load_raw import load_raw_to_postgres_op
from orchestration.ops.yolo_detect import yolo_detect_op
from orchestration.ops.build_dbt_models import run_dbt_models_op
import logging

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Define resources for database and file system access
from dagster import resource, Field, String

@resource(
    config_schema={
        "data_lake_path": Field(String, description="Path to the data lake"),
        "db_connection": Field(String, description="Database connection string"),
    }
)
def pipeline_resources(context):
    """Resource for managing pipeline dependencies like data lake path and database connection."""
    return {
        "data_lake_path": context.resource_config["data_lake_path"],
        "db_connection": context.resource_config["db_connection"],
    }

@job(
    resource_defs={"pipeline_resources": pipeline_resources},
    config={
        "resources": {
            "pipeline_resources": {
                "config": {
                    "data_lake_path": "data/raw",
                    "db_connection": "postgresql://user:password@localhost:5432/telegram_db",
                }
            }
        }
    },
    description="End-to-end Telegram data pipeline for medical business insights."
)
def telegram_pipeline() -> None:
    """
    Defines the Telegram data pipeline with explicit dependencies and logging.
    The pipeline:
    1. Loads raw Telegram data into PostgreSQL.
    2. Runs DBT models to transform data into a star schema.
    3. Performs YOLO object detection to enrich image data.
    """
    logger.info("Starting Telegram data pipeline execution")
    
    # Define operation dependencies
    raw_data = load_raw_to_postgres_op()
    dbt_results = run_dbt_models_op(raw_data)
    yolo_results = yolo_detect_op(dbt_results)
    
    logger.info("Telegram data pipeline completed successfully")
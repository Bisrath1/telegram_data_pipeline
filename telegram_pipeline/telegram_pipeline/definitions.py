import logging
from dagster import Definitions, load_assets_from_modules, AssetGroup, resource, Field, String
from telegram_pipeline import assets
from orchestration.jobs import telegram_pipeline as telegram_pipeline_job

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Define resources for pipeline dependencies
@resource(
    config_schema={
        "data_lake_path": Field(String, description="Path to the raw data lake"),
        "db_connection": Field(String, description="PostgreSQL connection string"),
        "dbt_project_dir": Field(String, description="Path to DBT project directory", default_value="dbt_project"),
    }
)
def pipeline_resources(context):
    """Resource for managing pipeline dependencies like data lake, database, and DBT project."""
    return {
        "data_lake_path": context.resource_config["data_lake_path"],
        "db_connection": context.resource_config["db_connection"],
        "dbt_project_dir": context.resource_config["dbt_project_dir"],
    }

# Load assets and validate
try:
    all_assets = load_assets_from_modules(
        modules=[assets],
        group_name="telegram_pipeline_assets"
    )
    logger.info(f"Successfully loaded {len(all_assets)} assets from telegram_pipeline.assets")
except Exception as e:
    logger.error(f"Failed to load assets: {str(e)}")
    raise

# Define Dagster Definitions
defs = Definitions(
    assets=all_assets,
    jobs=[telegram_pipeline_job],
    resources={
        "pipeline_resources": pipeline_resources.configured({
            "data_lake_path": "data/raw",
            "db_connection": "postgresql://user:password@localhost:5432/telegram_db",
            "dbt_project_dir": "dbt_project"
        })
    },
    description="Definitions for the Telegram data pipeline, including assets, jobs, and resources for medical business insights."
)

logger.info("Dagster Definitions initialized successfully")
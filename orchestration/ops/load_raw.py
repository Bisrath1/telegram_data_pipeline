import subprocess
import os
import logging
from dagster import op, OpExecutionContext, Out, Nothing, Field, String, Failure

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

@op(
    config_schema={
        "script_path": Field(
            String,
            default_value="scripts/load_raw_to_postgres.py",
            description="Path to the Python script for loading raw data to PostgreSQL"
        ),
    },
    out=Out(Nothing, description="Indicates successful loading of raw data to PostgreSQL"),
    required_resource_keys={"pipeline_resources"},
)
def load_raw_to_postgres_op(context: OpExecutionContext) -> None:
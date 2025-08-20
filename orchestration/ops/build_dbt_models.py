import subprocess
import os
import logging
from dagster import op, OpExecutionContext, In, Out, Field, String, Failure

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

@op(
    config_schema={
        "dbt_command": Field(
            String,
            default_value="run",
            description="DBT command to execute (e.g., 'run', 'test', 'compile')"
        ),
    },
    ins={"upstream": In(Nothing, description="Trigger from upstream operation")},
    out=Out(Nothing, description="Indicates successful DBT execution"),
    required_resource_keys={"pipeline_resources"},
)
def run_dbt_models_op(context: OpExecutionContext) -> None:
    """
    Executes a DBT command to transform data in the PostgreSQL warehouse.

    Args:
        context: Dagster execution context, providing access to resources and configuration.

    Raises:
        Failure: If the DBT command fails, with detailed error output.

    This operation:
    1. Changes to the DBT project directory specified in resources.
    2. Executes the configured DBT command (e.g., 'dbt run').
    3. Logs the execution status and output for observability.
    """
    dbt_project_dir = context.resources.pipeline_resources["dbt_project_dir"]
    dbt_command = context.op_config["dbt_command"]

    logger.info(f"Starting DBT {dbt_command} in directory: {dbt_project_dir}")

    try:
        # Change to DBT project directory
        os.chdir(dbt_project_dir)
        # Run DBT command with error capture
        result = subprocess.run(
            ["dbt", dbt_command],
            capture_output=True,
            text=True,
            check=True  # Raises CalledProcessError on non-zero exit code
        )
        logger.info(f"DBT {dbt_command} completed successfully. Output:\n{result.stdout}")
        context.log.info(f"DBT {dbt_command} completed successfully")

    except subprocess.CalledProcessError as e:
        error_msg = f"DBT {dbt_command} failed with exit code {e.returncode}:\n{e.stderr}"
        logger.error(error_msg)
        raise Failure(description=error_msg)
    except FileNotFoundError:
        error_msg = f"DBT project directory not found: {dbt_project_dir}"
        logger.error(error_msg)
        raise Failure(description=error_msg)
    except Exception as e:
        error_msg = f"Unexpected error during DBT {dbt_command}: {str(e)}"
        logger.error(error_msg)
        raise Failure(description=error_msg)
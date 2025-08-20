import subprocess
import os
import logging
from dagster import op, OpExecutionContext, In, Out, Nothing, Field, String, Failure

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

@op(
    config_schema={
        "script_path": Field(
            String,
            default_value="scripts/yolo_detect.py",
            description="Path to the Python script for YOLOv8 object detection"
        ),
        "model_path": Field(
            String,
            default_value="yolov8n.pt",
            description="Path to the YOLOv8 model file"
        ),
    },
    ins={"upstream": In(Nothing, description="Trigger from upstream DBT operation")},
    out=Out(Nothing, description="Indicates successful YOLOv8 detection and storage in PostgreSQL"),
    required_resource_keys={"pipeline_resources"},
)
def yolo_detect_op(context: OpExecutionContext) -> None:
    """
    Executes a Python script to run YOLOv8 object detection on new images and stores results in the PostgreSQL 'image_detections' table.

    Args:
        context: Dagster execution context, providing access to resources and configuration.

    Raises:
        Failure: If the script execution fails, the script/model file is not found, or an unexpected error occurs.

    This operation:
    1. Retrieves the script path, model path, and data lake details from pipeline resources.
    2. Executes the YOLOv8 detection script to process images and store results in the database.
    3. Logs execution status and output for observability, ensuring reliability for downstream analytics.
    """
    script_path = os.path.abspath(context.op_config["script_path"])
    model_path = os.path.abspath(context.op_config["model_path"])
    data_lake_path = context.resources.pipeline_resources["data_lake_path"]

    logger.info(f"Starting YOLOv8 detection with script: {script_path}, model: {model_path}, data lake: {data_lake_path}")

    try:
        # Verify script and model exist
        if not os.path.exists(script_path):
            error_msg = f"YOLO detection script not found: {script_path}"
            logger.error(error_msg)
            raise Failure(description=error_msg)
        if not os.path.exists(model_path):
            error_msg = f"YOLO model not found: {model_path}"
            logger.error(error_msg)
            raise Failure(description=error_msg)

        # Run the YOLO detection script
        result = subprocess.run(
            ["python", script_path, "--model", model_path, "--data-lake", data_lake_path],
            capture_output=True,
            text=True,
            check=True  # Raises CalledProcessError on non-zero exit code
        )
        logger.info(f"YOLOv8 detection completed successfully. Output:\n{result.stdout}")
        context.log.info("YOLOv8 detection results stored in PostgreSQL")

    except subprocess.CalledProcessError as e:
        error_msg = f"YOLO detection failed with exit code {e.returncode}:\n{e.stderr}"
        logger.error(error_msg)
        raise Failure(description=error_msg)
    except FileNotFoundError as e:
        error_msg = f"File not found error: {str(e)}"
        logger.error(error_msg)
        raise Failure(description=error_msg)
    except Exception as e:
        error_msg = f"Unexpected error during YOLO detection: {str(e)}"
        logger.error(error_msg)
        raise Failure(description=error_msg)
from dagster import op
import subprocess
import os

@op
def load_raw_to_postgres_op():
    """
    Runs the script that loads raw Telegram messages from the data lake into the PostgreSQL 'raw' schema.
    """
    script_path = os.path.abspath("scripts/load_raw_to_postgres.py")
    result = subprocess.run(["python", script_path], capture_output=True, text=True)

    if result.returncode != 0:
        raise Exception(f"Failed to load raw data:\n{result.stderr}")
    else:
        print(f"Success:\n{result.stdout}")

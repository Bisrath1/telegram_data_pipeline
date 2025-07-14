from dagster import op
import subprocess
import os

@op
def run_dbt_models_op():
    """
    Runs `dbt run` to transform data in the warehouse using dbt models.
    """
    os.chdir("telegram_medical_dbt")
    result = subprocess.run(["dbt", "run"], capture_output=True, text=True)

    if result.returncode != 0:
        raise Exception(f"DBT run failed:\n{result.stderr}")
    else:
        print(f"DBT Output:\n{result.stdout}")

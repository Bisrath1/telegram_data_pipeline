from dagster import op
import subprocess

@op
def run_dbt_models():
    print("Running dbt models...")
    subprocess.run(["dbt", "run"], check=True)

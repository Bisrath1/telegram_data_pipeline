from dagster import op

@op
def load_raw_data():
    # Your logic to load raw telegram data into Postgres
    print("Loading raw telegram data into Postgres...")
    # call your existing Python script or function here

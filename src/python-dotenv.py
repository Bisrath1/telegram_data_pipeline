from dotenv import load_dotenv
import os


load_dotenv()

api_id = os.getenv("API_ID")
db_user = os.getenv("POSTGRES_USER")

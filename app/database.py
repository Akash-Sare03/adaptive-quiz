from pymongo import MongoClient
from dotenv import load_dotenv
import os

load_dotenv()

# Get connection string from .env file
MONGODB_URL = os.getenv("MONGODB_URL")
DATABASE_NAME = os.getenv("DATABASE_NAME")

# Connect to MongoDB
client = MongoClient(MONGODB_URL)
db = client[DATABASE_NAME]

# Collections (like tables in SQL)
questions_collection = db["questions"]
sessions_collection = db["sessions"]

print("✅ Connected to MongoDB!")

# Helper functions
def get_questions_collection():
    return questions_collection

def get_sessions_collection():
    return sessions_collection
import os

from dotenv import load_dotenv

load_dotenv()

# Project
PROJECT_ID = os.getenv("PROJECT_ID")
REGION = os.getenv("REGION")

# Service Account
APP_SERVICE_ACCOUNT_ID = os.getenv("APP_SERVICE_ACCOUNT_ID")
APP_SERVICE_ACCOUNT = os.getenv("APP_SERVICE_ACCOUNT")

# Google Cloud Storage
BUCKET_NAME = os.getenv("BUCKET_NAME")
BUCKET_URI = os.getenv("BUCKET_URI")

# Vertex AI Platform
PROJECT_NAME = os.getenv("PROJECT_NAME")
PIPELINE_ROOT = os.getenv("PIPELINE_ROOT")
COMPILED_PIPELINE_JSON = os.getenv("COMPILED_PIPELINE_JSON")

# Data
CSV_FILE_NAME = os.getenv("CSV_FILE_NAME")
GCS_CSV_PATH = os.getenv("GCS_CSV_PATH")

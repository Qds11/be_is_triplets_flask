import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# S3 Configuration
S3 = {
    'api_key': os.getenv("S3_API_KEY"),
    'headers': {
        "Content-Type": "application/json",
        "X-Contacts-Key": os.getenv("S3_API_KEY")  # Include the API key in the headers
    },
    'url': "https://smuedu-dev.outsystemsenterprise.com/SMULab_AmazonS3/rest/AmazonS3",  # Base URL
    'api_mapping': {
        'fetch': "FetchFile",
        'fetch_url': "FetchFileUrl",
        'upload': "UploadFile",
        'delete': "DeleteFile"
    },
    "folder_name":"Alan4Testing",
    "rules_subfolder_name": "Rules"

}

# Default rules file
DEFAULT_RULES = "e0eceef8136ecfaadca1aa40b2b84e2b.json"


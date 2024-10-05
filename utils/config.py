import os
from dotenv import load_dotenv

# Load environment variables from .env file
#load_dotenv(".env.development")

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
    "folder_name":"CreditEvauation",
    "rules_subfolder_name": "Rules",
    "results_subfolder_name": "Results",
    "default_rules_filename":"Defaults.json",
    "latest_rules_filename":"latest_version.json"

}

OPEN_AI = {
    'api_key': os.getenv("OPENAI_API_KEY"),
    'headers': {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {os.getenv('OPENAI_API_KEY')}"  # Include the API key in the headers
    },
    "model":"gpt-4o",
    "max_tokens": 300,
    "url": "https://api.openai.com/v1/chat/completions"
}

CREDIT_EVALUATION_API_KEY = os.getenv('CREDIT_EVALUATION_API_KEY')
RULES_API_KEY = os.getenv('RULES_API_KEY')



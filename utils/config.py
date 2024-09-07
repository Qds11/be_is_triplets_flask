import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Fetch the API key from environment variables
S3_API_KEY = os.getenv("S3_API_KEY")

# Define common headers for requests
S3_API_HEADERS = {
    "Content-Type": "application/json",
    "X-Contacts-Key": S3_API_KEY  # Include the API key in the headers
}

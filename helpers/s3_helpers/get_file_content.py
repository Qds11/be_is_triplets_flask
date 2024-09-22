
import requests
import json
from helpers.s3_helpers.fetch_file_helper import fetch_file_url_from_s3
from helpers.error_helpers import handle_error

def get_file_content_from_key(filekey, foldername, subfoldername):
    try:
        # Extracting the rules_file from the request payload, or using DEFAULT_RULE
        response_data = fetch_file_url_from_s3(filekey,foldername, subfoldername)

        file_url = response_data.get('url')

        if not file_url:
            return handle_error('File URL not found in the response', 500)

        # Fetch the file content using the URL
        file_response = requests.get(file_url)
        if file_response.status_code != 200:
            return handle_error(f"Unable to download the file from {file_url}. Status code: {file_response.status_code}", 500)

        # Parse the file content as JSON
        try:
            file_content = json.loads(file_response.text)
            return file_content
        except json.JSONDecodeError as e:
            return handle_error(f"Failed to parse JSON from the file. Error: {str(e)}", 500)

    except requests.exceptions.RequestException as re:
        # Capture specific request-related errors
        return handle_error(f"Network error occurred: {str(re)}", 500)

    except Exception as e:
        # Capture all other errors
        return handle_error(f"An unexpected error occurred: {str(e)}", 500)
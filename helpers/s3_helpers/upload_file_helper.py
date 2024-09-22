import requests
from utils.config import S3
import json
import base64

def upload_file_to_s3(file_name, folder_name, subfolder_name, data, override = False):
    upload_url = f"{S3['url']}/{S3['api_mapping']['upload']}"

    # Check for missing parameters
    if not file_name or not folder_name or not subfolder_name or not data:
        raise ValueError('Missing required parameters')

    # Convert the JSON object to a string
    json_string = json.dumps(data)

    # Convert the JSON string to bytes
    json_bytes = json_string.encode('utf-8')

    # Encode the byte data to Base64
    base64_encoded = base64.b64encode(json_bytes)

    # Convert the Base64 byte string back to a regular string (optional, for readability)
    base64_string = base64_encoded.decode('utf-8')

    # Prepare the payload for the external API
    payload = {
        "folderName": folder_name,
        "subFolderName": subfolder_name,
        "fileName": file_name,
        "file": base64_string,
        "override": override
    }

    # Send POST request to the external API
    response = requests.post(upload_url, json=payload, headers=S3["headers"])

    # Check if the request was successful
    if response.status_code != 200:
        raise Exception(f"Failed to fetch file URL. Status code: {response.status_code}, error: {response.text}")

    # Return the response JSON
    return response.json()

import requests
from utils.config import S3

def delete_file_from_s3(key, folder_name, subfolder_name):
    delete_url = f"{S3['url']}/{S3['api_mapping']['delete']}"

    # Check for missing parameters
    if not key:
        raise ValueError('Missing required rules filename')

    # Prepare the payload for the external API
    payload = {
        "folderName": folder_name,
        "subFolderName": subfolder_name,
        "key": key,
    }

    # Send POST request to the external API
    response = requests.post(delete_url, json=payload, headers=S3["headers"])

    # Check if the request was successful
    if response.status_code != 200:
        raise Exception(f"Failed to delete file URL. Status code: {response.status_code}, error: {response.text}")

    # Return the response JSON
    return response.json()
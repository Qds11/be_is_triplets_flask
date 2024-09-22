import requests
from utils.config import S3

def fetch_file_url_from_s3(file_name, folder_name, subfolder_name):
    fetch_url = f"{S3['url']}/{S3['api_mapping']['fetch_url']}"

    # Check for missing parameters
    if not file_name:
        raise ValueError('Missing required rules filename')

    # Prepare the payload for the external API
    payload = {
        "folderName": folder_name,
        "subFolderName": subfolder_name,
        "key": file_name,
    }

    # Send POST request to the external API
    response = requests.post(fetch_url, json=payload, headers=S3["headers"])

    # Check if the request was successful
    if response.status_code != 200:
        raise Exception(f"Failed to fetch file URL. Status code: {response.status_code}, error: {response.text}")

    # Return the response JSON
    return response.json()


def fetch_file_key_from_s3(folder_name, subfolder_name):
    fetch_url = f"{S3['url']}/{S3['api_mapping']['fetch']}"

    # Prepare the payload for the external API
    payload = {
        "folderName": folder_name,
        "subFolderName": subfolder_name,
    }

    # Send POST request to the external API
    response = requests.post(fetch_url, json=payload, headers=S3["headers"])

    # Check if the request was successful
    if response.status_code != 200:
        raise Exception(f"Failed to fetch file key. Status code: {response.status_code}, error: {response.text}")

    # Return the response JSON
    return response.json()

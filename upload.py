from helpers.s3_helpers.upload_file_helper import upload_file_to_s3
from utils.config import  S3
import json
import base64
 # Import helper functions
from flask import request, request, jsonify, url_for
# S3_FOLDER_NAME = S3["folder_name"]
# RESULTS_SUBFOLDER_NAME = S3["rules_subfolder_name"]
# response_data = upload_file_to_s3("Defaults.json",S3_FOLDER_NAME,RESULTS_SUBFOLDER_NAME,{
#   "default_rules": "testrules20240922.json"
# },True
# )
data ={
  "default_rules": "testrules20240922.json"}
json_string = json.dumps(data)

# Convert the JSON string to bytes
json_bytes = json_string.encode('utf-8')

# Encode the byte data to Base64
base64_encoded = base64.b64encode(json_bytes)

# Convert the Base64 byte string back to a regular string (optional, for readability)
base64_string = base64_encoded.decode('utf-8')
print(base64_string)
#print(response_data)
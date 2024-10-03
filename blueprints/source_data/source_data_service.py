import base64
import requests
from pdf2image import convert_from_bytes
from io import BytesIO
import json
from flask import jsonify
#from utils.config import OPEN_AI
# OpenAI API Key
#api_key = OPEN_AI["api_key"]
api_key = None
# Function to encode an image to base64
def encode_image(image):
    buffered = BytesIO()
    image.save(buffered, format="JPEG")
    return base64.b64encode(buffered.getvalue()).decode('utf-8')

def get_source_data(urls):
    all_base64_images = []  # Initialize a 1D list for all base64 images

    for url in urls:
        # Download the PDF from the URL
        pdf_response = requests.get(url)

        # Ensure the request was successful
        if pdf_response.status_code != 200:
            return jsonify({'error': f'Failed to download the PDF from {url}'}), 500

        # Convert the PDF (downloaded as a byte stream) into images using convert_from_bytes
        images = convert_from_bytes(pdf_response.content)

        # Encode each image and extend the main list
        base64_images = [encode_image(image) for image in images]
        all_base64_images.extend(base64_images)  # Combine images into one list

    # Prepare the OpenAI API payload
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {api_key}"
    }

    # Example request content
    content = {
        "type": "text",
        "text": """Read and populate all the data for these 3 financial statements (Balance sheet, Income Statement, Cash Flow) if any in a JSON string, please separate the different types of financial statements (bolded header) by the years (don't return any other text, just the JSON string). Please do not miss anything."""
    }

    # Construct the payload with the text and images
    payload = {
        "model": "gpt-4o",
        "messages": [
            {
                "role": "user",
                "content": [content]
            }
        ]
    }

    # Add each image as base64 encoded data in the payload
    for base64_image in all_base64_images:
        payload["messages"][0]["content"].append({
            "type": "image_url",
            "image_url": {
                "url": f"data:image/jpg;base64,{base64_image}"
            }
        })

    # Send the request to OpenAI API
    response = requests.post("https://api.openai.com/v1/chat/completions", headers=headers, json=payload)

    # Check if the API request was successful
    if response.status_code != 200:
        return jsonify({'error': f"OpenAI API request failed: {response.text}"}), 500

    # Extract the content from the API response
    content = response.json()['choices'][0]['message']['content']

    # Find the index of the first and last curly braces
    start_index = content.find('{')
    end_index = content.rfind('}') + 1

    # Extract the JSON portion from the string
    json_string = content[start_index:end_index]
    json_data = json.loads(json_string)

    # Print or return the extracted JSON data
    print(json_data)
    return json_data



#get_source_data(["https://smu-bucket1.s3.ap-southeast-1.amazonaws.com/CreditEvauation/FinancialStatements/b8d37e2e2bf51c92e13185684406ca9c.pdf?X-Amz-Expires=604800&X-Amz-Algorithm=AWS4-HMAC-SHA256&X-Amz-Credential=AKIAZ4SULJZKRVBUSV45/20241003/ap-southeast-1/s3/aws4_request&X-Amz-Date=20241003T162558Z&X-Amz-SignedHeaders=host&X-Amz-Signature=c6c5486c56791251afae7a13d3f534ee752fe25f3f9ca5ed86335dfeb5ee2c8c"])
get_source_data(["https://smu-bucket1.s3.ap-southeast-1.amazonaws.com/CreditEvauation/FinancialStatements/d4e98a5d337d2936753c701b9531cbdb.pdf?X-Amz-Expires=604800&X-Amz-Algorithm=AWS4-HMAC-SHA256&X-Amz-Credential=AKIAZ4SULJZKRVBUSV45/20241003/ap-southeast-1/s3/aws4_request&X-Amz-Date=20241003T175129Z&X-Amz-SignedHeaders=host&X-Amz-Signature=50451fdb2d2238733ff1d411299176842ec50d06e1054b289eed31bc216048e4","https://smu-bucket1.s3.ap-southeast-1.amazonaws.com/CreditEvauation/FinancialStatements/c3968e84796b139cdab859a89b1dd857.pdf?X-Amz-Expires=604800&X-Amz-Algorithm=AWS4-HMAC-SHA256&X-Amz-Credential=AKIAZ4SULJZKRVBUSV45/20241003/ap-southeast-1/s3/aws4_request&X-Amz-Date=20241003T175140Z&X-Amz-SignedHeaders=host&X-Amz-Signature=2685b6e2b2f448e5b5faf1e4d916a0bd3ae54adbddcee381b2f58d24103dc3fa"])
# risk_grade_service.py
from helpers.s3_helpers.get_file_content import get_file_content_from_key
from helpers.s3_helpers.upload_file_helper import upload_file_to_s3
from utils.config import S3
from datetime import datetime

S3_FOLDER_NAME = S3["folder_name"]
RISK_GRADES_SUBFOLDER_NAME = S3["risk_grades_subfolder_name"]
DEFAULT_RISK_GRADES_FILENAME = S3["default_risk_grades_filename"]
LATEST_RISK_GRADES_FILENAME = S3["latest_risk_grades_filename"]


def get_risk_grade(credit_score, risk_grade_version=None):
    """Gets the risk grade for a given credit score."""
    # Fetch the risk grades (default version or provided version)
    data = fetch_risk_grades(risk_grade_version)
    risk_grades = data["risk_grades"]["risk_grades"]
    # Iterate through the risk grade limits and return the appropriate grade
    for grade, limits in risk_grades.items():
        if limits["lower"] <= credit_score <= limits["upper"]:
            return grade

    return "Grade not found"


# Logic to update the default risk grade
def update_default_risk_grade(new_default_risk_version):
    if not new_default_risk_version:
        raise ValueError('New default risk grade version number is required')

    data = {"default_risk_grade": new_default_risk_version}
    upload_file_to_s3(DEFAULT_RISK_GRADES_FILENAME, S3_FOLDER_NAME, RISK_GRADES_SUBFOLDER_NAME, data, True)
    default_risk_file_content = get_file_content_from_key(DEFAULT_RISK_GRADES_FILENAME, S3_FOLDER_NAME, RISK_GRADES_SUBFOLDER_NAME)

    return default_risk_file_content["default_risk_grade"]

# Logic to get the default risk grade
def get_default_risk_grade():
    default_risk_file_content = get_file_content_from_key(DEFAULT_RISK_GRADES_FILENAME, S3_FOLDER_NAME, RISK_GRADES_SUBFOLDER_NAME)
    default_risk_file = default_risk_file_content["default_risk_grade"]
    return default_risk_file

# Logic to fetch the risk grades (by version or default)
def fetch_risk_grades(risk_grade_version=None):
    if not risk_grade_version:
        risk_grade_version = get_default_risk_grade()

    print("Risk grade version:", risk_grade_version)
    risk_grade_file = f"risk_grade_v{risk_grade_version}.json"

    risk_grade_content = get_file_content_from_key(risk_grade_file, S3_FOLDER_NAME, RISK_GRADES_SUBFOLDER_NAME)
    return {"risk_grade_file": risk_grade_file, "risk_grades": risk_grade_content}

# Logic to upload new risk grades
def upload_risk_grades_service(risk_grades, description='', set_default=False):
    try:
        current_time = datetime.now()
        formatted_time = current_time.strftime('%Y-%m-%d %H:%M:%S')

        # Prepare risk grade file content
        risk_grades_content = {
            'timestamp': formatted_time,
            'description': description,
            'risk_grades': risk_grades
        }

        # Get latest risk grades version
        latest_version = get_file_content_from_key(LATEST_RISK_GRADES_FILENAME, S3_FOLDER_NAME, RISK_GRADES_SUBFOLDER_NAME)["latest_version"]
        current_version = latest_version + 1
        filename = f"risk_grade_v{current_version}.json"

        # Upload new risk grade version file
        key = upload_file_to_s3(filename, S3_FOLDER_NAME, RISK_GRADES_SUBFOLDER_NAME, risk_grades_content, True)
        latest_version_data = {"latest_version": current_version}

        if set_default:
            update_default_risk_grade(current_version)  # Call the logic to update default risk grade

        upload_file_to_s3(LATEST_RISK_GRADES_FILENAME, S3_FOLDER_NAME, RISK_GRADES_SUBFOLDER_NAME, latest_version_data, True)

        return {'message': 'Risk grade file uploaded', 'key': key["key"]}

    except Exception as e:
        raise Exception(f"Error uploading risk grade file: {str(e)}")

# Logic to get all risk grades
def get_all_risk_grades():
    try:
        latest_version = get_file_content_from_key(LATEST_RISK_GRADES_FILENAME, S3_FOLDER_NAME, RISK_GRADES_SUBFOLDER_NAME)["latest_version"]
        risk_grade_files = {}

        for version in range(1, latest_version + 1):
            risk_grades = get_file_content_from_key(f"risk_grade_v{version}.json", S3_FOLDER_NAME, RISK_GRADES_SUBFOLDER_NAME)
            if not isinstance(risk_grades, dict):
                risk_grade_files[f"risk_grade_v{version}.json"] = "Something is wrong with this file. Unable to get file content."
            else:
                risk_grade_files[f"risk_grade_v{version}.json"] = risk_grades

        return risk_grade_files
    except Exception as e:
        raise Exception(f"Error getting risk grade files: {str(e)}")

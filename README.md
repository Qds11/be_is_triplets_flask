# be_is_triplets_flask

Set up a virtual environment before starting this project

## How to set up a virtual env
```
python3 -m venv venv
source ./venv/bin/activate
```

## Create .env file
```
CORS_ALLOWED_ORIGINS=http://localhost,http://127.0.0.1,http://your-frontend-domain.com
AWS_ACCESS_KEY_ID=your-aws-access-key-id
AWS_SECRET_ACCESS_KEY=your-aws-secret-access-key
S3_BUCKET=your-s3-bucket-name

```

## Install required packages

```
pip install -r requirements.txt
```

## Running the server
```
python app.py

```
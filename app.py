from flask import Flask, request, jsonify, send_file, render_template
import boto3
import os
from werkzeug.utils import secure_filename
from datetime import datetime
import uuid

# Initialize Flask app
app = Flask(__name__)

# AWS S3 Configuration
AWS_ACCESS_KEY = "YOUR ACCESS KEY"
AWS_SECRET_KEY = "YOUR SECRET KEY"
S3_BUCKET = "YOUR BUCKET NAME"
S3_REGION = "YOUR BUCKET REGION"

# Initialize Boto3 S3 client
s3 = boto3.client(
    "s3",
    aws_access_key_id=AWS_ACCESS_KEY,
    aws_secret_access_key=AWS_SECRET_KEY,
    region_name=S3_REGION,
)

UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# Upload File API
@app.route("/upload", methods=["POST"])
def upload_file():
    file = request.files["file"]
    if file:
        filename = secure_filename(file.filename)
        file_id = str(uuid.uuid4())  # Unique ID
        s3.upload_fileobj(file, S3_BUCKET, filename)
        return jsonify({"message": "File uploaded successfully", "file_id": file_id}), 200
    return jsonify({"error": "No file provided"}), 400

# Download File API
@app.route("/download/<filename>", methods=["GET"])
def download_file(filename):
    s3.download_file(S3_BUCKET, filename, f"{UPLOAD_FOLDER}/{filename}")
    return send_file(f"{UPLOAD_FOLDER}/{filename}", as_attachment=True)

@app.route("/")
def home():
    return render_template("index.html")

if __name__ == "__main__":
    app.run(debug=True)

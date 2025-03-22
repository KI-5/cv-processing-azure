from flask import Flask, request, jsonify
import os
from dotenv import load_dotenv
from werkzeug.utils import secure_filename
from azure.storage.blob import BlobServiceClient
# from azure.ai.vision import VisionClient
# from email.mime.text import MIMEText
# from email.mime.multipart import MIMEMultipart
import logging
logging.basicConfig(level=logging.INFO)
from cv_processing import extract_cv_data
from email_service import send_followup_email


load_dotenv(override=True)
app=Flask(__name__)


#Blob config
blob_account_name=os.getenv("AZURE_STORAGE_ACCOUNT_NAME")
blob_account_key=os.getenv("AZURE_STORAGE_ACCOUNT_KEY")
blob_container_name="cv-uploads"

blob_service_client=BlobServiceClient(f"https://{blob_account_name}.blob.core.windows.net",credential=blob_account_key)

# #computer vision config
# vision_endpoint=os.getenv("AZURE_VISION_ENDPOINT")
# vision_key=os.getenv("AZURE_VISION_KEY")
# vision_client=VisionClient(vision_endpoint, vision_key)

# #gmail smtp config
# gmail_user=os.getenv("GMAIL_USER")
# gmail_pass=os.getenv("GMAIL_PASS")



#uploading directory
upload_folder="uploads"
os.makedirs(upload_folder, exist_ok=True)
app.config["upload_folder"]=upload_folder

#define the allowed extensions
accepted_extensions={"pdf", "docx"}

'''
Method to define allowed file types
@param filename: name of the file
@return: boolean value
'''
def allowed_file(filename):
    return "." in filename and filename.rsplit(".", 1)[1].lower() in accepted_extensions


'''Method to upload the CV
@return: JSON response
'''
@app.route("/upload", methods=["POST"])
def upload_cv():
    logging.debug("Uploading CV")
    if "cv" not in request.files:
        return jsonify({"error": "No file uploaded"}), 400

    file=request.files["cv"]
    if file.filename=="" or not allowed_file(file.filename):
        return jsonify({"error":"Invalid file type"}), 400

    #save the file
    filename=secure_filename(file.filename)
    file_path=os.path.join(app.config["upload_folder"], filename)
    file.save(file_path)

    #upload to blob stoage
    blob_client = blob_service_client.get_blob_client(container=blob_container_name, blob=filename)
    with open(file_path, "rb") as data:
        blob_client.upload_blob(data, overwrite=True)

    blob_url = f"https://{blob_account_name}.blob.core.windows.net/{blob_account_name}/{filename}"

    # Extract text using Azure Computer Vision
    cv_data = extract_cv_data(blob_url)
    

    # Store extracted data as JSON in Blob Storage
    json_filename = f"{filename.rsplit('.', 1)[0]}.json"
    json_blob_client = blob_service_client.get_blob_client(container=blob_container_name, blob=json_filename)
    json_blob_client.upload_blob(json.dumps(cv_data), overwrite=True)

    # Extract name & email from CV
    applicant_name = cv_data.get("name", "Applicant")
    applicant_email = cv_data.get("email", "")

    # Send email if email exists
    email_status = "No email sent"
    if applicant_email:
        email_status = send_followup_email(applicant_email, applicant_name)

    # Response
    return jsonify({
        "cv_public_link": blob_url,
        "cv_data": cv_data,
        "json_blob_url": f"https://{blob_account_name}.blob.core.windows.net/{blob_container_name}/{json_filename}",
        "email_status": email_status
    })

if __name__=="__main__":
    app.run(debug=True)

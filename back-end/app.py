from flask import Flask, request, jsonify
import os
from dotenv import load_dotenv
from werkzeug.utils import secure_filename
from upload_to_drive import upload_to_drive
from cv_processing import extract_cv_data
# from process_cv import extract_cv_data
from sheets import store_in_google_sheets
from webhook import send_webhook
from email_to_send import send_followup_email
import logging
logging.basicConfig(level=logging.INFO)


load_dotenv(override=True)
app=Flask(__name__)

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

    #upload to gdrive
    drive_link=upload_to_drive(file_path)

    #extracting data from cv
    cv_data=extract_cv_data(file_path)

    #get name and email of applicant
    applicant_name = cv_data["personal_info"].get("name", "Applicant")
    applicant_email = cv_data["personal_info"].get("email", "unknown@example.com")
    print(applicant_email)
    #storing in sheets
    store_in_google_sheets(cv_data, drive_link)

    # Send follow-up email
    if applicant_email != "unknown@example.com":
        email_status = send_followup_email(applicant_email, applicant_name)
        logging.info(f"Follow-up email status: {email_status}")
    else:
        logging.warning("No valid email found in CV data. Skipping follow-up email.")


    logging.debug("Data stored in Google Sheets. Calling webhook")
    #seding webhook
    #webhook_response=send_webhook(cv_data, drive_link)
    #logging.debug("Webhook response received", webhook_response)
    #response data
    response_data={
        "cv_public_link":drive_link,
        "cv_data":cv_data,
        #"webhook_response":webhook_response,
        "email_status": email_status if applicant_email != "unknown@example.com" else "No email sent"
    }

    return jsonify(response_data)

if __name__=="__main__":
    app.run(debug=True)

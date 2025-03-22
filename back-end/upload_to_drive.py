import os
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload
from google.oauth2 import service_account

SCOPES = ["https://www.googleapis.com/auth/drive.file"]
SERVICE_ACCOUNT_FILE = "service_account.json"

'''
Method to upload the file to Google Drive
@param file_path: path to the file
@return: link to the file in Google Drive
'''
def upload_to_drive(file_path):
    creds=service_account.Credentials.from_service_account_file(SERVICE_ACCOUNT_FILE, scopes=SCOPES)
    drive_service=build("drive", "v3", credentials=creds)

    file_metadata={"name": os.path.basename(file_path), "parents": ["1NxemdbSC2r4Tu_QqFOiKdqUdxJtD7naY"]} 
    media=MediaFileUpload(file_path, resumable=True)
    uploaded_file=drive_service.files().create(body=file_metadata, media_body=media, fields="id").execute()

    file_id=uploaded_file.get("id")
    drive_link=f"https://drive.google.com/uc?id={file_id}"
    return drive_link



import gspread
from google.oauth2.service_account import Credentials

access_file="service_account.json"  
spreadsheet_name="Job Applications"

'''
Method to store data in Google Sheets
@param cv_data:data extracted from the CV
@param cv_link:link to the CV
'''
def store_in_google_sheets(cv_data, cv_link):
    try:
        print("Authenticate and connect with sheets.....")
        print("Data: " ,cv_data)
        #credeqntials
        creds=Credentials.from_service_account_file(access_file, scopes=["https://www.googleapis.com/auth/spreadsheets", "https://www.googleapis.com/auth/drive"])
        client= gspread.authorize(creds)
        #open sheet
        sheet =client.open(spreadsheet_name).sheet1 
        print("Connected..", sheet.title)
    
            
        #append the data to the sheet
        row= [
            cv_data.get("personal_info", {}).get("name", ""),
            cv_data.get("personal_info", {}).get("email", ""),
            ", ".join(cv_data.get("education", [])),
            ", ".join(cv_data.get("certifications", [])),
            ", ".join(cv_data.get("projects", [])),
            cv_link
        ]
        sheet.append_row(row)
        print("Data stored successfully", row)
        return "Data stored successfully"
    except Exception as e:
    
        print("Error:", str(e))
        return f"Failed to store data: {str(e)}"



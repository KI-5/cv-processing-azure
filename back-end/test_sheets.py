import gspread
from google.oauth2.service_account import Credentials

access_file = "service_account.json"  
spreadsheet_name = "Job Applications"

def test_store_in_google_sheets():
    try:
        print("Authenticating with Google Sheets...")
        creds = Credentials.from_service_account_file(access_file, scopes = ["https://www.googleapis.com/auth/spreadsheets"])
        client = gspread.authorize(creds)
        sheet = client.open(spreadsheet_name).sheet1  
        print("Connected successfully!")

        # Test writing dummy data
        row = ["Test Name", "test@example.com", "CS Degree", "Python Cert", "Test Project", "https://testdrive.com"]
        sheet.append_row(row)

        print("✅ Data stored successfully in Google Sheets!")
    except Exception as e:
        print("❌ Error storing data in Google Sheets:", e)

# Run the test
test_store_in_google_sheets()

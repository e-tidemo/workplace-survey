import gspread
from google.oauth2.service_account import Credentials

SCOPE = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive.file",
    "https://www.googleapis.com/auth/drive"
    ]

CREDS = Credentials.from_service_account_file('creds.json')
SCOPED_CREDS = CREDS.with_scopes(SCOPE)
GSPREAD_CLIENT = gspread.authorize(SCOPED_CREDS)
SHEET = GSPREAD_CLIENT.open('workplace_survey')

def get_workplace_data():
    """
    Get answers about workplace environment from employees
    """
    print("Please answer the following questions as truthfully as possible")

    data_str = input("Enter your job title here: ")

    work_data = data_str.split(",")
    validate_data(work_data)

def validate_data(values):
    print(values)


get_workplace_data()
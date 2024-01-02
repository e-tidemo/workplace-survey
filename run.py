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
    while True:
        print("Please register what department you work in, design, hr, project management or customer service")
        print("You need to enter the name of your department in lowercase letters")

        data_str = input("Enter your department here: ")

        work_data = data_str.split(",")
        validate_data(work_data)

        if validate_data(work_data):
            print("Data is valid!")
            break

    return work_data

def validate_data(values):
    """
    Raises ValueError if input is not a valid department
    """
    valid_departments = ["design", "hr", "project management", "customer service"]

    try:
        if values[0] not in valid_departments:
            raise ValueError("This department does not exist here")
    except ValueError as e:
        print(f"Invalid data: {e}, please try again. \n")
        return False

    return True

data = get_workplace_data()
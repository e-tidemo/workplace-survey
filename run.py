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

def get_department_data():
    """
    Get answers about what department the person answering works in
    """
    while True:
        print("Please register what department you work in\n")
        print("Do you work in design, hr, project management or customer service? \n")
        print("You need to enter the name of your department in lowercase letters \n")

        data_str = input("Enter your department here: ")
        department_data = data_str.split(",")

        validate_data(department_data)

        if validate_data(department_data):
            print("Data is valid!")
            break

    return department_data



def get_age_data():
    """
    Get answers about the age of the person answering the survey
    """
    while True:
        print("Please register your age\n")
        print("You need to enter your age in numbers \n")

        age_str = input("Enter your age here: ")
        age_data = age_str.split(",")

        validate_data(age_data)

        if validate_data(age_data):
            print("Data is valid!")
            break

    return age_data


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

def update_sheet1_worksheet(data):
    """
    Update survey worksheet, add new row with the list data provided
    """
    print("Updating Work Survey worksheet...\n")
    work_worksheet = SHEET.worksheet("Sheet1")
    work_worksheet.append_row(data)
    print("Work survey worksheet updated successfully.\n")

data = get_department_data()
print(data)
update_sheet1_worksheet(data)
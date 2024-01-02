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

        validate_data([data_str])

        if validate_data([data_str]):
            print("Data is valid!")
            break

    return [data_str]



def get_age_data():
    """
    Get answers about the age of the person answering the survey
    """
    while True:
        print("Please register your age\n")
        print("You need to enter your age in numbers \n")

        age_str = input("Enter your age here: ")

        validate_age([age_str])

        if validate_age([age_str]):
            print("Data is valid!")
            break

    return [age_str]

def get_gender_data():
    """
    Get answers about the gender of the person answering the survey
    """
    while True:
        print("Please register your gender\n")
        print("You need to enter your gender as male, female, or other \n")

        gender_str = input("Enter your gender here: ")

        validate_gender([gender_str])

        if validate_gender([gender_str]):
            print("Data is valid!")
            break

    return [gender_str]

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

def validate_age(values):
    """
    Raises ValueError if input is not a valid age
    """
    try:
        age = int(values[0])
        if age < 18 or age > 70:
            raise ValueError("Age must be between 18 and 70")
    except ValueError as e:
        print(f"Invalid data: {e}, please try again. \n")
        return False

    return True

def validate_gender(values):
    """
    Raises ValueError if input is not a valid gender
    """
    valid_genders = ["male", "female", "other"]

    try:
        if values[0] not in valid_genders:
            raise ValueError("Gender must be male, female, or other")
    except ValueError as e:
        print(f"Invalid data: {e}, please try again. \n")
        return False

    return True

def collect_survey_data():
    """
    Collect all survey answers into one list
    """
    department_data = get_department_data()
    age_data = get_age_data()
    gender_data = get_gender_data()

    survey_data = department_data + age_data + gender_data

    return survey_data

def update_sheet1_worksheet(data):
    """
    Update survey worksheet, add new row with the list data provided
    """
    print("Updating Work Survey worksheet...\n")
    work_worksheet = SHEET.worksheet("Sheet1")
    work_worksheet.append_row(data)
    print("Work survey worksheet updated successfully.\n")

all_survey_data = collect_survey_data()
print(all_survey_data)
update_sheet1_worksheet(all_survey_data)
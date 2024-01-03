import gspread
from google.oauth2.service_account import Credentials
import pandas as pd

SCOPE = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive.file",
    "https://www.googleapis.com/auth/drive"
    ]

CREDS = Credentials.from_service_account_file('creds.json')
SCOPED_CREDS = CREDS.with_scopes(SCOPE)
GSPREAD_CLIENT = gspread.authorize(SCOPED_CREDS)
SHEET = GSPREAD_CLIENT.open('workplace_survey')
WORKSHEET_TITLE = 'Sheet1'
spreadsheet = SHEET
worksheet = spreadsheet.worksheet(WORKSHEET_TITLE)

# Questions for the survey
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
        print("You need to enter your gender as male, female, or other. Remember to use lowercase letters. \n")

        gender_str = input("Enter your gender here: ")

        validate_gender([gender_str])

        if validate_gender([gender_str]):
            print("Data is valid!")
            break

    return [gender_str]

def get_office_data():
    """
    Get answers about the physical work environment in the office
    """
    while True:
        print("Take a moment and think about how you find the physical work environment in the office.\n")
        print("Consider things like the heating, ergonomic aspect of your desk area, noise level, etc. \n")
        print("You then need to enter how you feel the work environment is based on the scale 'terrible', 'bad', 'needs improvement', 'good', 'great'.\n")
        print("Please write your answer in lowercase letters. \n")

        office_str = input("Enter your view of the physical office work environment here: ")

        validate_office([office_str])

        if validate_office([office_str]):
            print("Data is valid!")
            break

    return [office_str]

def get_social_data():
    """
    Get answers about the social work environment
    """
    while True:
        print("Take a moment and think about how you find the social work environment.\n")
        print("You then need to enter how you feel the work environment is based on the scale 'terrible', 'bad', 'needs improvement', 'good', 'great'.\n")
        print("Please write your answer in lowercase letters. \n")

        social_str = input("Enter your view of the social work environment here: ")

        validate_office([social_str])

        if validate_office([social_str]):
            print("Data is valid!")
            break

    return [social_str]

def get_lunchroom_data():
    """
    Get answers about the physical work environment in the lunch room/ break room
    """
    while True:
        print("Take a moment and think about how you find the physical work environment in the break room/lunch room.\n")
        print("Consider things like the heating, noise level, enough space for everyone, etc. \n")
        print("You then need to enter how you feel the environment in the break room is based on the scale 'terrible', 'bad', 'needs improvement', 'good', 'great'.\n")
        print("Please write your answer in lowercase letters.\n")

        lunchroom_str = input("Enter your view of the environment in the break room/lunch room here: ")

        validate_office([lunchroom_str])

        if validate_office([lunchroom_str]):
            print("Data is valid!")
            break

    return [lunchroom_str]

# Make sure all inputs are valid data that will work in the survey
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

def validate_office(values):
    """
    Raises ValueError if input is not one of the terrible - great-scale options
    """
    valid_office = ["terrible", "bad", "needs improvement", "good", "great"]

    try:
        if values[0] not in valid_office:
            raise ValueError("The answer you have given is not one of the options in the scale from terrible to great")
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
    office_data = get_office_data()
    social_data = get_social_data()
    lunchroom_data = get_lunchroom_data()

    survey_data = department_data + age_data + gender_data + office_data + social_data + lunchroom_data

    return survey_data

def update_sheet1_worksheet(data):
    """
    Update survey worksheet, add new row with the list data provided
    """
    print("Updating Work Environment Survey worksheet...\n")
    work_worksheet = SHEET.worksheet("Sheet1")
    work_worksheet.append_row(data)
    print("Work Environment Survey worksheet updated successfully.\n")

# Calculations of correlations between positive/negative answers and age/gender
# First - define age groups.
# Code to define the age groups is from towadsdatascience.com
def age_group(age):
    
    """
    Creates an age bucket for each participant using the age variable.
    Meant to be used on a DataFrame with .apply().
    """
    
    # Convert to an int, in case the data is read in as an "object" (aka string)
    age = int(age)
    
    if age < 30:
        bucket = '<30'
    
    # Age 30 to 39 ('range' excludes upper bound)
    if age in range(30, 35):
        bucket = '30-34'
        
    if age in range(35, 40):
        bucket = '35-39'
        
    if age in range(40, 45):
        bucket = '40-44'
    
    if age in range(45, 50):
        bucket = '45-49'
   
    if age >= 50:
        bucket = '50+'

    return bucket 

def process_data(df):
    df['Age_Bucket'] = df['Age'].apply(age_group)

# How to get data from spreadsheet into python is done with the help of code from Dataquest - see credits in README
def calculate_total_responses(worksheet, all_responses):
    data = worksheet.get_all_records()
    df = pd.DataFrame(data)

    print("Columns in DataFrame:")
    print(df.columns)
    process_data(df)

    # Count occurrences of all responses in specified age groups
    age_groups_to_count = ['<30', '30-34','35-39', '40-44', '45-49', '50+']
    
    print("Number of responses in each age group:")
    for age_group in age_groups_to_count:
        count_all = df[df['Age_Bucket'] == age_group].apply(lambda row: row.isin(all_responses)).sum(axis=1).sum()
        print(f"{age_group}: {count_all}")
    
    # Count occurrences of all responses in specified gender groups
    gender_groups_to_count = ['male', 'female', 'other']
    
    print("\nNumber of responses in each gender group:")
    for gender_group in gender_groups_to_count:
        count_all = df[df['Gender'] == gender_group].apply(lambda row: row.isin(all_responses)).sum(axis=1).sum()
        print(f"{gender_group}: {count_all}")

    return count_all
    
# Count occurrences of 'terrible', 'bad' and 'needs improvement' in specified gender groups
def calculate_correlation(worksheet, negative_responses):
    data = worksheet.get_all_records()
    df = pd.DataFrame(data)

    print("Columns in DataFrame:")
    print(df.columns)
    process_data(df)

    negative_responses = ["terrible", "bad", "needs improvement"]

    # Count occurrences of 'terrible', 'bad' and 'needs improvement' in specified age groups
    age_groups_to_count = ['<30', '30-34','35-39', '40-44', '45-49', '50+']
    
    print("Number of negative responses in each age group:")
    for age_group in age_groups_to_count:
        count_negative = df[df['Age_Bucket'] == age_group].apply(lambda row: row.isin(negative_responses)).sum(axis=1).sum()
        count_all = df[df['Age_Bucket'] == age_group].apply(lambda row: row.isin(["terrible", "bad", "needs improvement", "good", "great"])).sum(axis=1).sum()
        print(f"{age_group}: {count_negative} out of {count_all}")
    
    # Count occurrences of 'terrible', 'bad' and 'needs improvement' in specified gender groups
    gender_groups_to_count = ['male', 'female', 'other']
    
    print("\nNumber of negative responses in each gender group:")
    for gender_group in gender_groups_to_count:
        count_negative = df[df['Gender'] == gender_group].apply(lambda row: row.isin(negative_responses)).sum(axis=1).sum()
        count_all = df[df['Gender'] == gender_group].apply(lambda row: row.isin(["terrible", "bad", "needs improvement", "good", "great"])).sum(axis=1).sum()
        print(f"{gender_group}: {count_negative} out of {count_all}")

    return count_all, count_negative

def main():
    all_survey_data = collect_survey_data()
    print(all_survey_data)
    update_sheet1_worksheet(all_survey_data)
    data = worksheet.get_all_records()
    df = pd.DataFrame(data)

    process_data(df)

    count_all = calculate_total_responses(worksheet, ["terrible", "bad", "needs improvement", "good", "great"])
    calculate_correlation(worksheet, ["terrible", "bad", "needs improvement"])

print("Welcome to the first step in improving our work environment together!\n")
main()

import gspread
import os
from google.oauth2.service_account import Credentials
import pandas as pd
from operator import itemgetter

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
        print("Please register what department you work in.\n")
        print("Do you work in design, hr, ")
        print("project management or customer service? \n")
        print("Enter the name of your department in lowercase letters \n")

        data_str = input("Enter your department here: \n")

        validate_data([data_str])

        if validate_data([data_str]):
            break

    return [data_str]


def get_age_data():
    """
    Get answers about the age of the person answering the survey
    """
    while True:
        print("Please register your age\n")
        print("You need to enter your age in numbers \n")

        age_str = input("Enter your age here: \n")

        validate_age([age_str])

        if validate_age([age_str]):
            break

    return [age_str]


def get_gender_data():
    """
    Get answers about the gender of the person answering the survey
    """
    while True:
        print("Please register your gender\n")
        print("You need to enter your gender as male, female, or other.")
        print("Remember to use lowercase letters. \n")

        gender_str = input("Enter your gender here: \n")

        validate_gender([gender_str])

        if validate_gender([gender_str]):
            break

    return [gender_str]


def get_office_data():
    """
    Get answers about the physical work environment in the office
    """
    while True:
        print("Take a moment and think about how you find")
        print("the physical work environment in the office.\n")
        print("Consider things like the heating, ")
        print("ergonomic aspect of your desk area, noise level, etc. \n")
        print("Enter how you feel the work environment is using the scale")
        print("'terrible', 'bad', 'needs improvement', 'good', 'great'.\n")
        print("Please write your answer in lowercase letters. \n")

        office_str = input("I think the work environment in the office is: \n")

        validate_office([office_str])

        if validate_office([office_str]):
            break

    return [office_str]


def get_social_data():
    """
    Get answers about the social work environment
    """
    while True:
        print("Take a moment ")
        print("to think about how the social work environment is.\n")
        print("Enter how you feel the work environment is using the scale")
        print("'terrible', 'bad', 'needs improvement', 'good', 'great'.\n")
        print("Please write your answer in lowercase letters. \n")

        social_str = input("I think the social work environment is: \n")

        validate_office([social_str])

        if validate_office([social_str]):
            break

    return [social_str]


def get_lunchroom_data():
    """
    Get answers about the physical work environment
    in the lunch room/ break room
    """
    while True:
        print("Take a moment and think about how you find the physical")
        print("work environment in the break room/lunch room.\n")
        print("Consider things like the heating, noise level, ")
        print("enough space for everyone, etc. \n")
        print("Enter how you find the environment in the break room using the")
        print(" scale 'terrible', 'bad', 'needs improvement', 'good', \n")
        print("'great'. Please write your answer in lowercase letters.\n")

        lunchroom_str = input("The environment in the break room is: \n")

        validate_office([lunchroom_str])

        if validate_office([lunchroom_str]):
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
            raise ValueError("The answer you gave is not in the given scale")
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
    print("Thank you for your participation! ")
    print("We will talk more about work environment")
    print("and the results of this survey at our next Monday meeting. \n")
    print("If you are admin staff you can enter")
    print("your password to see the results of the survey.\n")


def show_results_password():
    while True:
        password_str = input("Enter the password here: \n")
        if validate_password([password_str]):
            return True
        else:
            print("If you are in the admin staff, re-enter the password.\n")


def validate_password(values):
    """
    Raises ValueError if input is not one of the terrible - great-scale options
    """
    valid_password = os.environ.get("ADMIN")

    try:
        if values[0] not in valid_password:
            raise ValueError("The password you have submitted is not correct")
    except ValueError as e:
        print(f"Invalid data: {e}, please try again or leave the survey. \n")
        return False

    return True


# Calculations of correlations between positive/negative answers and age/gender
# First - define age groups.
# Code to define the age groups is from towardsdatascience.com
def age_group(age):
    """
    Creates an age bucket for each participant using the age variable.
    Meant to be used on a DataFrame with .apply().
    """

    # Convert to an int, in case the data is read in as a string
    age = int(age)
    if age < 30:
        bucket = '<30'

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


# Count occurrences of 'terrible', 'bad' and 'needs improvement' in
# each gender group
def calculate_correlation(worksheet, negative_responses):
    """
    Calculate the amount of negative responses in each age and gender group
    """
    data = worksheet.get_all_records()
    df = pd.DataFrame(data)

    print("Columns in DataFrame:")
    print(df.columns)
    process_data(df)

    negative_responses = ["terrible", "bad", "needs improvement"]

    age_groups_to_count = ['<30', '30-34', '35-39', '40-44', '45-49', '50+']

    print("Amount of negative responses in each age group:")

    for age_group in age_groups_to_count:

        count_negative = 0
        count_all = 0

        filtered_df = df[df['Age_Bucket'] == age_group]

        for index, row in filtered_df.iterrows():
            for response in row:
                if response in negative_responses:
                    count_negative += 1
                if response in negative_responses + ["good", "great"]:
                    count_all += 1

        neg_percent_age = int((count_negative / count_all * 100)) if count_all != 0 else 0
        print(f"{age_group}: {neg_percent_age}%")

    gender_groups_to_count = ['male', 'female', 'other']
    print("Amount of negative responses in each gender group:")

    for gender_group in gender_groups_to_count:

        count_negative = 0
        count_all = 0

        filtered_df = df[df['Gender'] == gender_group]

        for index, row in filtered_df.iterrows():
            for response in row:
                if response in negative_responses:
                    count_negative += 1
                if response in negative_responses + ["good", "great"]:
                    count_all += 1
        neg_percent_gender = int((count_negative / count_all * 100)) if count_all != 0 else 0
        print(f"{gender_group}: {neg_percent_gender}%")

    return count_all, count_negative


def calculate_urgent(worksheet, negative_responses, count_all):
    """
    Calculates the percentage of negative responses
    in each area of work environment and
    presents the area with most negative responses
    """
    data = worksheet.get_all_records()
    df = pd.DataFrame(data)

    print("Columns in DataFrame:")
    print(df.columns)
    process_data(df)

    negative_responses = ["terrible", "bad", "needs improvement"]

    columns_to_count = ['Office', 'Social', 'Break room']

    print("Amount of negative opinions in each area, ")
    print("presented in order from highest percentage to lowest:")

    results = []

    for column in columns_to_count:
        count_negative = 0
        count_all = 0

        for index, response in df[column].items():
            if response in negative_responses:
                count_negative += 1
            if response in negative_responses + ["good", "great"]:
                count_all += 1
        neg_percent_columns = int((count_negative / count_all * 100)) if count_all != 0 else 0
        results.append((column, neg_percent_columns))

    results.sort(reverse=True, key=itemgetter(1))

    for column, percentage in results:
        print(f"{column}: {percentage}%")

    return count_all, count_negative


def main():
    all_survey_data = collect_survey_data()
    update_sheet1_worksheet(all_survey_data)
    data = worksheet.get_all_records()
    df = pd.DataFrame(data)

    process_data(df)

    if show_results_password():
        calculate_correlation(worksheet, ["terrible", "bad", "needs improvement"])
        calculate_urgent(worksheet, 'negative_responses', 'count_all')
    else:
        pass


print("Welcome to the first step ")
print("in improving our work environment together!\n")
print("In the following survey you will need to answer in lowercase letters. \n")
print("Please take some time to read the instructions that come with ")
print("each question and take some time to think about your answers. \n")
main()

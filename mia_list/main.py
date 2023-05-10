# -----------------------------------------------------------
# Creates Google Sheet containing list of MIA students based
# off of master list stored in Google Sheet
#
# -----------------------------------------------------------

import gspread
import numpy as np
from date import *
np.set_printoptions(threshold=np.inf)


def cur_week_list(raw_data):
    """
    This function generates a list of students who are missing in the current week based on the provided raw data.

    Args:
        raw_data (numpy array): The raw data containing the attendance records.

    Returns:
        list: A list of students who are missing in the current week.
    """
    # Getting the list of dates for the current week
    week_list = adjust_date_list(get_week_dates())

    # Removing rows with empty values
    spaceless_array = raw_data[~np.all(raw_data == '', axis=1)]

    # Deleting rows containing 'X' or 'x' for the current week's dates
    mia_list = np.delete(spaceless_array, np.where(
        (spaceless_array[:, week_list[0]:week_list[1]] == 'X') |
        (spaceless_array[:, week_list[0]:week_list[1]] == 'x'))[0], axis=0)

    # Selecting the second column from the remaining rows
    mia_list = mia_list[:, 1]

    # Reshaping the array to a column vector
    mia_list = np.reshape(mia_list, (mia_list.size, 1))

    # Converting the numpy array to a nested list
    mia_list = mia_list.tolist()

    return mia_list


def last_week_list(raw_data):
    """
    This function generates a list of students who were missing in the last week based on the provided raw data.

    Args:
        raw_data (numpy array): The raw data containing the attendance records.

    Returns:
        list: A list of students who did not have a mark ('X' or 'x') for attendance last week.
    """
    # Getting the list of dates for the last week and adjusting them
    last_week = adjust_date_list(get_last_week())

    # Removing rows with empty values
    spaceless_array = raw_data[~np.all(raw_data == '', axis=1)]

    # Deleting rows containing 'X' or 'x' for the last week's dates
    mia_list = np.delete(spaceless_array, np.where(
        (spaceless_array[:, last_week[0]:last_week[1]] == 'X') |
        (spaceless_array[:, last_week[0]:last_week[1]] == 'x'))[0], axis=0)

    # Selecting the second column from the remaining rows
    mia_list = mia_list[:, 1]

    # Reshaping the array to a column vector
    mia_list = np.reshape(mia_list, (mia_list.size, 1))

    # Converting the numpy array to a list
    mia_list = mia_list.tolist()

    return mia_list


def make_month_list(raw_data):
    """
    This function generates a list of students who were missing for the entire month based on the provided raw data.

    Args:
        raw_data (numpy array): The raw data containing the attendance records.

    Returns:
        list: A list of students who did not have a mark ('X' or 'x') for the entire month.
    """
    # Removing rows with empty values
    spaceless_array = raw_data[~np.all(raw_data == '', axis=1)]

    # Removing rows containing 'X' or 'x' in any column
    mia_list = spaceless_array[~np.any((spaceless_array == 'X') | (spaceless_array == 'x'), axis=1)]

    # Selecting the second column from the remaining rows
    mia_list = mia_list[:, 1]

    # Reshaping the array to a column vector
    mia_list = np.reshape(mia_list, (mia_list.size, 1))

    # Converting the numpy array to a list
    mia_list = mia_list.tolist()

    return mia_list


def format_sheet(mia_list_sheet):
    """
    Formats the MIA List sheet by adding column titles and applying formatting.

    Args:
        mia_list_sheet: The Google Sheet object representing the MIA List sheet.

    Returns:
        None
    """
    # Adding column titles to column A, C, and E
    mia_list_sheet.update('C1', 'Current Week')
    mia_list_sheet.update('A1', 'Last Week')
    mia_list_sheet.update('E1', 'Entire Month')

    # Formatting the titles to be bold
    mia_list_sheet.format('A1:E1', {'textFormat': {'bold': True}})


def write_data(mia_list, sh, cell):
    """
    Writes the provided data to the specified cell in the given Google Sheet.

    Args:
        mia_list: The list of data to be written.
        sh: The Google Sheet object where the data will be written.
        cell: The cell address where the data will be written (e.g., 'A1').

    Returns:
        None
    """
    sh.values_update(
        cell,
        params={'valueInputOption': 'RAW'},
        body={'values': mia_list}
    )



def main():
    # Authenticate with Google Sheets
    sa = gspread.service_account()

    # Open the Google Sheet
    sh = sa.open('Test Script')

    # Select the worksheet to extract data from
    worksheet = sh.worksheet('Sheet1')

    # Retrieve the data from the worksheet
    raw_array = np.array(worksheet.get_all_values())

    # Process the data for the current week
    mia_list = cur_week_list(raw_array)

    # Process the data for the last week
    list_last_week = last_week_list(raw_array)

    # Process the data for the entire month
    month_list = make_month_list(raw_array)

    # Clear the destination sheet before writing new data
    sh.values_clear("'MIA List 1'!A1:E1000")

    # Open the destination sheet
    mia_list_sheet = sh.worksheet('MIA List 1')

    # Format the destination sheet
    format_sheet(mia_list_sheet)

    # Write the data for the current week
    write_data(mia_list, sh, 'MIA List 1!C3')

    # Write the data for the last week
    write_data(list_last_week, sh, 'MIA List 1!A3')

    # Write the data for the entire month
    write_data(month_list, sh, 'MIA List 1!E3')


if __name__ == '__main__':
    main()

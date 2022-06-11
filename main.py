# -----------------------------------------------------------
# Creates Google Sheet containing list of MIA students based
# off of master list stored in Google Sheet
#
# (C) 2022 Brandon DiZuzio, Florida, United States of America
# email Bdizuzio@gmail.com
# -----------------------------------------------------------

import gspread
import numpy as np
from date import *
np.set_printoptions(threshold=np.inf)


def cur_week_list(raw_data):
    """
    - The function will parse through the array and remove all rows that are filled with empty space
      is a row filled with ("").

    - The function will then parse through the array and remove all rows that contain an 'X' or 'x'

    - The function will lastly use numpy to get the 2nd item from each row

    :param raw_data: (numpy array): the numpy array that will be parsed through

    :return: A parsed array
    """
    # Making a list containing the first and last day of the week
    week_list = get_week_dates()
    week_list = adjust_date_list(week_list)

    # removing all rows with only ("")
    spaceless_array = raw_data[~np.all(raw_data == '', axis=1)]

    # removing all rows that contain an 'X' or 'x'
    # mia_list = spaceless_array[~np.any((spaceless_array == 'X') | (spaceless_array == 'x'), axis=1)]

    # deleting rows that contain an 'X' or 'x' based on the given range of columns
    mia_list = np.delete(spaceless_array, np.where(
        (spaceless_array[:, week_list[0]:week_list[1]] == 'X') |
        (spaceless_array[:, week_list[0]:week_list[1]] == 'x'))[0], axis=0)

    # using numpy slicing we get the second column of the matrix
    mia_list = mia_list[:, 1]

    # reshaping the list into a 2d array
    mia_list = np.reshape(mia_list, (mia_list.size, 1))

    # making 2d numpy array into list
    mia_list = mia_list.tolist()

    return mia_list


def last_week_list(raw_data):
    """
    - The function will make a list of dates (last monday and sunday)

    - Then will adjust the dates to make them equal to the column values of the MIA LIST

    - Then will pull all mia students for last week and make a new list with those students

    :param raw_data: (numpy array)

    :return: A list of students that did not have a mark ('X' or 'x') for attendance last week
    """
    last_week = get_last_week()
    last_week = adjust_date_list(last_week)

    spaceless_array = raw_data[~np.all(raw_data == '', axis=1)]

    mia_list = np.delete(spaceless_array, np.where(
        (spaceless_array[:, last_week[0]:last_week[1]] == 'X') |
        (spaceless_array[:, last_week[0]:last_week[1]] == 'x'))[0], axis=0)

    mia_list = mia_list[:, 1]

    mia_list = np.reshape(mia_list, (mia_list, 1))

    return mia_list


def format_sheet( mia_list_sheet):
    # Adding a column title to column A and C
    mia_list_sheet.update('C1', 'Current Week')
    mia_list_sheet.update('A1', 'Last Week')

    # Formatting the title to be bold
    mia_list_sheet.format('A1:C1', {'textFormat': {'bold': True}})


def write_cur_week(mia_list, sh):
    # gspread method that updates the Google sheet while only using 1 api call
    # First takes the in the name of the sheet and the starting cell
    # The param is how the data will be input either rows or columns or raw. (raw means the data will be used
    #       as is and will not be parsed)
    # The body is the list that will be inputted into the sheet
    sh.values_update(
        'MIA List 1!C3',
        params={'valueInputOption': 'RAW'},
        body={'values': mia_list}
    )


def write_last_week(mia_list, sh):
    # gspread method that updates the Google sheet while only using 1 api call
    # First takes the in the name of the sheet and the starting cell
    # The param is how the data will be input either rows or columns or raw. (raw means the data will be used
    #       as is and will not be parsed)
    # The body is the list that will be inputted into the sheet
    sh.values_update(
        'MIA List 1!A3',
        params={'valueInputOption': 'RAW'},
        body={'values': mia_list}
    )


def main():
    # Linking the sheets to the code
    sa = gspread.service_account()

    # Opening the file that will be getting worked on
    sh = sa.open('Test Script')

    # Selecting the worksheet that the data will be extracted from
    worksheet = sh.worksheet('Sheet1')

    # getting all values from the mia list and directly turning it into a np array
    raw_array = np.array(worksheet.get_all_values())

    # storing the 2d array returned by list_parsing
    mia_list = cur_week_list(raw_array)

    # clearing the spreadsheet with the given range
    sh.values_clear("'MIA List 1'!A1:C1000")

    # Opening the MIA List sheet
    mia_list_sheet = sh.worksheet('MIA List 1')

    # format and print lists needed
    format_sheet(mia_list_sheet)
    write_cur_week(mia_list, sh)


if __name__ == '__main__':
    main()

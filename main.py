# -----------------------------------------------------------
# Creates Google Sheet containing list of MIA students based
# off of master list stored in Google Sheet
#
# (C) 2022 Brandon DiZuzio, Florida, United States of America
# email Bdizuzio@gmail.com
# -----------------------------------------------------------

import gspread
import numpy as np
np.set_printoptions(threshold=np.inf)


def list_parsing(raw_data, values):
    """

    - The function will parse through the array and remove all rows that are filled with empty space
      is a row filled with ("").

    - The function will then parse through the array and remove all rows that contain an 'X' or 'x'

    - The function will lastly use numpy to get the 2nd item from each row


    :parameter: raw_data (numpy array): the numpy array that will be parsed through


    :return: A parsed array
    """

    starting_range = values[0]
    ending_range = values[1]

    # removing all rows with only ("")
    spaceless_array = raw_data[~np.all(raw_data == '', axis=1)]

    # removing all rows that contain an 'X' or 'x'
    # mia_list = spaceless_array[~np.any((spaceless_array == 'X') | (spaceless_array == 'x'), axis=1)]

    mia_list = np.delete(spaceless_array, np.where(
        (spaceless_array[:, starting_range:ending_range] == 'X') |
        (spaceless_array[:, starting_range:ending_range] == 'x'))[0], axis=0)

    # using numpy library we get the second item from each row and that's all were left with
    mia_list = mia_list[:, 1]

    # reshaping the list into a 2d array
    mia_list = np.reshape(mia_list, (mia_list.size, 1))

    return mia_list


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
    week_one = [6, 11]
    mia_list = list_parsing(raw_array, week_one)

    # making 2d numpy array into list
    mia_list = mia_list.tolist()

    # clearing the spreadsheet with the given range
    sh.values_clear("'MIA List 1'!A1:A1000")

    # gspread method that updates the Google sheet while only using 1 api call
    # First takes the in the name of the sheet and the starting cell
    # The param is how the data will be input either rows or columns or raw. (raw means the data will be used
    #       as is and will not be parsed)
    # The body is the list that will be inputted into the sheet
    sh.values_update(
        'MIA List 1!A1',
        params={'valueInputOption': 'RAW'},
        body={'values': mia_list}
    )


if __name__ == '__main__':
    main()

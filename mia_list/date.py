from datetime import date, timedelta

COLUMN_BUFFER = 6


def get_week_dates():
    """
    - The function will get the date using the datetime module

    - Then get the dates for the week using the timedetla function

    - Lastly make a list with the start and finish dates of the week

    :return: A list consisting of the start and finish day dates for the week
    """
    today = date.today()
    start = today - timedelta(days=today.weekday())
    finish = start + timedelta(days=6)
    date_range = [start.day, finish.day]

    return date_range


def get_last_week():
    """
    - The function get last Monday and Sundays dates

    - Then put them into a list

    :return: a list containing last Monday and Sundays dates.
    """
    today = date.today()
    start = today - timedelta(days=today.weekday()) + timedelta(days=2, weeks=-1)
    finish = start + timedelta(days=6)
    date_range = [start.day, finish.day]

    return date_range


def adjust_date_list(date_range):
    """
    - This function will adjust the date range list so that the range of numbers is aligned with the MIA LIST

    :param date_range: Range of dates (Monday : Sunday)
    :return: An adjusted date range that is accurate with the MIA LIST.
    """

    date_range[0] = date_range[0] + COLUMN_BUFFER
    date_range[1] = date_range[1] + COLUMN_BUFFER

    return date_range


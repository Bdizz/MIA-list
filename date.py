from datetime import date, timedelta


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

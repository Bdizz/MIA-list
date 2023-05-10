from datetime import date, timedelta

COLUMN_BUFFER = 6


def get_week_dates():
    """
    Get the start and finish dates of the current week.

    Returns:
        list: A list containing the start and finish day dates for the week.
    """
    today = date.today()
    start = today - timedelta(days=today.weekday())
    finish = start + timedelta(days=6)
    date_range = [start.day, finish.day]

    return date_range


def get_last_week():
    """
    Get the start and finish dates of the previous week.

    Returns:
        list: A list containing the start and finish day dates of the last week.
    """
    today = date.today()
    start = today - timedelta(days=today.weekday()) + timedelta(days=2, weeks=-1)
    finish = start + timedelta(days=6)
    date_range = [start.day, finish.day]

    return date_range


def adjust_date_list(date_range):
    """
    Adjust the date range list so that the range of numbers is aligned with the MIA LIST.

    Args:
        date_range (list): Range of dates (Monday:Sunday).

    Returns:
        list: An adjusted date range that is accurate with the MIA LIST.
    """
    date_range[0] += COLUMN_BUFFER
    date_range[1] += COLUMN_BUFFER

    return date_range

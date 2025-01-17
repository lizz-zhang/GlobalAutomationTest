from datetime import datetime, timedelta
import pdb
import time


# get current timestamp
def get_current_timestamp():
    return int(round(time.time() * 1000))


# get current utc datetime
def get_current_utc_datetime():
    return datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%S.%fZ")


def get_next_weekday(target_weekday):
    """
    Get the date of the target weekday in next week (target_weekday: 0 = Monday, 1 = Tuesday, ..., 6 = Sunday)
    """
    current_date = datetime.now()
    days_until_target_day = target_weekday - current_date.weekday() + 7
    next_weekday_date = current_date + timedelta(days=days_until_target_day)
    return next_weekday_date.strftime("%Y-%m-%d")


# print(get_next_weekday(0))


def get_start_and_end_time_for_today_search():
    """
    Get the starttime and endtime for today - you can use this for LiveChatHistory search.
    """
    start_time = datetime.now().strftime("%Y-%m-%d") + "T00:00:00+08:00"
    end_time = (datetime.now() + timedelta(days=1)).strftime(
        "%Y-%m-%d"
    ) + "T00:00:00+08:00"

    # pdb.set_trace()
    return start_time, end_time


# print(get_start_and_end_time_for_today_search())


def get_start_and_end_time_for_last_7days_search():
    """
    Get the starttime and endtime for today - you can use this for LiveChatHistory search.
    """
    start_time = (datetime.now() - timedelta(days=7)).strftime(
        "%Y-%m-%d"
    ) + "T00:00:00+08:00"
    end_time = datetime.now().strftime("%Y-%m-%d") + "T00:00:00+08:00"

    # pdb.set_trace()
    return start_time, end_time


# print(get_start_and_end_time_for_today_search())


def get_start_and_end_time_for_day_view():
    """
    Get the starttime and endtime for day view.
    """
    start_time = (datetime.now() - timedelta(days=1)).strftime(
        "%Y-%m-%d"
    ) + "T16:00:00.000Z"
    end_time = datetime.now().strftime("%Y-%m-%d") + "T16:00:00.000Z"

    # pdb.set_trace()
    return start_time, end_time


def get_start_and_end_time_for_day_view_tomorrow():
    """
    Get the starttime and endtime for day view.
    """
    start_time = datetime.now().strftime("%Y-%m-%d") + "T16:00:00.000Z"
    end_time = (datetime.now() + timedelta(days=1)).strftime(
        "%Y-%m-%d"
    ) + "T16:00:00.000Z"

    # pdb.set_trace()
    return start_time, end_time


# get_start_and_end_time_for_day_view()


def get_start_and_end_time_for_week_view():
    """
    Get the starttime and endtime for week view. Please note that Sunday is the first day of the week.
    """
    # get the first day of this week
    first_day_of_this_week = datetime.now() - timedelta(days=datetime.now().weekday())

    first_day_of_week_view = first_day_of_this_week - timedelta(
        days=1
    )  # since Sunday is the first day of the week, we need to add 1

    start_time = (first_day_of_week_view - timedelta(days=1)).strftime(
        "%Y-%m-%d"
    ) + "T16:00:00.000Z"

    last_day_of_week_view = first_day_of_week_view + timedelta(days=6)

    end_time = last_day_of_week_view.strftime("%Y-%m-%d") + "T16:00:00.000Z"

    # pdb.set_trace()
    return start_time, end_time


# get_start_and_end_time_for_week_view()


def get_start_and_end_time_for_month_view():
    """
    Get the starttime and endtime for month view. Please note that Sunday is the first day of the week.
    """

    # get the first day of this month
    first_day_of_this_month = datetime.now().replace(day=1)
    # get the weekday of the first day of this month
    first_day_of_this_month_weekday = first_day_of_this_month.weekday()

    first_day_of_month_view = first_day_of_this_month - timedelta(
        first_day_of_this_month_weekday + 1
    )  # since Sunday is the first day of the week, we need to add 1

    start_time = (first_day_of_month_view - timedelta(days=1)).strftime(
        "%Y-%m-%d"
    ) + "T16:00:00.000Z"

    last_day_of_month_view = first_day_of_month_view + timedelta(days=41)

    end_time = last_day_of_month_view.strftime("%Y-%m-%d") + "T16:00:00.000Z"

    # pdb.set_trace()
    return start_time, end_time

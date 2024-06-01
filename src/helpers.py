import re
from datetime import datetime, timedelta

from dateutil.relativedelta import relativedelta

from src.constants import CATEGORIES, PLANS, TOPUPS
from src.enums import ECommands


def is_command_valid(command: str) -> bool:
    """Checks if the entered command is valid or not

    Args:
        command (str): command to check

    Returns:
        bool: Is command valid or not
    """
    return ECommands.has_command(command)


def is_category_valid(category: str):
    return category in CATEGORIES


def is_plan_valid(plan: str):
    return plan in PLANS


def is_date_valid(date: str):
    pattern = re.compile(r'\d{2}-\d{2}-\d{4}')
    match = pattern.match(date)

    if match:
        date_split = date.split('-')
        # validate day
        if int(date_split[0]) > 31 or int(date_split[0]) < 1:
            return False
        if int(date_split[1]) > 12 or int(date_split[1]) < 1:
            return False
        return True

    return False


def is_topup_valid(topup: str):
    return topup in TOPUPS


def increment_and_subtract_date(date_str: str, months: int, subtract_days: int):
    """
    Function to increment date by months and subtract subtract_days days
    """
    # Parse the date string
    date_format = "%d-%m-%Y"
    original_date = datetime.strptime(date_str, date_format)

    # Increment by the specified number of months
    incremented_date = original_date + relativedelta(months=months)

    # Subtract 10 days
    final_date = incremented_date - timedelta(days=subtract_days)

    # Format the final date back to string
    final_date_str = final_date.strftime(date_format)

    return final_date_str


def read_file(filepath):
    with open(filepath, 'r') as f:
        contents = f.readlines()
    return contents

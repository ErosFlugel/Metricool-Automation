import calendar
from datetime import datetime, timedelta

#Global current Date
CURRENT_DATE = datetime.now().replace(hour=23, minute=59, second=59, microsecond=0)

def get_range_iso_date(start, end=CURRENT_DATE):

    # Format date -> ISO for last 4 weeks
    date_start = start.isoformat() + "+00:00"
    date_end = end.isoformat() + "+00:00"

    return (date_start, date_end)

def get_monthly_range_date(month):
    #Global date same time
    current_date = datetime.now().replace(hour=23, minute=59, second=59, microsecond=0)

    #To check if the operation is made the final day of the month (it should be available)
    final_day_month = not ((current_date + timedelta(days=1)).month == current_date.month)

    #Date range if the operation is in the current year
    if (final_day_month and current_date.month == month) or (current_date.month > month):

        starting_date = current_date.replace(day=1, month=month)

        _, num_days = calendar.monthrange(current_date.year, month)
        ending_date = current_date.replace(day=num_days, month=month)

    #Date range for previous months
    else:
        starting_date = current_date.replace(day=1, month=month, year=(current_date.year - 1))

        _, num_days = calendar.monthrange(current_date.year - 1, month)
        ending_date = current_date.replace(day=num_days, month=month, year=(current_date.year - 1))

    # Return formated date ranges
    return get_range_iso_date(starting_date, ending_date)
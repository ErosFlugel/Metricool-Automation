from datetime import datetime

#Global current Date
CURRENT_DATE = datetime.now().replace(hour=23, minute=59, second=59, microsecond=0)

def get_range_iso_date(start, end=CURRENT_DATE):

    # Format date -> ISO for last 4 weeks
    date_start = start.isoformat() + "+00:00"
    date_end = end.isoformat() + "+00:00"

    return (date_start, date_end)
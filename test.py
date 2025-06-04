
from datetime import datetime

from matplotlib.dates import relativedelta

def format_time(time: any):
    if isinstance(time, str):
        dt = datetime.fromisoformat(time)
        return dt.strftime('%Y-%m-%d %H:%M:%S')
    elif isinstance(time, datetime):
        return time.strftime('%Y-%m-%d %H:%M:%S')
    else:
        return "start_time is None or unknown type"


if __name__ == "__main__":
    print(format_time(datetime(2025, 5, 28, 16, 48, 58)))
    print(format_time(datetime.now()))
    print(format_time(None))
    print(format_time(123))
    print(format_time("2024-01-01 00:00:00"))

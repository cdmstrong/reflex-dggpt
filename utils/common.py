
from datetime import datetime

def format_time(time: any):
    if isinstance(time, str):
        dt = datetime.fromisoformat(time)
        return dt.strftime('%Y-%m-%d %H:%M:%S')
    elif isinstance(time, datetime):
        return time.strftime('%Y-%m-%d %H:%M:%S')
    else:
        return "start_time is None or unknown type"



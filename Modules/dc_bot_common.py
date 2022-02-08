import time
import json
from datetime import datetime

# UTC + 1h
timezone = 3600

def now() -> str:
    return datetime.fromtimestamp(int(time.time()) + timezone).strftime("%a, %d %b %Y %H:%M:%S")

def log_error(error_msg, errlog_file):
    with open(errlog_file, "a") as error_logs:
        error_logs.write(now() + " => " + str(error_msg) + "\n")

def format_time_at(when):
    return datetime.fromtimestamp(when + timezone).strftime('at %H:%M on %d. %m. %Y')
    
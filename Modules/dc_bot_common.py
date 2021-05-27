import time
import json

def now():
    return time.strftime("%a, %d %b %Y %H:%M:%S")

def log_error(error_msg):
    with open("error.log", "a") as error_logs:
        error_logs.write(now() + " => " + str(error_msg) + "\n")

from dc_bot_imports import *

def log_error(error_msg):
    with open("error.log", "a") as error_logs:
        error_logs.write(time.strftime("%a, %d %b %Y %H:%M:%S") + " => " + str(error_msg) + "\n")
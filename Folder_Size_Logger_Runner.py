import time as t
import json
import datetime

with open("config.json", "r") as file:
    config = json.loads(file.read())

time_of_day = config["time_of_day"]
one_day_in_seconds = datetime.timedelta(days=1).total_seconds()

while True:
    now = datetime.datetime.now()
    time_to_run_today = datetime.datetime(now.year, now.month, now.day, time_of_day["hour"], time_of_day["minute"], 0)
    time_difference = time_to_run_today.timestamp() - now.timestamp()

    print("waiting until {}:{}...".format(time_of_day["hour"], time_of_day["minute"]), end="\r")
    # sleep until it's time to run again
    # if the time difference is negative it's because we passed the time today already,
    # and we add 24 hours so that it runs the next day
    if time_difference > 0:
        t.sleep(time_difference)
    else:
        t.sleep(time_difference+one_day_in_seconds)
    # once it's time, run the program
    exec(open("Folder_Size_Logger_V4.py", "r").read()) # run the logger

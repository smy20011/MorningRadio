import schedule
import time
import os


def make():
    os.system("make")


schedule.every().day.at("07:30").do(make)

while True:
    schedule.run_pending()
    time.sleep(1)

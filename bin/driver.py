import datetime
import sched
from collections import namedtuple
from configparser import ConfigParser
from sys import argv
from time import sleep, time

import pyautogui
import pytz
from selenium import webdriver


def register():

    conf = ConfigParser()
    conf.read("./.config")
    url = conf["DEFAULT"]["url"]
    print(url)
    driver = webdriver.Chrome()
    driver.get(url)
    driver.maximize_window()

    print(pyautogui.size())
    print(pyautogui.position())

    Point = namedtuple("Point", ["x", "y"])

    class TimeSlot:
        def __init__(self, x, y):
            self.slot = Point(x, y)
            self.register_slot = Point(x + 75, y + 95)

    if len(argv) != 2:
        exit(1, "Not enough args")

    if argv[1] == "swim":
        elem = driver.find_element_by_id("btnPersonalTraining")
        elem.click()
        sleep(3)
        elem2 = driver.find_element_by_id("phNetworkScheduleControl1_btnDepartment3")
        elem2.click()
        sleep(3)
        print(dir(driver))
    elif argv[1] == "ball":
        elem = driver.find_element_by_id("btnRacquetSportsBookCourt")
        elem.click()
        sleep(3)
        elem2 = driver.find_element_by_id("phNetworkScheduleControl1_btnDepartment2")
        elem2.click()
        sleep(3)
    else:
        exit(1, "Unsupported mode")

    next_page = True
    if next_page:
        pyautogui.moveTo(1393, 347)
        pyautogui.click()
        sleep(2)

    # slot = TimeSlot(1625, 735)
    slot = TimeSlot(875, 916)
    sleep(2)
    pyautogui.moveTo(*slot.slot)
    pyautogui.click()
    sleep(2)
    pyautogui.moveTo(*slot.register_slot)
    pyautogui.click()

    explore = False
    while explore:
        print(pyautogui.position())

    sleep(5)
    driver.close()
    exit(0)


if __name__ == "__main__":
    est = pytz.timezone("US/Eastern")
    dt = datetime.datetime(2021, 3, 5, 13, 59, 52)

    aware = est.localize(dt)

    print(dt)
    print(aware)
    print(dt.timestamp())
    print(aware.timestamp())
    s = sched.scheduler(time, sleep)
    delay = aware.timestamp() - time()
    dry_run = True
    if dry_run:
        delay = 2

    s.enter(delay, 1, register)
    s.run()
    register()

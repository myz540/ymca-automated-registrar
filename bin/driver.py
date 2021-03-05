#!/usr/bin/env python

import datetime
import sched
from configparser import ConfigParser
from time import sleep, time
import argparse

import pyautogui
import pytz
from selenium import webdriver

from ymca_automated_registrar import core


def register(url: str, event: str, timeslot: core.TimeSlot, explore: bool):

    print(url)
    # instantiate driver and go the landing page
    driver = webdriver.Chrome()
    driver.get(url)
    driver.maximize_window()

    # if exploring, keep printing out mouse position
    while explore:
        print(pyautogui.position())

    # navigate to the event
    core.navigate_to_event(event=event, driver=driver, delay=3)

    # if the timeslot is on a sunday or monday, registration will be on the next page
    if timeslot.weekday() in [6, 0]:
        core.navigate_to_next_page()

    core.move_and_click(timeslot.slot)
    core.move_and_click(timeslot.register_slot)

    explore = False
    while explore:
        print(pyautogui.position())

    sleep(5)
    driver.close()
    exit(0)


if __name__ == "__main__":

    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-e", "--event", choices=["swim", "ball"], help="event to register for"
    )
    parser.add_argument(
        "-s",
        "--slot-pos",
        nargs=2,
        type=float,
        help="mouse position (x, y) of the time slot",
    )
    parser.add_argument(
        "-t", "--time", help="datetime string for the time slot to register"
    )
    parser.add_argument(
        "--explore", action="store_true", help="use this mode to identify slot pos"
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="use this mode to dry-run the scripted registration",
    )
    parser.add_argument("--debug", action="store_true")
    parser.add_argument("--verbose", action="store_true")

    args = parser.parse_args()

    print(args)

    # get the event from the registry of supported events
    event = core.event_registry.get(args.event)

    # read conf file to get URL
    conf = ConfigParser()
    conf.read("./.config")
    url = conf["DEFAULT"]["url"]

    # assume EST
    tz = pytz.timezone("US/Eastern")
    # try to parse the provided date time string
    dt = datetime.datetime.strptime(args.time, "%Y-%m-%d %H:%M:%S")

    # make timeslot from pos
    timeslot = core.TimeSlot(x=args.slot_pos[0], y=args.slot_pos[1], dt=dt)

    print(dt)
    aware_dt = tz.localize(dt)

    exit(0)

    s = sched.scheduler(time, sleep)
    delay = 2 if args.dry_run else aware_dt.timestamp() - time()
    s.enter(
        delay,
        1,
        register,
        kwargs={
            "url": url,
            "event": event,
            "timeslot": timeslot,
            "explore": args.explore,
        },
    )
    s.run()

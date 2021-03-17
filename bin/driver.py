#!/usr/bin/env python

import argparse
import datetime
import sched
from configparser import ConfigParser
from pathlib import Path
from time import sleep, time

import pyautogui
import pytz
from selenium import webdriver
from ymca_automated_registrar import core


def prepare_registration(
    event: core.Event,
    timeslot: core.TimeSlot,
    conf: ConfigParser,
    driver: webdriver.chrome.webdriver.WebDriver,
):
    url = conf["DEFAULT"]["url"]
    user = conf["DEFAULT"]["user"]
    password = conf["DEFAULT"]["password"]

    # get URL, max windowo, and go the landing page
    driver.get(url)
    driver.maximize_window()

    print("Logging in...")
    print(url, user, "*" * len(password))
    core.login(user=user, password=password, driver=driver, delay=2)

    # navigate to the event
    print("Navigating to main event...")
    core.navigate_to_event(event=event.main_event_link, driver=driver, delay=3)

    # if the timeslot is on a sunday or monday, registration will be on the next page
    if timeslot.weekday in [6, 0]:
        print("Next page...")
        core.navigate_to_next_page()


def register(
    event: core.Event,
    timeslot: core.TimeSlot,
    explore: bool,
    driver: webdriver.chrome.webdriver.WebDriver,
    scroll: bool,
):
    print("Navigating to sub-event...")
    core.navigate_to_event(event=event.sub_event_link, driver=driver, delay=3)

    if scroll:
        print("Scrolling to bottom...")
        core.scroll_to_bottom()

    print("Registering for time slot...")
    core.move_and_click(point=timeslot.slot, delay=1)
    core.move_and_click(point=timeslot.register_slot, delay=1)

    # if exploring, keep printing out mouse position
    while explore:
        try:
            print(pyautogui.position())
            sleep(1)
        except KeyboardInterrupt:
            break

    sleep(5)
    driver.close()
    driver.quit()
    exit(0)


def custom_wait(x):
    print(f"Waiting...{x:.2f}")
    sleep(x)


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
        help="mouse position (x, y) of the time slot. This is the position of the time slot you want to register",
    )
    parser.add_argument(
        "-t",
        "--time",
        help="datetime string for the time slot to register. This is used to schedule the registration and corresponds "
        "to the time that the registration opens",
    )
    parser.add_argument(
        "--explore", action="store_true", help="use this mode to identify slot pos"
    )
    parser.add_argument(
        "--scroll",
        action="store_true",
        help="sometimes the timeslot is at the bottom of the page and you need to scroll to register",
    )
    parser.add_argument(
        "--dryrun",
        action="store_true",
        help="use this mode to dry-run the scripted registration",
    )
    parser.add_argument("--debug", action="store_true")
    parser.add_argument("--verbose", action="store_true")

    args = parser.parse_args()

    print(args)

    # instantiate driver to pass around
    driver = webdriver.Chrome()

    # get the event from the registry of supported events
    event = core.event_registry.get(args.event)

    # read conf file to get URL
    conf = ConfigParser()
    conf_file = Path(__file__).parents[1] / ".config"
    conf.read(conf_file)
    url = conf["DEFAULT"]["url"]

    # assume EST
    tz = pytz.timezone("US/Eastern")
    # try to parse the provided date time string
    if args.time:
        dt = datetime.datetime.strptime(args.time, "%Y-%m-%d %H:%M:%S")
    else:
        dt = datetime.datetime.now()

    # make timeslot from pos
    if args.slot_pos:
        timeslot = core.TimeSlot(x=args.slot_pos[0], y=args.slot_pos[1], dt=dt)
    else:
        timeslot = core.TimeSlot(x=100, y=100, dt=dt)

    print(dt)
    aware_dt = tz.localize(dt)

    s = sched.scheduler(time, custom_wait)
    if args.dryrun:
        # delay between launch and prepare()
        init_delay = 5
        # delay between launch and register()
        registration_delay = 20
    else:
        init_delay = aware_dt.timestamp() - time() - 20
        registration_delay = aware_dt.timestamp() - time()

    s.enter(
        init_delay,
        1,
        prepare_registration,
        kwargs={"event": event, "timeslot": timeslot, "conf": conf, "driver": driver},
    )
    s.enter(
        registration_delay,
        2,
        register,
        kwargs={
            "event": event,
            "timeslot": timeslot,
            "explore": args.explore,
            "driver": driver,
            "scroll": args.scroll
        },
    )
    s.run()

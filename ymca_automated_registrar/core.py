from datetime import datetime
from selenium import webdriver
from typing import NamedTuple, Optional
from time import sleep
import pyautogui

class Event(NamedTuple):
    event: str
    main_event_link: str
    sub_event_link: str


swim = Event(
    event="swim",
    main_event_link="btnPersonalTraining",
    sub_event_link="phNetworkScheduleControl1_btnDepartment3",
)

ball = Event(
    event="ball",
    main_event_link="btnRacquetSportsBookCourt",
    sub_event_link="phNetworkScheduleControl1_btnDepartment2",
)


event_registry = {
    swim.event: swim,
    ball.event: ball,
}


class Point(NamedTuple):
    x: float
    y: float


class TimeSlot:
    def __init__(self, x: float, y: float, dt: datetime):
        self.slot = Point(x, y)
        self.register_slot = Point(x + 75, y + 95)
        self.dt = dt
        self.weekday = dt.weekday()


def navigate_to_event(
    event: Event,
    driver: webdriver.chrome.webdriver.WebDriver,
    delay: int = 0,
) -> None:

    if not delay:
        delay = 0

    elem = driver.find_element_by_id(event.main_event_link)
    elem.click()
    sleep(delay)
    elem2 = driver.find_element_by_id(event.sub_event_link)
    elem2.click()
    sleep(delay)


def navigate_to_next_page():
    pyautogui.moveTo(1393, 347)
    pyautogui.click()
    sleep(2)


def move_and_click(point: Point, delay: int = 0):
    pyautogui.moveTo(point)
    pyautogui.click()
    sleep(delay)


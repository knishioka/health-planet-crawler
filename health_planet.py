import argparse
import datetime
import os
import time
from datetime import timedelta

import pandas as pd
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.firefox.webdriver import WebDriver


def main(start_date: datetime.date, end_date: datetime.date) -> pd.DataFrame:
    logged_in_driver = login()

    health_data = {}
    for i in range((end_date - start_date).days + 1):
        health_data[(start_date + timedelta(i)).strftime("%Y/%m/%d")] = get_health_data(
            logged_in_driver, created_on=(start_date + timedelta(i)).strftime("%Y%m%d")
        )
    pd.DataFrame.from_dict(health_data, orient="index").to_csv(f"health_data_{start_date}-{end_date}.csv")


def login() -> WebDriver:
    options = Options()
    options.add_argument("-headless")
    driver = webdriver.Firefox(options=options)
    driver.get("https://www.healthplanet.jp/en/login.do")
    time.sleep(0.5)
    driver.find_element_by_name("loginId").send_keys(os.environ["HEALTH_PLANET_ID"])
    driver.find_element_by_name("passwd").send_keys(os.environ["HEALTH_PLANET_PASSWORD"])
    driver.find_element_by_id("btnSet").click()
    return driver


def get_health_data(logged_in_driver: WebDriver, created_on: str) -> dict:
    """Get scanned health data.

    Args:
        logged_in_driver: Logged in selenium driver.
        created_on:

    Returns:
        dict: Health data (e.g. Weight, Body Fat, etc.)

    """
    logged_in_driver.get(f"https://www.healthplanet.jp/en/innerscan.do?date={created_on}")
    soup = BeautifulSoup(logged_in_driver.page_source, "html.parser")
    if data_table := soup.find("div", {"id": "inputdata_area"}):
        return {e.find("th").text.strip(): e.find("td").text.split()[0] for e in data_table.find_all("tr")}
    else:
        return {}


def date_type(date_str: str) -> datetime.date:
    """Convert date string to date object.

    Args:
        date_str: Date string.

    Returns:
        datetime.date
    """
    return datetime.date.fromisoformat(date_str)


if __name__ == "__main__":
    arg_parser = argparse.ArgumentParser()
    arg_parser.add_argument(
        "-s", "--start-date", help="Start date must be in ISO format. For example: 2020-01-01.", type=date_type
    )
    arg_parser.add_argument(
        "-e", "--end-date", help="End date must be in ISO format. For example: 2020-01-01.", type=date_type
    )
    args = arg_parser.parse_args()
    main(start_date=args.start_date, end_date=args.end_date)

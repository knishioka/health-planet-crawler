import os

from selenium import webdriver
from selenium.webdriver.firefox.webdriver import WebDriver
from bs4 import BeautifulSoup


def main() -> dict:
    logged_in_driver = login()
    logged_on = "20210901"
    return {logged_on: get_health_data(logged_in_driver, logged_on)}


def login() -> WebDriver:
    driver = webdriver.Firefox()
    driver.get("https://www.healthplanet.jp/en/login.do")
    driver.find_element_by_name("loginId").send_keys(os.environ["HEALTH_PLANET_ID"])
    driver.find_element_by_name("passwd").send_keys(
        os.environ["HEALTH_PLANET_PASSWORD"]
    )
    driver.find_element_by_id("btnSet").click()
    return driver


def get_health_data(logged_in_driver: WebDriver, logged_on: str) -> dict:
    logged_in_driver.get(
        f"https://www.healthplanet.jp/en/innerscan.do?date={logged_on}"
    )
    soup = BeautifulSoup(logged_in_driver.page_source, "html.parser")
    return {
        e.find("th").text.strip(): e.find("td").text.split()[0]
        for e in soup.find("div", {"id": "inputdata_area"}).find_all("tr")
    }


if __name__ == "__main__":
    print(main())

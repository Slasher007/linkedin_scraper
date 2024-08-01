import os
from linkedin_scraper import actions
from driver_setup import setup_driver
import time
import pandas as pd

linked_user = "xorover503@qodiq.com"


def scroll_to_bottom(driver):

    # Initial page height
    last_height = driver.execute_script("return document.body.scrollHeight")

    while True:
        # Scroll down to the bottom of the page
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

        # Wait for the page to load
        time.sleep(2)  # Adjust time depending on the page load time

        # Calculate new page height
        new_height = driver.execute_script("return document.body.scrollHeight")

        # Check if we've reached the bottom of the page
        if new_height == last_height:
            break  # Break the loop if height hasn't changed

        last_height = new_height  # Update the last height to the new height


def get_company_people_details(driver, company_url):
    driver.get(f"{company_url}/people")
    time.sleep(3)

    # Scroll to bottom
    scroll_to_bottom(driver)


if __name__ == "__main__":
    driver = setup_driver()

    email = os.getenv("LINKEDIN_USER")
    password = os.getenv("LINKEDIN_PASSWORD")

    # Load company list
    df_companies = pd.read_csv('company.csv')

    # Login LinkedIn
    actions.login(driver, email, password)

    for index, row in df_companies.iterrows():
        time.sleep(5)
        get_company_people_details(driver, row['linked_url'])

from linkedin_scraper import actions
from driver_setup import setup_driver
import time
import pandas as pd
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys


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


def accept_cookies(driver):

    # find all buttons
    buttons = driver.find_elements(By.TAG_NAME, 'button')

    # Check button where text is "Tout accepter"
    for button in buttons:
        button_text = button.text
        button_text = button_text.lower()
        if 'accepter' in button_text:
            button.click()
            break


def search_company_employees(driver, company_name):
    # Send keys in search bar "{company_name} LinkedIn employees"
    search_bar = driver.find_element(By.XPATH, '//textarea[@title="Rechercher"]')
    search_bar.send_keys(f"{company_name} linkedin employees", Keys.ENTER)


def get_google_search_results(driver):
    all_a_tag = driver.find_elements(By.TAG_NAME, 'a')

    hrefs = []
    for a_tag in all_a_tag:
        href = a_tag.get_attribute('href')
        if href and (('/in/' in href) or ('/post/' in href)):
            print(href)
            hrefs.append(href)

    return hrefs


def click_next_page(driver):
    next_button = driver.find_element(By.ID, "pnnext")
    next_button.click()


if __name__ == "__main__":
    # Setup driver
    driver = setup_driver()

    # Load company list
    df_companies = pd.read_csv('company.csv')

    # Go in google search
    driver.get('https://www.google.com')
    time.sleep(3)

    # Accept cookies
    accept_cookies(driver)
    time.sleep(2)

    page = 1
    page_limit = 10
    for index, row in df_companies.iterrows():

        # Search company employees on Google
        search_company_employees(driver, row['name'])
        time.sleep(2)

        while page <= page_limit:
            print(f"------------------Page:{page}----------------------")
            # Get page search results
            search_results = get_google_search_results(driver)
            print(f"Result found: {len(search_results)}")
            time.sleep(3)

            # Click next page
            click_next_page(driver)
            page = page + 1
            time.sleep(4)

    # Login LinkedIn
    #actions.login(driver)

    #for index, row in df_companies.iterrows():

    #    time.sleep(5)
    #    get_company_people_details(driver, row['linked_url'])

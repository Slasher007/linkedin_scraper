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
        if href and (('/in/' in href) or ('/posts/' in href)):
            print(href)
            hrefs.append(href)

    return hrefs


def click_next_page(driver):
    next_button = driver.find_element(By.ID, "pnnext")
    next_button.click()


def close_contextual_signin_modal_screen(driver):

    # Select modal screen
    modal_screen = driver.find_element(By.XPATH, '//section[@aria-modal="true"]')

    if modal_screen:
        # Select all buttons in modal_screen
        all_buttons = modal_screen.find_elements(By.TAG_NAME, 'button')

        # Select button where "dismiss" in class attribute
        for button in all_buttons:
            button_class_value = button.get_attribute('class')
            if 'dismiss' in button_class_value:
                button.click()
                break

    else:
        print("No contextual signin modal screen")


if __name__ == "__main__":
    # Setup driver
    driver = setup_driver()

    #driver.get("https://fr.linkedin.com/posts/simon-berthou-baa338a8_hydrog%C3%A8ne-activity-7110899789700939777-afsy")
    #time.sleep(3)
    #close_contextual_signin_modal_screen(driver)

    # Load company list
    df_companies = pd.read_csv('company.csv')

    for index, row in df_companies.iterrows():
        page = 1
        page_limit = 10

        # Go in google search
        driver.get('https://www.google.com')
        time.sleep(3)

        # Accept cookies
        try:
            accept_cookies(driver)
            time.sleep(2)
        except:
            pass

        print(f"######### {row['name'].upper()} #############")
        # Search company employees on Google
        search_company_employees(driver, row['name'])
        time.sleep(2)

        while page <= page_limit:
            print(f"------------------Page {page}----------------------")
            # Get page search results
            search_results = get_google_search_results(driver)
            print(f"Results found: {len(search_results)}")
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

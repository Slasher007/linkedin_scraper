import os
from driver_setup import setup_driver
import pandas as pd
import time
from linkedin_scraper.actions import login

linked_user = "xorover503@qodiq.com"


def get_company_people_details(driver, company_url):
    time.sleep(2)
    driver.get(f"{company_url}/people")


if __name__ == "__main__":
    # Setup credentials
    email = os.getenv("LINKEDIN_USER")
    password = os.getenv("LINKEDIN_PASSWORD")

    # Load company list
    companies = pd.read_csv('company.csv')

    # Setup driver
    driver = setup_driver()
    driver.get('google.com')

    # Login LinkedIn
    #driver = login(driver=driver, email=email, password=password, cookie=None)

    # Get company people
    #for company in companies:
        #get_company_people_details(driver, company)
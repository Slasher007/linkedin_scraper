import os
from linkedin_scraper import Person, actions
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from driver_setup import setup_driver

email = os.getenv("LINKEDIN_USER")
password = os.getenv("LINKEDIN_PASSWORD")

driver = setup_driver()
actions.login(driver, email, password) # if email and password isnt given, it'll prompt in terminal
person = Person("https://www.linkedin.com/in/adrian0350", contacts=[], driver=driver)

print("Person: " + person.name)
print("Person contacts: ")

for contact in person.contacts:
	print("Contact: " + contact.name + " - " + contact.occupation + " -> " + contact.url)

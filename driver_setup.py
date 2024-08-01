from selenium import webdriver
from selenium.webdriver.chrome.options import Options


def setup_driver():

    options = Options()
    options.add_experimental_option("detach", True)
    options.add_argument("--start-maximized")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--disable-gpu")
    options.add_argument("--remote-debugging-port=9222")

    options.binary_location = 'C:/Program Files/BraveSoftware/Brave-Browser/Application/brave.exe'  # Set the path to your custom Chrome binary
    driver = webdriver.Chrome(options=options)
    driver.maximize_window()

    return driver
import os
import time

from dotenv import load_dotenv
from selenium import webdriver
from selenium.common import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

load_dotenv()

class InternetSpeedBot:
    def __init__(self, down, up):
        self.email = os.environ.get('Y_EMAIL')
        self.password = os.environ.get('Y_PASSWORD')
        self.url = os.environ.get('Y_LOGIN_URL')
        self.down = down
        self.up = up
        self.driver = webdriver.Chrome()
        self.wait = WebDriverWait(self.driver, 10)

    def login(self):
        try:
            self.driver.get(self.url)

            email_input = self.wait.until(EC.element_to_be_clickable((By.NAME, "email")))
            email_input.send_keys(self.email)
            password_input = self.wait.until(EC.element_to_be_clickable((By.NAME, "password")))
            password_input.send_keys(self.password)

            submit_btn = self.wait.until(EC.element_to_be_clickable((By.CLASS_NAME, "y-login-submit")))
            submit_btn.click()

            self.wait.until(EC.visibility_of_element_located((By.CLASS_NAME, "x-sidebar-logo")))
            print("Login Successful")
        except TimeoutException:
            print("Login Failed")

    def get_internet_speed(self):
        pass

    def tweet_at_provider(self):
        pass


promised_down = os.environ.get('PROMISED_DOWN')
promised_up = os.environ.get('PROMISED_UP')

try:
    bot = InternetSpeedBot(down=promised_down, up=promised_up)
    bot.login()

    time.sleep(10)
finally:
    bot.driver.quit()

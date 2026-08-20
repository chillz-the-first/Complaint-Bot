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
        self.down = float(down)
        self.up = float(up)
        self.driver = webdriver.Chrome()
        self.wait = WebDriverWait(self.driver, 10)

    def login(self):
        try:
            print('Logging in...')
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
        try:
            print('Getting Internet Speed...')
            self.driver.get(os.environ.get("TEST_URL"))

            start_btn = self.wait.until(EC.element_to_be_clickable(
                (By.XPATH, '//*[@id="root"]/div/div[1]/div/div[2]/div[2]/div[2]/div/div/div[2]/div[2]/button')
            ))
            start_btn.click()

            long_wait = WebDriverWait(self.driver, 60)
            results = long_wait.until(EC.visibility_of_element_located(
                (By.XPATH, '//*[@id="root"]/div/div[1]/div/div[2]/div[2]/div[2]/div/div/div/div[1]/p')
            ))

            download = long_wait.until(EC.visibility_of_element_located(
                (By.XPATH,
                 '//*[@id="root"]/div/div[1]/div/div[2]/div[2]/div[2]/div/div/div/div[2]/div[2]/div[1]/div[1]/div/h3')
            )).text
            download = float(download)
            download = float(download)
            upload = long_wait.until(EC.visibility_of_element_located(
                (By.XPATH,
                 '//*[@id="root"]/div/div[1]/div/div[2]/div[2]/div[2]/div/div/div/div[2]/div[2]/div[1]/div[2]/div/h3')
            )).text
            upload = float(upload)

            print(f"Internet Speed: {download} / {upload}")
            return download, upload
        except TimeoutException:
            print("Speed test failed")

    def tweet_at_provider(self, d_speed, u_speed):
        print("Tweeting at provider")
        if self.down > d_speed or self.up > u_speed:
            msg = (f"Hey @vodacom, why is my internet speed {d_speed}Mbps down/{u_speed}Mbps up"
                   f"when I pay for {self.down}Mbps down/{self.up}Mbps up")

            post = self.wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@id="tweet-compose"]')))
            post.send_keys(msg)

            self.wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@id="post-btn"]'))).click()
            print("Tweet posted")


promised_down = os.environ.get('PROMISED_DOWN')
promised_up = os.environ.get('PROMISED_UP')

try:
    bot = InternetSpeedBot(down=promised_down, up=promised_up)
    d_load, u_load = bot.get_internet_speed()
    bot.login()
    bot.tweet_at_provider(d_speed=d_load, u_speed=u_load)
    time.sleep(20)
finally:
    bot.driver.quit()

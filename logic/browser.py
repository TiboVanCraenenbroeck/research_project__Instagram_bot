import logging
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import sys
import os
from time import sleep
import numpy as np

PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))
BASE_DIR = os.path.dirname(PROJECT_ROOT)
sys.path.insert(0, BASE_DIR)

from secrets_bot import Secrets

class Browser:
    def __init__(self, login: bool = -1):
        self.webdriver = webdriver.Chrome(
            executable_path="C:/Users/Tibovc/Desktop/MCT/research_project/code/chromedriver.exe")

        if login >= 0:
            self.login(login)

    def login(self, account_nr: int):
        self.webdriver.get("https://instagram.com")
        sleep(np.random.uniform(0.1, 2))
        self.webdriver.find_element_by_xpath(
            "/html/body/div[2]/div/div/div/div[2]/button[1]").click()
        sleep(np.random.uniform(0.1, 2))

        input_username = self.webdriver.find_element_by_xpath(
            '//*[@id="loginForm"]/div/div[1]/div/label/input')
        input_username.send_keys(Secrets.login[account_nr]["email"])

        sleep(np.random.uniform(0.1, 2))
        input_password = self.webdriver.find_element_by_xpath(
            '//*[@id="loginForm"]/div/div[2]/div/label/input')
        input_password.send_keys(Secrets.login[account_nr]["password"])
        sleep(np.random.uniform(0.1, 2))

        input_password.send_keys(Keys.ENTER)

        sleep(np.random.uniform(1, 3))

        try:
            self.webdriver.find_element_by_xpath(
                '//*[@id="react-root"]/section/main/div/div/div/div/button').click()
        except Exception as e:
            logging.error(e)
        sleep(np.random.uniform(1, 3))
        try:
            self.webdriver.find_element_by_xpath(
                '/html/body/div[4]/div/div/div/div[3]/button[2]').click()
        except Exception as e:
            logging.error(e)
    
    def browser_close(self):
        self.webdriver.quit()
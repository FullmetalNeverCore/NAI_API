import sys,time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By


class TheEndOfNAI():
    def CALL_DESTRUCTOR(driver):
        driver.quit()
        
class DefaultConfig(Exception):
    pass
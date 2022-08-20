from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from config import email,password
from excep import DefaultConfig
import time



class SystemManipulation:
    def __init__():
        if email == "test@gmail.com" or password == "test":raise DefaultConfig("Add your email or password in config.py file.")

    def auth(driver,url : str):
        driver.get(url)
        print("Loggining in...")
        time.sleep(15) # page initial load
        WebDriverWait(driver, 40).until(EC.presence_of_element_located((By.XPATH, "//input[@type='email']"))).send_keys(email + Keys.RETURN)
        WebDriverWait(driver, 40).until(EC.presence_of_element_located((By.XPATH, "//input[@type='password']"))).send_keys(password + Keys.RETURN)
        WebDriverWait(driver,100).until(lambda x: driver.title == "Stories - NovelAI")
        print("Ready!/Searching for stories!")

    def find_stories(driver):
        try:stories = [x.get_attribute("aria-label") for x in driver.find_elements_by_xpath("//*[@class='sc-7760eb68-22 cTmnLL sidebar-story-card']")]
        except Exception as e: 
            print("The exeption occured,probably this story is not exist in your story list,try again.")
            return False 
        return stories

    def button_interaction(driver,label,btnname : str):
        try:WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.XPATH, f"//*[@{label}='{btnname}']"))).click()
        except Exception as e: 
            return False 
        return True


class StoryManipulation:
    def send_input(driver,inp : list):
        for x in range(len(inp)):
                if x != (len(inp)-1):
                    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, "//textarea[@placeholder='Write your input here']"))).send_keys(inp[x] + Keys.RETURN)
                    WebDriverWait(driver,20).until(EC.presence_of_element_located((By.XPATH,"//button[@aria-label='Undo' and not (@disabled)]"))).click()
                else:
                    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, "//textarea[@placeholder='Write your input here']"))).send_keys(inp[x] + Keys.RETURN)
        return StoryManipulation.get_output(driver)

    def get_output(driver):
        time.sleep(15) # Wait for answer to generate
        return [x.text for x in driver.find_elements_by_xpath("//*[@class='aiText']")][-1]
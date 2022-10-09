import random
from telnetlib import GA
import time
import psutil
import subprocess
import os,shutil
from os import system,name 
import sys
from datetime import date
from time import perf_counter
#from pyvirtualdisplay import Display #for rpi usage 
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import config 
from dataclasses import dataclass
import bindwithnai
import logging

@dataclass
class ChatClass:
    name : str
    name2 : str

@dataclass 
class ArgumentClass:
    story : str

class NAI:
    AG = ArgumentClass("zero")

    def __init__(self) -> None:
        print(self.logo())
        if input('imagen? ') == 'y':NAI_interaction().img_operation_loop()
        else:NAI_interaction().main_operation_loop()

    def logo(self):
        return '''
  _   _                _    _    ___ 
 | \ | | _____   _____| |  / \  |_ _|
 |  \| |/ _ \ \ / / _ \ | / _ \  | | 
 | |\  | (_) \ V /  __/ |/ ___ \ | | 
 |_| \_|\___/ \_/ \___|_/_/   \_\___|     ver1.13beta
                                            
        
        
        
        '''
    def clear(self):
        if name == 'nt':
            _ = system('cls')
        else:
            _ = system('clear')

    def characters_name(self): return ChatClass(input("Name1?: "),input("Name2?: "))

    def choose_ur_adventure(self): return ArgumentClass(input("Choose your story: "))

    def main_gameplay_loop(self,driver):
        self.clear()
        self.logo()
        if(input("Is it a chat? (y/n)") == "n"):
            while True:
                user_input = input("N: ").split("//")
                print(user_input)
                if(input("Proceed?(y/n)") == "y"):print(bindwithnai.StoryManipulation.send_input(driver,user_input))
        else:
            name_set_up = self.characters_name()
            print(f"DEBUG {name_set_up.name} {name_set_up.name2}")
            while True:
                user_input = input("N: ")
                user_input = f"{name_set_up.name}: " + user_input + f"//{name_set_up.name2}: "
                print(user_input)
                if(input("Proceed?(y/n)") == "y"):print(bindwithnai.StoryManipulation.send_input(driver,user_input.split("//")))

class NAI_interaction(NAI):
        def __init__(self):
            self.opts = Options()

            #self.display = Display(visible=0, size=(800, 600)) #for rpi usage 
            #self.display.start() #for rpi usage 
            prefs = {"download.default_directory" : os.getcwd()}
            self.opts.add_argument("--disable-extensions")
            self.opts.add_argument("--proxy-server='direct://'")
            self.opts.add_argument("--proxy-bypass-list=*")
            self.opts.add_argument("--start-maximized")
            #self.opts.add_argument('--headless')
            self.opts.add_experimental_option("prefs",prefs)
            self.opts.add_argument('--disable-gpu')
            self.opts.add_argument('--disable-dev-shm-usage')
            self.opts.add_argument('--no-sandbox')
            self.opts.add_argument('--ignore-certificate-errors')
            self.opts.add_argument("--log-level=3")
            self.opts.add_experimental_option("excludeSwitches", ["enable-logging"])
            self.driver = webdriver.Chrome(options=self.opts)
            self.url = "https://novelai.net/login"

        def main_discord_loop(self,input):
            pass 
        
        def tg_img_op_loop(self,prompt):
            bindwithnai.SystemManipulation.auth(self.driver,self.url)
            super().clear()
            super().logo()
            bindwithnai.SystemManipulation.button_interaction(self.driver,"aria-label","Close Modal")
            bindwithnai.SystemManipulation.button_interaction(self.driver,"class","sc-48c34ae8-2 sc-48c34ae8-5 sc-9bc708a6-3 eVqxtQ lfyMed jSaLDb")
            bindwithnai.ImaGenManipulation.send_prompt(self.driver,prompt)
            bindwithnai.SystemManipulation.button_interaction(self.driver,"class","sc-434b3404-37 heUCxe")
            time.sleep(10)
            bindwithnai.ImaGenManipulation.save_img(self.driver)
            self.driver.close()

        def img_operation_loop(self):
            bindwithnai.SystemManipulation.auth(self.driver,self.url)
            super().clear()
            super().logo()
            bindwithnai.SystemManipulation.button_interaction(self.driver,"aria-label","Close Modal")
            bindwithnai.SystemManipulation.button_interaction(self.driver,"class","sc-48c34ae8-2 sc-48c34ae8-5 sc-9bc708a6-3 eVqxtQ lfyMed jSaLDb")
            while True:
                bindwithnai.ImaGenManipulation.send_prompt(self.driver,input("Input your prompt here: "))
                bindwithnai.SystemManipulation.button_interaction(self.driver,"class","sc-434b3404-37 heUCxe")
                time.sleep(10)
                bindwithnai.ImaGenManipulation.save_img(self.driver)
                NAI_interaction().img_work()
        
        def img_work(self):
            for x in os.listdir(f"./"):
                if ".png" in x:
                    shutil.copy2(f'./{x}',f"./png/{x}")
                    os.remove(x)

        def main_operation_loop(self):
            bindwithnai.SystemManipulation.auth(self.driver,self.url)
            super().clear()
            super().logo()
            bindwithnai.SystemManipulation.button_interaction(self.driver,"aria-label","Close Modal")
            bindwithnai.SystemManipulation.button_interaction(self.driver,"class","sc-7760eb68-1 hfJtMi toggler menubar-toggler")
            print("\n".join(bindwithnai.SystemManipulation.find_stories(self.driver)))
            while True:
                print(f"AG: {super().AG.story}")
                stories = super().choose_ur_adventure()
                if(stories.story in bindwithnai.SystemManipulation.find_stories(self.driver)):
                    bindwithnai.SystemManipulation.button_interaction(self.driver,"aria-label",stories.story)
                    time.sleep(5)
                    super().main_gameplay_loop(self.driver)
                else:
                    print("The exeption occured,probably this story is not exist in your story list,try again.")


if __name__ == "__main__":
    NAI()

import time
import unittest
from helpers import Common
from selenium import webdriver

# append the path of home directory
from log import logger
from selenium.webdriver.common.by import By


class TestPreSales():

    #@classmethod


    # launch the presales url
    def testlaunch(self):
        self.helper = Common()
        self.logger = logger()
        try:
            url = "https://mcassessor.maricopa.gov/"
            # Original start
            driver = self.helper.launch(url)
            cookie = driver.get_cookies()
            assert driver != None, "Unable to launch the Home Page"
            self.logger.info("Successfully launched the Home Page")
            time.sleep(5)
            #print(self.common.getElement("xpath").get_attribute("style"))
            self.helper.Search_Org()
            print("Done")

        except Exception as e:
            print(e)
        # self.logger.error(e)

TestPreSales().testlaunch()
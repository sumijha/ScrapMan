import csv
import os, sys, inspect
import time
from selenium import webdriver

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))))
from log import logger
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class Common():

    def __init__(self, driver=None):

        self.logger = logger()
        self.driver = driver
        self.File = open('output.csv', 'w', newline='')
        self.myFile = open('input.csv', newline='')
        self.Writer = csv.writer(self.File)
        self.Reader = csv.DictReader(self.myFile)
        wait = None

    # @property
    def launch(self, url):
        try:
            print("--------------------------")
            # self.report.report()
            print("launch")
            # DesiredCapabilities
            options = webdriver.ChromeOptions()
            options.add_argument('--ignore-certificate-errors')
            options.add_argument('--ignore-ssl-errors')
            options.add_argument('--start-maximized')
            options.add_argument('--disable-extensions')
            # options.add_argument("--user-data-dir=C:\\Users\\sujha\\AppData\\Local\Google\\Chrome\\User Data\\Default")
            dir_path = os.path.dirname(
                os.path.dirname(os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))))
            chromedriver = os.getcwd() + "/driver/chromedriver"
            os.environ["webdriver.chrome.driver"] = chromedriver
            print("driver initiated")
            self.driver = webdriver.Chrome(options=options, executable_path=chromedriver)

            # launch Application
            # self.logger.info('************Launch website**************')
            self.driver.get(url)

            return self.driver

        except Exception as e:
            print(e)
            # self.logger.error(e)
            return False

    def login(self):
        try:
            self.waitforElement("")
            self.setValue("", "")
            self.click("")
            # self.logger.info("*******LOGIN Successfull***********")
            return True
        except Exception as e:
            self.logger.error(e)
            return False

    def waitforElement(self, slocator):
        try:
            # Declaration of WebDriverWait
            self.wait = WebDriverWait(self.driver, 20)

            # findByXpath:
            self.logger.info("waiting for element " + loc)
            self.wait.until(EC.visibility_of_element_located(By.XPATH, slocator))

        except Exception as e:
            print(e)
            # self.logger.error(e)

    def click(self, loc):

        try:
            self.getElement(loc).click()

        except Exception as e:
            print(e)
            # self.logger.error(e)

    def setValue(self, loc, value):
        try:
            self.getElement(loc).send_keys(value)

        except Exception as e:
            print(e)
            # self.logger.error(e)

    def getElement(self, slocator):

        element = None
        try:
            # findByXpath
            element = self.driver.find_element(By.XPATH, slocator)

            return element

        except Exception as e:
            self.logger.error(e)
            print(e)
            return element

    def getElements(self, slocator):

        #	elements=None
        try:
            # findByXpath
            elements = self.driver.find_elements(By.XPATH, slocator)

            return elements

        except Exception as e:
            print(e)
            self.logger.error(e)
            return element

    def closeBrowser(self):
        try:
            self.driver.close()
        except Exception as e:
            print(e)


    # Write in CSV with Data
    def write_csv(self, Datalist):
        try:
            self.Writer.writerow(Datalist)
        except Exception as e:
            print(e)

    # Close the File
    def Close_File(self):
        self.File.close()
        print('Close File')

    ## Start for Scrap Auto ###

    # Read BusinessName Data
    def Get_Data(self):
        alist = []
        for row in self.Reader:
            alist.append(row['InpOrgName'])
        self.myFile.close()
        return alist

    # Search for Org Scrap Auto
    def Search_Org(self):
        locInpOrgName = "//input[@class='homeSearchField']"
        locBtnSrch = "//button[@class='homeSearchBtn']"

        data_list = self.Get_Data()
        inputKeyWord = data_list[0]

        self.setValue(locInpOrgName, inputKeyWord)
        self.click(locBtnSrch)
        time.sleep(4)

        self.Get_RealPropDet()

    def Get_RealPropDet(self):
        moreFlag = False
        locLnkAPN = "//div[@id='real-property-results-section']//td[@class='collapsing one wide']//a"
        locMoreSec = "//div[@id='more-results']//td[@class='collapsing one wide']//a"
        locBtnViewMore = "//div[@id='real-property-results-section']//a[text()='View more results']"
        locBtnViewMoreRental = "//div[@id='rental-results-section']//a[text()='View more results']"
        locLnkAPNRental = "//div[@id='rental-results-section']//td[@class='collapsing one wide']//a"
        locbtnISRCH = "//i[@id='search-button']"

        self.Writer.writerow(
            ['APN', 'Parcel_Type', 'Property Information', 'Owner Information', 'Mailing Address', 'Deed Number',
             'Last Deed Date', 'Sale Date', 'Sale Price'])
        try:
            while True:
                if moreFlag:
                    eleRecords = self.getElements(locMoreSec)
                else:
                    eleRecords = self.getElements(locLnkAPN)
                for ele in range(len(eleRecords)):
                    self.driver.execute_script("arguments[0].click();",eleRecords[ele])
                    time.sleep(1)
                    # Write in CSV
                    self.Write_RentalData()
                    self.driver.execute_script("window.history.go(-1)")
                    time.sleep(3)
                    if moreFlag:
                        eleRecords = self.getElements(locMoreSec)
                    else:
                        eleRecords = self.getElements(locLnkAPN)

                if self.getElement(locBtnViewMore) is None:
                    break
                else:
                    btnMore = self.getElement(locBtnViewMore)
                    self.driver.execute_script("arguments[0].click();", btnMore)
                    time.sleep(3)
                    moreFlag = True

            #Scroll Into View
            self.click(locbtnISRCH)
            time.sleep(3)
            self.driver.execute_script("arguments[0].scrollIntoView();", self.getElement(locLnkAPNRental))
            moreFlag = False

            while True:
                if moreFlag:
                    eleRecords = self.getElements(locMoreSec)
                else:
                    eleRecords = self.getElements(locLnkAPNRental)
                for ele in range(len(eleRecords)):
                    self.driver.execute_script("arguments[0].click();",eleRecords[ele])
                    time.sleep(1)
                    # Write in CSV
                    self.Write_RentalData()
                    self.driver.execute_script("window.history.go(-1)")
                    time.sleep(3)
                    if moreFlag:
                        eleRecords = self.getElements(locMoreSec)
                    else:
                        eleRecords = self.getElements(locLnkAPNRental)

                if self.getElement(locBtnViewMoreRental) is None:
                    break
                else:
                    btnViewMore = self.getElement(locBtnViewMoreRental)
                    self.driver.execute_script("arguments[0].click();",btnViewMore)
                    time.sleep(3)
                    moreFlag = True

            # Close File
            self.Close_File()

        except Exception as e:
            print(e)
            self.Close_File()

    #Write Rental Property Data
    def Write_RentalData(self):
        data_RealProp = []
        locAPNVal = "(//h3[@class='ui huge basic header' and text()])[1]"
        locParcelVal = "(//h3[@class='ui huge basic header' and text()])[2]"
        locPropInfo = "//div[text()='Property Information']/parent::div//a/strong"
        locOwnerInfo = "//div[text()='Owner Information']/parent::div//a/strong"
        locProInfo = "//div[text()='Property Information']/parent::td//a/strong"
        locOwnInfo = "//div[text()='Owner Information']/parent::td//a/strong"
        locMailingAdd = "//td[text()='Mailing Address']/following-sibling::td"
        locDeedNumber = "//td[text()='Deed Number']/following-sibling::td/a"
        locDeedDate = "//td[text()='Last Deed Date']/following-sibling::td"
        locSaleDate = "//td[text()='Sale Date']/following-sibling::td"
        locSalePrice = "//td[text()='Sale Price']/following-sibling::td"

        eleAPN = self.getElement(locAPNVal)
        eleParcelVal = self.getElement(locParcelVal)
        elePropInfo = self.getElement(locPropInfo)
        eleOwnerInfo = self.getElement(locOwnerInfo)
        eleProInfo = self.getElement(locProInfo)
        eleOwnInfo = self.getElement(locOwnInfo)
        eleMailAdd = self.getElement(locMailingAdd)
        eleDeedNum = self.getElement(locDeedNumber)
        eleDeedDate = self.getElement(locDeedDate)
        eleSaleDate = self.getElement(locSaleDate)
        eleSalePrice = self.getElement(locSalePrice)


        data_RealProp.append(eleAPN.text)

        if not eleParcelVal is None:
            data_RealProp.append(eleParcelVal.text)
        else:
            data_RealProp.append('')

        if not elePropInfo is None:
            data_RealProp.append(elePropInfo.text)
        elif not eleProInfo is None:
            data_RealProp.append(eleProInfo.text)
        else:
            data_RealProp.append('')

        if not eleOwnerInfo is None:
            data_RealProp.append(eleOwnerInfo.text)
        elif not eleOwnInfo is None:
            data_RealProp.append(eleOwnInfo.text)
        else:
            data_RealProp.append('')

        if not eleMailAdd is None:
            data_RealProp.append(eleMailAdd.text)
        else:
            data_RealProp.append('')

        if not eleDeedNum is None:
            data_RealProp.append(eleDeedNum.text)
        else:
            data_RealProp.append('')

        if not eleDeedDate is None:
            data_RealProp.append(eleDeedDate.text)
        else:
            data_RealProp.append('')

        if not eleSaleDate is None:
            data_RealProp.append(eleSaleDate.text)
        else:
            data_RealProp.append('')

        if not eleSalePrice is None:
            data_RealProp.append(eleSalePrice.text)
        else:
            data_RealProp.append('')

        self.write_csv(data_RealProp)

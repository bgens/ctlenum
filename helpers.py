import requests
import urllib3
from selenium import webdriver
from os import path, makedirs


class traceable:
    def __init__(self, url, output_dir):
        self.url = url
        urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning) #Remove ssl warning output
        self.options = webdriver.ChromeOptions()
        self.options.add_argument("headless")
        self.options.add_argument('--ignore-certificate-errors')
        self.options.add_argument('--disable-extensions')
        self.options.add_argument('--disable-dev-shm-usage')
        self.options.add_argument('--disable-gpu')
        self.options.add_argument('disable-infobars')
        self.options.add_experimental_option('excludeSwitches', ['enable-logging'])
        self.output_dir = output_dir

    def httpStatus(self):
        check = requests.get(self.url, verify=False, timeout=1) #Disable ssl verification
        return check.status_code

    def getScreenshot(self):
        with webdriver.Chrome("./chromedriver.exe", chrome_options=self.options) as driver:
            driver.set_window_size(width=2200, height=1800)
            driver.get(self.url)
#            time.sleep(2)
            driver.save_screenshot(self.output_dir + self.url.split('/')[2] + ".png")


def checkFolder(domain):
    try:
        if path.exists("./output/" + domain + "/") is True:
            pass
        else:
            makedirs("./output/" + domain + "/")
    except():
        print("Probable permissions issue for checking/creating output Directory `./output/`")

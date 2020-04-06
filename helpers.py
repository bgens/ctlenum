import requests
import urllib3
from selenium import webdriver
from os import path, makedirs
from selenium.common.exceptions import TimeoutException


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
        user_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.163 Safari/537.36'
        header = {'User-Agent': user_agent}
        try:
            check = requests.get(self.url, verify=False, headers=header, timeout=2) #Disable ssl verification
            return check.status_code
        except(requests.exceptions.TooManyRedirects):
            status_code = 301
            return status_code


    def getScreenshot(self):
        with webdriver.Chrome("./chromedriver.exe", chrome_options=self.options) as driver:
            driver.set_window_size(width=2200, height=1800)
            driver.set_page_load_timeout(5)
            try:
                driver.get(self.url)
                driver.save_screenshot(self.output_dir + self.url.split('/')[2] + ".png")
            except TimeoutException as ex:
                print("URL: [ " + self.url + " ] failed to respond.  Error: " + str(ex))
                driver.close()


def checkFolder(domain):
    try:
        if path.exists("./output/" + domain + "/") is True:
            pass
        else:
            makedirs("./output/" + domain + "/")
    except():
        print("Probable permissions issue for checking/creating output Directory `./output/`")

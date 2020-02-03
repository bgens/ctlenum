import requests
import urllib3
#import ctlenum
#from multiprocessing import Pool

class traceable:
    def __init__(self, url):
        self.url = url
        urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning) #Remove ssl warning output

    def httpStatus(self):
        check = requests.get(self.url, verify=False, timeout=1) #Disable ssl verification
        return check.status_code

    def getScreenshot(self):
        pass

class auxilary:
    def __init__(self):
        pass

#if __name__ == '__main__':
#    target = traceable('https://google.com')
#    print(target.httpStatus())

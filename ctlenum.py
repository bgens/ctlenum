import argparse
import requests
import config
import urllib3
from helpers import traceable
from threading import Thread
from Queue import Queue
import logging

parser = argparse.ArgumentParser()
parser.add_argument('--target', help="target for scan. example: --target google.com", required=True)
parser.add_argument('-w', action='store_true', help="Wildcards.  Shows wildcard subdomains like: *.google.com")
parser.add_argument('-a', action='store_true', help="All output. Show non-target domains caught in search."
                                                    " Useful for finding vendors for target domain")
parser.add_argument('-s', action='store_false', help="Generate traceable traffic using http requests")
parser.add_argument('-ss', action='store_false', help="Take screenshot of target domain")

args = parser.parse_args()

target = args.target


class CtlEnum(object):
    def __init__(self, api, domain, wild=False, all_domains=False, scan=False, screenshot=False):
        self.api = api
        self.domain = domain
        self.wild = wild
        self.all_domains = all_domains
        self.scan = scan
        self.screenshot = screenshot
        self.q = Queue()
        urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning) #Remove ssl warning output

    def print_target(self):
        print('Target Domain: ', str(self.domain))

    def get_dns(self):
        url = ['https://api.certspotter.com/v1/issuances?domain=', self.domain,
               '&include_subdomains=true&match_wildcards=true&expand=dns_names']
        bearer = ['Bearer ', self.api]
        header = {'Authorization': ''.join(bearer)}
        r = requests.get(''.join(url), headers=header, verify=False).json()
        dns_list = list()

        for item in r:
            list_count = len(item['dns_names'])
            if list_count > 1:
                for entry in item['dns_names']:
                    if self.wild is False and entry[0][:1] == '*':
                        pass
                    else:
                        dns_list.append(str(entry))
            else:
                str_item = str(item['dns_names'][0])
                if self.wild is False and str_item[0][:1] == '*':
                    pass
                else:
                    dns_list.append(str_item)
        return dns_list

    def doScan(self, dnsentry):
        if self.all_domains is False:
            if self.domain in dnsentry:
                try:
                    url_check = traceable("https://" + dnsentry + "/")
                    message = (dnsentry + " ----- ")
                    if url_check.httpStatus() == 200:
                        message = (message + str(url_check.httpStatus()))
                        if self.screenshot is True:
                            url_check.getScreenshot()
                            message = (message + " ----- Screenshot Captured")
                            return message
                    else:
                        return message
                except requests.ConnectionError:
                    message = (message + "Connection Error")
                    return message
                except requests.ReadTimeout:
                    message = (message + "No Response")
                    return message
        else:
            try:
                url_check = traceable("https://" + dnsentry + "/")
                message = (dnsentry + " ----- ")
                if url_check.httpStatus() == 200:
                    message = (message + str(url_check.httpStatus()))
                    if self.screenshot is True:
                        url_check.getScreenshot()
                        message = (message + " ----- Screenshot Captured")
                        return message
                else:
                    return message
            except requests.ConnectionError:
                message = (message + "Connection Error")
                return message
            except requests.ReadTimeout:
                message = (message + "No Response")
                return message

def droneWork():
    while True:
        targ = q.get()
        output = scanme.doScan(targ)
        if output is not None:
            logging.info(output)
        q.task_done()

if __name__ == '__main__':
    scanme = CtlEnum(config.api_key, domain=target, scan=True, screenshot=True)
    q = Queue()
    logging.basicConfig(format='%(message)s', level=logging.INFO)
    for entry in scanme.get_dns():
        q.put(entry)

    for x in range(30):
        t = Thread(target=droneWork)
        t.daemon = True
        t.start()
    q.join()

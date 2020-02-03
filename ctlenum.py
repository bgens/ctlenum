import argparse
import requests
import config
from helpers import traceable

parser = argparse.ArgumentParser()
parser.add_argument('--target', help="target for scan. example: --target google.com", required=True)
parser.add_argument('-w', action='store_true', help="Wildcards.  Shows wildcard subdomains like: *.google.com")
parser.add_argument('-a', action='store_true', help="All output. Show non-target domains caught in search."
                                                    " Useful for finding vendors for target domain")


args = parser.parse_args()

target = args.target


class CtlEnum(object):
    def __init__(self, api, domain, wild):
        self.api = api
        self.domain = domain
        self.wild = wild

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

        return set(dns_list)


scan = CtlEnum(config.api_key, target, args.w)

if __name__ == '__main__':
    if args.a is False:
        for dnsentry in scan.get_dns():
            if target in dnsentry:
                try:
                    url_check = traceable("https://" + dnsentry + "/")
                    print(dnsentry + " ----- "),
                    print(url_check.httpStatus())
                except requests.ConnectionError:
                    print("Connection Error")
                except requests.ReadTimeout:
                    print("No Response")
    else:
        for dnsentry in scan.get_dns():
            try:
                url_check = traceable("https://" + dnsentry + "/")
                print(dnsentry + " ----- "),
                print(url_check.httpStatus())
            except requests.ConnectionError:
                print("Connection Error")
            except requests.ReadTimeout:
                print("No Response")

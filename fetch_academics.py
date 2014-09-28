# -*- coding: utf-8 -*-
import urllib, urllib2
import json
import os
from bs4 import BeautifulSoup

class Academic_Fetcher():
    def __init__(self):
        self.url = 'http://www.yarbis1.yildiz.edu.tr/face/ara/loadSearchResults.php'
        self.academics = []

    def start_fetching(self):
        alphabet = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N',
                    'O', 'P', 'R', 'S', 'T', 'U', 'V', 'Y', 'Z']
        for letter in alphabet:
            # post request for every letter
            url_2 = 'http://www.yarbis1.yildiz.edu.tr/face/ara/loadSearchResults.php'
            values = dict(harf=letter)
            data = urllib.urlencode(values)
            req = urllib2.Request(url_2, data)
            rsp = urllib2.urlopen(req)
            content = rsp.read()
            self.process_soup(self.turn_data_to_soup(content))
            print 'academics starts with ' + letter + ' completed.'

    def turn_data_to_soup(self, data):
        soup = BeautifulSoup(data)
        return soup

    def process_soup(self, soup):
        body_tree = soup.find("tbody")
        all_rows = body_tree.find_all("tr")
        for row in all_rows:
            academic_name = row.find("td", attrs = {'width': '120px'}).text
            academic_department = row.find("td", attrs = {'width': '150px'}).text
            academic_title = row.find("td", attrs = {'width': '60px'}).text
            academic_homepage_row = row.find("td", attrs = {'width': '70px'})
            academic_homepage = academic_homepage_row.find('a')['href']
            academic = {
                'name': academic_name,
                'department': academic_department,
                'title': academic_title,
                'homepage': academic_homepage
            }
            self.academics.append(academic)

    def jsonify(self):
        return json.dumps(self.academics, indent=4, separators=(',', ': '))

    def write_json(self):
        dir = os.path.dirname(os.path.abspath(__file__))
        filename = "academics.json"
        file = open(dir + "/" + filename, "wb")
        file.write(self.jsonify())
        file.close()


if __name__ == '__main__':
    academic_fetcher = Academic_Fetcher()
    academic_fetcher.start_fetching()
    academic_fetcher.jsonify()
    academic_fetcher.write_json()
    print "total %d academics." % (len(academic_fetcher.academics))

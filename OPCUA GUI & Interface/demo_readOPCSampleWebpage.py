from bs4 import BeautifulSoup
import datetime, time
import requests
from tinydb import TinyDB, Query
import urllib3
import xlsxwriter
import re

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

url = "https://lamn18.github.io/"
total_added = 0

def make_soup(url):
    page = requests.get(url)
    return BeautifulSoup(page.text, 'lxml')

def testReadWebpage():
    soup = make_soup(url)

    l = soup.find("div",{"class":"row"})

    state = findState(1, str(l))
    print("current state is {}".format(state))

    i = 0
    while i < 5:
        soup = make_soup(url)
        l = soup.find("div",{"class":"row"})
        new_state = findState(1, str(l))
        if new_state != state:
            print("state has chaned to {}".format(new_state))
            state = new_state
        i+=1

def findState(n, list):
    idname = "s{}".format(n)
    temp_regex = r"(?<=" + re.escape(idname) + r"\">)(.*?)(?=</p>)"
    return re.search(temp_regex, list).group(0)




testReadWebpage()
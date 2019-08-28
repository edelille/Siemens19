from bs4 import BeautifulSoup
import datetime, time
from tinydb import TinyDB, Query
import urllib3
import xlsxwriter
import re

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

url = 'https://finance.yahoo.com/quote/BA/'
total_added = 0

def make_soup(url):
    http = urllib3.PoolManager()
    r = http.request("GET", url)
    return BeautifulSoup(r.data, 'lxml')

def testReadWebpage():
    soup = make_soup(url)

    #try to find stock price
    l = soup.find("div",{"id":"app"})
    sp = findStockPrice(str(l))
    print("Boeing's stock price is {} currently".format(sp))
    while True:
        soup = make_soup(url)
        l = soup.find("div",{"id":"app"})
        new_sp = findStockPrice(str(l))
        if (new_sp != sp):
            print("Boeing's stock price changed to {}".format(new_sp))
            sp = new_sp


def findStockPrice(list):
    return re.search(r"(?<=data-reactid=\"52\">)(.*?)(?=</span>)", list).group(0)

testReadWebpage()
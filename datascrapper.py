from requests import get
from requests.exceptions import RequestException
from contextlib import closing
from bs4 import BeautifulSoup
import csv

filename = 'Scrapped_data1.csv'

def simple_get(url):
    try:
        with closing(get(url, stream=True)) as resp:
            if is_good_response(resp):
                return resp.content
            else:
                return None
    except RequestException as e:
        log_error('Error during requests to {0} : {1}'.format(url, str(e)))
        return None

def is_good_response(resp):
    content_type = resp.headers['Content-Type'].lower()
    return (resp.status_code == 200
            and content_type is not None
            and content_type.find('html') > -1)

def log_error(e):
    print(e)

def extract_page(url):
    raw_html = simple_get(url)
    html = BeautifulSoup(raw_html, 'html.parser')
    entries = html.findAll('div', {"class": "entry"})
    for entry in entries:
        #print(entry)
        entryheader = entry.find('h2', {"class": "entry-title"})
        entrytitle = entryheader.find('a')
        entrydetails = entry.find('p').text
        print("Entry Title: ",entrytitle.string)
        print("Entry Link: ", entrytitle['href'])
        print("Entry Details: ", entrydetails)
        db_insert(entrytitle.string, entrytitle['href'], entrydetails)


def check_exists(href):
    with open(filename, mode='rb') as f:
        csvreader = csv.reader(f, delimiter=",")
        for row in csvreader:
            if href in row[1]:
                return False
            else:
                return True

def db_insert(title, link, details):
    with open(filename, mode='a', encoding="utf-8") as csv_file:
        plugin_writer = csv.writer(csv_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        plugin_writer.writerow([title, link, details])

def start_scrap(search, pages):
    for i in range(1, pages):
        curr_page = str(i)
        url = "https://wordpress.org/plugins/search/" + search + "/" + curr_page
        print("Current URL: ", url)
        extract_page(url)


url = 'https://www.coches.net/segunda-mano/?pg=2'

import requests
from bs4 import BeautifulSoup as soup
headers={"user_agent":"mozilla"}
req=requests.get(url, headers=headers)
page=soup(req.text, "html.parser")

print(page)
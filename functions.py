import requests
from bs4 import BeautifulSoup

def fetchHTML(url):
    query = requests.get(url)
    htmlcontent = query.content
    soup = BeautifulSoup(htmlcontent, 'html.parser')
    return soup
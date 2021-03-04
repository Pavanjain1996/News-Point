#importing modules
import requests
from bs4 import BeautifulSoup
from main import Article
from main import db

#This function is to fetch html data from website
def fetchHTML(url):
    query = requests.get(url)
    htmlcontent = query.content
    soup = BeautifulSoup(htmlcontent, 'html.parser')
    return soup

#This function will fiter and collect data from html data of BBC website and push into database
def bbcNews():
    soup = fetchHTML('https://www.bbc.com/news')
    h3 = soup.find_all('h3', class_='gs-c-promo-heading__title gel-pica-bold nw-o-link-split__text')
    para = soup.find_all('p', class_='gs-c-promo-summary gel-long-primer gs-u-mt nw-c-promo-summary')
    links = soup.find_all('a', class_='gs-c-promo-heading gs-o-faux-block-link__overlay-link gel-pica-bold nw-o-link-split__anchor')
    image_url = soup.find_all('div', class_='gs-o-responsive-image gs-o-responsive-image--16by9')
    for i in range(len(image_url)):
        t = image_url[i].findChild().get('data-src')
        image_url[i] = t[:30] + '600' + t[37:]
    for i in range(4):               #Pushing data to database
        article = Article.query.filter_by(headline=h3[i].get_text()).all()
        if article:           #Checking if the data is already present or not
            print('Article Exists')
        else:
            article = Article(headline=h3[i].get_text(),image_url=image_url[i],content=para[i+2].get_text(),redirect_url='https://www.bbc.com'+links[i].get('href'),data_from='BBC News')
            db.session.add(article)
            db.session.commit()

#Laod functions to push data into database
bbcNews()
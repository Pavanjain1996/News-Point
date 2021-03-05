#importing modules
import requests
from bs4 import BeautifulSoup
from main import Article
from main import db

#This function will fetch html data from website
def fetchHTML(url):
    query = requests.get(url)
    htmlcontent = query.content
    soup = BeautifulSoup(htmlcontent, 'html.parser')
    return soup

#This function will push data into database
# heading - tags
# image_url - url
# content - tags
# redirect_url - url
def pushData(headline, image_url, content, redirect_url, data_from):
    for i in range(len(headline)):
        article = Article.query.filter_by(headline=headline[i].get_text()).all()
        if article:
            print('Article from',data_from,'Exists')
        else:
            article = Article(headline=headline[i].get_text(),image_url=image_url[i],content=content[i].get_text(),redirect_url=redirect_url[i],data_from=data_from)
            db.session.add(article)
            db.session.commit()
            print('Article Posted from', data_from)

#This function will filter the data from html data of BBC website
def bbcNews():
    soup = fetchHTML('https://www.bbc.com/news')
    headline = soup.find_all('h3', class_='gs-c-promo-heading__title gel-pica-bold nw-o-link-split__text')
    content = soup.find_all('p', class_='gs-c-promo-summary gel-long-primer gs-u-mt nw-c-promo-summary')
    redirect_url = soup.find_all('a', class_='gs-c-promo-heading gs-o-faux-block-link__overlay-link gel-pica-bold nw-o-link-split__anchor')
    redirect_url = ['https://www.bbc.com'+x.get('href') for x in redirect_url]
    image_url = soup.find_all('div', class_='gs-o-responsive-image gs-o-responsive-image--16by9')
    for i in range(len(image_url)):
        t = image_url[i].findChild().get('data-src')
        image_url[i] = t[:30] + '600' + t[37:]
    pushData(headline[:4], image_url[:4], content[2:6], redirect_url[:4], 'BBC News')

#This function will filter the data from html data of CNN Website
def cnnNews():
    soup = fetchHTML('https://www.nytimes.com/section/world')
    h2 = soup.find_all('h2', class_='css-byk1jx e4e4i5l1')
    headline = [ x.findChild() for x in h2 ]
    redirect_url = ['https://www.nytimes.com/'+t.get('href') for t in headline]
    content = soup.find_all('p', class_='css-tskdi9 e4e4i5l4')
    image_url = soup.find_all('div', class_='css-10wtrbd')
    image_url = image_url[:2]
    image_url = [ x.findChild().findChild().findChild().get('src') for x in image_url]
    pushData(headline[:2], image_url[:2], content[:2], redirect_url[:2], 'CNN News')

#This function will filter the data from html data of aajtak Website
def aajtak():
    soup = fetchHTML('https://www.aajtak.in/')
    soup = soup.find_all('div', class_='hhm-stoy-left-body')
    headline = [soup[0].findChildren()[2]]
    image_url = [soup[0].findChildren()[4].get('src')]
    content = [soup[0].findChildren()[6]]
    redirect_url = [soup[0].findChildren()[0].get('href')]
    pushData(headline, image_url, content, redirect_url, 'AajTak News')

#This function will filter the data from html data of aajtak Website
def indiaTV():
    soup = fetchHTML('https://www.indiatvnews.com/')
    soup = soup.find_all('li', class_='eventTracking')
    headline = [i.find_all('h2')[0] for i in soup]
    image_url = [i.find_all('img')[0].get('data-original') for i in soup]
    content = [i.find_all('h2')[0] for i in soup]
    redirect_url = [i.find_all('a')[0].get('href') for i in soup]
    pushData(headline, image_url, content, redirect_url, 'indiaTV News')

#Throwing Everything into database
def setDatabase():
    bbcNews()
    cnnNews()
    aajtak()
    indiaTV()

#Launching
setDatabase()
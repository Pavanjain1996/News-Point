from flask import Flask, render_template
import requests
from bs4 import BeautifulSoup

app = Flask(__name__)

@app.route('/')
def index():
    url = 'https://www.bbc.com/news'
    query = requests.get(url)
    htmlcontent = query.content
    soup = BeautifulSoup(htmlcontent, 'html.parser')
    h3 = soup.find_all('h3', class_='gs-c-promo-heading__title gel-pica-bold nw-o-link-split__text')
    para = soup.find_all('p', class_='gs-c-promo-summary gel-long-primer gs-u-mt nw-c-promo-summary')
    links = soup.find_all('a', class_='gs-c-promo-heading gs-o-faux-block-link__overlay-link gel-pica-bold nw-o-link-split__anchor')
    content_to_send=[]
    for i in range(3):
        content_to_send.append([i+1,h3[i].get_text(),para[i+2].get_text(),'https://www.bbc.com'+links[i].get('href')])
    return render_template('index.html', content=content_to_send)

if __name__=='__main__':
    app.run()
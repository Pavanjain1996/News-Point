from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from functions import fetchHTML

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///news.db'
db = SQLAlchemy(app)

class Article(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    headline = db.Column(db.String(200), nullable=False)
    image_url = db.Column(db.String(1000), nullable=False)
    content = db.Column(db.String(400), nullable=False)
    redirect_url = db.Column(db.String(400), nullable=False)
    data_from = db.Column(db.String(200), nullable=False)

    def __repr__(self):
        return headline

def bbcNews():
    k = 1
    soup = fetchHTML('https://www.bbc.com/news')
    h3 = soup.find_all('h3', class_='gs-c-promo-heading__title gel-pica-bold nw-o-link-split__text')
    para = soup.find_all('p', class_='gs-c-promo-summary gel-long-primer gs-u-mt nw-c-promo-summary')
    links = soup.find_all('a', class_='gs-c-promo-heading gs-o-faux-block-link__overlay-link gel-pica-bold nw-o-link-split__anchor')
    image_url = soup.find_all('div', class_='gs-o-responsive-image gs-o-responsive-image--16by9')
    for i in range(len(image_url)):
        t = image_url[i].findChild().get('data-src')
        image_url[i] = t[:30] + '600' + t[37:]
    content=[]
    for i in range(3):
        content.append([k,h3[i].get_text(),para[i+2].get_text(),'https://www.bbc.com'+links[i].get('href'),image_url[i],'BBC News'])
        k=k+1
    return content

@app.route('/')
def index():
    bbc = bbcNews()
    content = []
    content.extend(bbc)
    return render_template('index.html', content=content)

if __name__=='__main__':
    app.run()
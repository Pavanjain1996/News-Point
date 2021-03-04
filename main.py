#importing modules
from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy

#creating and configuring app
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///news.db'
db = SQLAlchemy(app)

#Creating class
class Article(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    headline = db.Column(db.String(200), nullable=False)
    image_url = db.Column(db.String(1000), nullable=False)
    content = db.Column(db.String(400), nullable=False)
    redirect_url = db.Column(db.String(400), nullable=False)
    data_from = db.Column(db.String(200), nullable=False)

    def __repr__(self):
        return self.headline

#Url Routes
@app.route('/')
def index():
    content = Article.query.order_by(Article.id.desc()).limit(10).all()
    return render_template('index.html', content=content)

#Launching App
if __name__=='__main__':
    app.run()
from flask import Flask , render_template , request ,redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)

## the sql database confic
SQLALCHEMY_TRACK_MODIFICATIONS = False
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'
db = SQLAlchemy(app)

## database models
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20), unique=True, nullable=False)
    password = db.Column(db.String(20),nullable=False)
    profile_img = db.Column(db.String(), default='main.jpg')
    posts = db.relationship('Post', backref='auther',lazy=True)
    def __repr__(self):
        return self.name
    
class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(40),nullable=False)
    content = db.Column(db.String(1000),nullable=False)
    date = db.Column(db.DateTime,default=datetime.utcnow)
    auther_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable= False)

    def __repr__(self):
        return self.title
    
    
@app.route('/')
def test():
    return 'hellow world'

if __name__ == '__main__':
    app.run(debug=True)
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

## login  
@app.route('/', methods = ['GET','POST'])
def login():
    if request.method == "GET":
        return render_template('login.html')
    else:
        name = request.form.get('name')
        password = request.form.get('password')
        if User.query.filter_by(name=name).filter_by(password=password).all() == []:
            return redirect('/')
        else:
            Use = User.query.filter_by(name=name).filter_by(password=password).first() 
            return redirect('/posts/%s'%Use.id)

## signin 
@app.route('/signin', methods= ['GET','POST'])
def signin():
    if request.method == 'GET' :
        return render_template('signin.html')
    else:
        name = request.form.get('name')
        password = request.form.get('password')
        u = User(name=name, password=password)
        db.session.add(u)
        db.session.commit()
        id = User.query.filter_by(name=name).filter_by(password=password).first().id
        return redirect('posts/%s'%id)
    
## posts
@app.route('/posts/<int:id>',methods= ["GET","POST"])
def posts(id):
    user = User.query.get_or_404(id)
    if request.method == "GET":
        return render_template('posts.html', user=user)
    else:
        title = request.form.get("title")
        content = request.form.get('content')
        p = Post(title=title, content=content, auther_id = id)
        db.session.add(p)
        db.session.commit()
        return render_template('posts.html', user=user)

if __name__ == '__main__':
    app.run(debug=True)
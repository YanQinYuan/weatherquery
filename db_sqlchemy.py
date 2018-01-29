from flask_sqlalchemy import SQLAlchemy
from flask import Flask
import psycopg2
from datetime import datetime
from constant import POSTGRES_USER, POSTGRES_PW, POSTGRES_URL, POSTGRES_DB
# from datetime import datetime
app = Flask(__name__)
app.config.from_object(__name__) # load config from this file , flaskr.py
# Load default config and override config from an environment variable
DB_URL = 'postgresql+psycopg2://{user}:{pw}@{url}/{db}'\
            .format(user=POSTGRES_USER,pw=POSTGRES_PW,url=POSTGRES_URL,db=POSTGRES_DB)
# ----> 需要先建立数据库

app.config['SQLALCHEMY_DATABASE_URI'] = DB_URL
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False # silence the deprecation warning

db = SQLAlchemy(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(200), unique=False, nullable=True)
    password = db.Column(db.String(200), unique=False, nullable=True)
    def __repr__(self):
        return self.username, self.password
    
    def save(self):
        db.session.add(self)
        db.session.commit()

class History(db.Model):
    user_id = db.Column(db.Integer, primary_key=True)
    city = db.Column(db.String(80), nullable=False)
    result = db.Column(db.Text, nullable=False)
    day = db.Column(db.DateTime, nullable=False,
        default=datetime.utcnow)
    def __repr__(self):
        return self.user_id, self.city, self.result, self.day

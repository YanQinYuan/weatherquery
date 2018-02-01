# encoding:utf-8
#session需要用的
API = "https://api.seniverse.com/v3/weather/daily.json"
LANGUAGE = "zh-Hans"
SECRET_KEY = "ygnfdic5sis9nfpt"
DIALECT = 'mysql'
DRIVER = 'pymysql'
USERNAME = 'esaytowrite'
PASSWORD = '11111111'
HOST = '101.132.133.202'
PORT = '3306'
DATABASE = 'esaytowrite'
import os

DB_URI = '{}+{}://{}:{}@{}:{}/{}?charset=utf8'.format(DIALECT,DRIVER,USERNAME,PASSWORD,HOST,PORT,DATABASE)
SQLALCHEMY_DATABASE_URI = DB_URI

SQLALCHEMY_TRACK_MODIFICATIONS = False

#微信token
WX_TOKEN = '2vX79QF'
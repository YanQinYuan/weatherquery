# -*- coding: utf-8 -*-
from flask import Flask,url_for, render_template, request, redirect
from weatherquery import get_weather
# from database import get_city_weather, insert_data, update_weather,get_history, isExisted, add_user,register_check, create_table
# from wtforms import Form, TextField,PasswordField,validators
from urllib import parse
import os
from flask import session, g, abort, flash, escape
import hashlib
import datetime
from db_sqlchemy import User, History
# from flask_sqlalchemy import SQLAlchemy
# from wechatpy.crypto import WeChatCrypto
# from wechatpy import parse_message, create_reply
# from wechatpy.utils import check_signature
# from wechatpy.exceptions import InvalidSignatureException
# from wechatpy.exceptions import InvalidAppIdException
import psycopg2
# from datetime import datetime
app = Flask(__name__)
app.config.from_object(__name__) # load config from this file , flaskr.py
# Load default config and override config from an environment variable

app.config.update(dict(
    DATABASE=os.path.join(app.root_path, 'weather128.db'),
    SECRET_KEY='e35d7f4348184ed6a9aa15adfdb8c6f0' # uuid.uuid4.hex
))
app.config.from_envvar('FLASKR_SETTINGS', silent=True)

@app.cli.command('resetdb')
def resetdb_command():
    """Destroys and creates the database + tables."""

    from sqlalchemy_utils import database_exists, create_database, drop_database
    if database_exists(DB_URL):
        print('Deleting database.')
        drop_database(DB_URL)
    if not database_exists(DB_URL):
        print('Creating database.')
        create_database(DB_URL)

    print('Creating tables.')
    db.create_all()
    print('Shiny!')

@app.route('/register/', methods=['GET', 'POST'])
def user_register():
    context = {}
    error = None
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        re_password = request.form.get('re_password')
        if not username:
            error = '用户名不能为空'
        elif not password:
            error = '密码不能为空'
        elif password != re_password:
            error = '两次输入的密码不一致'
        elif query_user(username):
            error = '用户已存在'
        if error is None:
            # create_user(username, password)
            user = User(username=username, password=password)
            db.session.add(admin)
            db.session.cmmit()
            return redirect(url_for('login'))
        else:
            context.update({
            'error':error,
            'username':username
            })
    return render_template('register.html', **context)
@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    context = {}
    if request.method == "POST":
        username = request.form.get('username')
        password = request.form.get('password')
        if not username:
            error = '请输入用户名'
        else:
            # user = get_user()
            user = User(username=username)
            if not user:
                error = '用户不存在'
            else:
                user_password = user[-1]
                if password != user_password:
                    error = '用户名或密码错误'
                else:
                    session['login'] = True
                    session['user'] = user
                    return redirect(url_for('query'))
        context.update({
        'error':error
        })
    return render_template('login.html', **context)

@app.route('/logout')
def logout():
    # remove the username from the session if it's there
    session["login"] = False
    session["user"] = None
    return redirect(url_for('login'))

# set the secret key.  keep this really secret:
# app.secret_key = 'A0Zr98j/3yX R~XHH!jmN]LWX/,?RT'

@app.route('/', methods=['GET','POST'])
def query():
    city_query = request.args.get('city')
    user = session.get('user')
    query_time = datetime.datetime.now()
    if request.args.get('query')=="Query" and len(city_query) != 0:
        create_table() # reset history 
        try:
            weather_str = get_city_weather(city_query)
            print(weather_str + "database")
            return render_template('index.html', weather_str=weather_str)
        except TypeError:
            try:
                day,location,weather,low,weather_str = get_weather(city_query)
                user_id = user[0]
                username = user[1]
                insert_history(user_id, city_query, weather_str, query_time)
                return render_template('index.html', weather_str=weather_str)
            except TypeError:
                try:
                    day,location,weather,low,weather_str = get_weather(city_query)
                    return render_template('index.html', weather_str=weather_str)
                except ValueError:
                    error = '无该城市天气信息'
                    return render_template('index.html', error=error)
    elif request.args.get('history')=="History":
        try:
            user_id = user[0]
            username = user[1]
            history = query_history(user_id)
            return render_template('index.html', history=history)
        except TypeError:
            error = '请先登录'
            return render_template('index.html', error=error)
    elif request.args.get('help')=="Help":
        help = "help"
        return render_template("index.html",help=help)
    elif request.args.get('update')=="help":
        city = city_query.split(' ')[0]
        print(city + "1")
        update = city_query.split(' ')[1]
        print(city+"\n"+update)
        update_data = update_weather(city, update)
        print(update_data,"2")
        return render_template('index.html', update_data=update_data)
    else:
        error = '请输入正确的城市名'
    return render_template('index.html', error=error)

if __name__ == '__main__':
    app.run(debug=True)

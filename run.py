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


TOKEN = os.getenv('WECHAT_TOKEN', '123456')
EncodingAESKey = os.getenv('WECHAT_ENCODING_AES_KEY', '')
AppId = os.getenv('WECHAT_APP_ID', '')
app.config.update(dict(
    DATABASE=os.path.join(app.root_path, 'weather.db'),
    SECRET_KEY='e35d7f4348184ed6a9aa15adfdb8c6f0' # uuid.uuid4.hex
))
app.config.from_envvar('FLASKR_SETTINGS', silent=True)

def connect_db():
    """Connects to the specific database."""
    parse.uses_netloc.append("postgres")
    url = parse.urlparse(os.environ.get("DATABASE_URL"))
    if url:
        conn = psycopg2.connect(
            database=url.path[1:],
            user=url.username,
            password=url.password,
            host=url.hostname,
            port=url.port
        )
    else:
        conn = psycopg2.connect("dbname=weather user=postgres password=swan port=5432 host=127.0.0.1")
    return conn

def get_db():
    """Opens a new database connection if there is none yet for the
    current application context.
    """
    if not hasattr(g, 'pg_db'):
        g.pg_db = connect_db()
    return g.pg_db
# print(get_db)
@app.teardown_appcontext
def close_db(error):
    """Closes the database again at the end of the request."""
    if hasattr(g, 'pg_db'):
        g.pg_db.close()

def init_db():
    db = get_db()
    cur = db.cursor()
    with app.open_resource('schema.sql', mode='r') as f:
        for sql in f.read().split(';'):
            if sql.strip():
                cur.execute(sql.strip())
    db.commit()


@app.cli.command('initdb')
def initdb_command():
    """Initializes the database."""
    init_db()
    print('Initialized the database.')
def encode_password(password):
    return hashlib.md5(('slat:weatherquery' + password).encode()).hexdigest()

def create_user(username, password):
    raw_password = encode_password(password)
    conn = get_db()
    with conn:
        cur = conn.cursor()
        cur.execute("""INSERT INTO users (username, password) values(%s, %s);
                     """,(username, raw_password))
    conn.commit()

@app.cli.command('initadmin')
def initadmin_command():
    """Initializes the database."""
    create_user("admin", "123456")
    print('Initialized the admin.')
def query_user(username):
    conn = get_db()
    with conn:
        cur = conn.cursor()
        sql_query = """SELECT * FROM users where username='{}' """.format(username)
        cur.execute(sql_query)
        user = cur.fetchone()
        return user
    print(user)
@app.cli.command('queryadmin')
def queryadmin_command():
    """query_admin."""
    print(query_user('admin'))
def query_history(user_id):
    conn = get_db()
    with conn:
        cur = conn.cursor()
        sql_query = """SELECT result from "history" where user_id='{}'""".format(user_id)
        cur.execute(sql_query)
        history = cur.fetchall()
        return history
def isExisted_history(city):
    conn = get_db()
    with conn:
        cur = conn.cursor()
        sql_query = """SELECT result from "history" where city='{}'""".format(city)
        cur.execute(sql_query)
        history = cur.fetchall()
        if len(history) == 0:
            return False
        else:
            return True
def insert_history(user_id, city, result, query_time):
    conn = get_db()
    with conn:
        cur = conn.cursor()
        sql_query = """INSERT INTO "history" (user_id, city, result, query_time)
        values ('{}','{}','{}','{}')""".format(user_id, city, result, query_time)
        cur.execute(sql_query)
    conn.commit()
# add entry
def get_city_weather(location):
    conn = get_db()
    with conn:
        cur = conn.cursor()
        sql_query = """SELECT day,city,weather,temp from weather where city='{}'""".format(location)
        cur.execute(sql_query)
        data = cur.fetchone()
    weather_str = f"""{data[0]},{data[1]}天气:{data[2]},气温:{data[3]}"""
    return weather_str

def update_weather(location, weather):
    conn = get_db()
    with conn:
        cur = conn.cursor()
        sql_query = """UPDATE weather SET weather='{}' where city='{}'""".format(weather, location)
        cur.execute(sql_query)
        # conn.commit()
        sql_query2 = """SELECT * from weather where city='{}'""".format(location)
        cur.execute(sql_query2)
        update_data = cur.fetchall()
    return update_data

def create_table():
    conn = get_db()
    with conn:
        cur = conn.cursor()
        sql_query = """DROP TABLE if exists weather"""
        cur.execute(sql_query)
        sql_query2 = """CREATE TABLE "weather" (
        day varchar(64),
        city varchar(64),
        weather varchar(64),
        temp varchar(64))"""
        cur.execute(sql_query2)
    conn.commit()
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
            create_user(username, password)
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
            user = query_user(username)
            if not user:
                error = '用户不存在'
            else:
                user_password = user[-1]
                if encode_password(password) != user_password:
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
        create_table()
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

# @app.route('/wechat', methods=['GET', 'POST'])
# def wechat():
#     signature = request.args.get('signature', '')
#     timestamp = request.args.get('timestamp', '')
#     nonce = request.args.get('nonce', '')
#     echo_str = request.args.get('echostr', '')
#     encrypt_type = request.args.get('encrypt_type', '')
#     msg_signature = request.args.get('msg_signature', '')

#     print('signature:', signature)
#     print('timestamp: ', timestamp)
#     print('nonce:', nonce)
#     print('echo_str:', echo_str)
#     print('encrypt_type:', encrypt_type)
#     print('msg_signature:', msg_signature)

#     try:
#         check_signature(TOKEN, signature, timestamp, nonce)
#     except InvalidSignatureException:
#         abort(403)
#     if request.method == 'GET':
#         return echo_str
#     else:
#         print('Raw message: \n%s' % request.data)
#         crypto = WeChatCrypto(TOKEN, EncodingAESKey, AppId)
#         try:
#             msg = crypto.decrypt_message(
#                 request.data,
#                 msg_signature,
#                 timestamp,
#                 nonce
#             )
#             print('Descypted message: \n%s' % msg)
#         except (InvalidSignatureException, InvalidAppIdException):
#             abort(403)
#         msg = parse_message(msg)
#         if msg.type == 'text':
#             reply = create_reply(msg.content, msg)
#         else:
#             reply = create_reply('Sorry, can not handle this for now', msg)
#         return crypto.encrypt_message(
#             reply.render(),
#             nonce,
#             timestamp
#         )

if __name__ == '__main__':
    app.run(debug=True)

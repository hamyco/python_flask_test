# coding: utf-8

from flask import Flask, render_template, redirect, request, abort, make_response
import urllib.parse
import requests
import json
import jwt
import os
from datetime import datetime
from argparse import ArgumentParser
import sqlite3
from flask import g


app = Flask(__name__)

DATABASE_FILE = 'db/sqlite_test.db'
TEST_TABLE_NAME = 'test_table'
app.INIT_DONE = False


def init_db():
    db_connection = get_db()
    curs = db_connection.cursor()
    curs.execute('SELECT COUNT(*) FROM sqlite_master WHERE TYPE="table" AND NAME="' + TEST_TABLE_NAME + '"')
    if curs.fetchone() == (0,):
        print('Table not exists! Need to create table')
        curs.execute('create table ' + TEST_TABLE_NAME + '(id INTEGER PRIMARY KEY AUTOINCREMENT, key text, value text)')
    else:
        print('Table exists!')


def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(DATABASE_FILE)
    return db


def read_all_data():
    db_connection = get_db()
    curs = db_connection.cursor()
    sql_str = 'select * from ' + TEST_TABLE_NAME
    curs.execute(sql_str)
    data = curs.fetchall()
    db_connection.close()
    return data


@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        print('db closed')
        db.close()


@app.route('/', methods=['GET'])
def home():
    if not app.INIT_DONE:
        init_db()
        app.INIT_DONE = True

    msg = 'Try the following test:'
    # return name
    return render_template('sqlite_test/sqlite_test_home.html', title='sqlite test', msg=msg)


@app.route('/set_db_data')
def set_db_data():
    return render_template('sqlite_test/set_db_data.html', title='db test')


@app.route('/sql_execute', methods=['POST'])
def sql_execute():
    key = request.form["key"]
    value = request.form["value"]

    db_connection = get_db()
    curs = db_connection.cursor()
    # 'insert into test_sqlite_db(key, value) values("k2", "v2")'
    curs.execute('insert into ' + TEST_TABLE_NAME + '(key, value) values("' + key + '", "' + value + '")')
    db_connection.commit()
    db_connection.close()

    # make_responseでレスポンスオブジェクトを生成する
    if key and value:
        msg = "data <" + key + ',' + value + '> was set!'

    response = make_response(render_template('sqlite_test/sqlite_test_home.html', title='db test', msg=msg))

    max_age = 60 * 5    # 5 min
    expires = int(datetime.now().timestamp()) + max_age

    response.set_cookie(key,
                        value=value,
                        max_age=max_age,
                        expires=expires,
                        secure=True,
                        httponly=True)

    # レスポンスを返す
    return response


@app.route('/get_db_data')
def get_db_data():
    data = read_all_data()
    response = make_response(render_template('sqlite_test/get_db_data.html', data=data))
    return response


# run command: python sqlite.py -p [PORT] -d True -t True -o 127.0.0.1
if __name__ == "__main__":
    arg_parser = ArgumentParser(
        usage='Usage: python ' + __file__ + ' [--port <port>] [--help]'
    )
    arg_parser.add_argument('-p', '--port', type=int, default=5000, help='port')
    arg_parser.add_argument('-d', '--debug', default=False, help='debug')
    arg_parser.add_argument('-t', '--testing', default=False, help='testing mode')
    # If executing program on remote (not localhost), the host needs to be set 0.0.0.0
    arg_parser.add_argument('-o', '--host', type=str, default='0.0.0.0', help='your host')
    options = arg_parser.parse_args()

    if options.debug:
        app.config['TESTING'] = True
    else:
        app.config['TESTING'] = False

    app.run(debug=options.debug, port=options.port, host=options.host)

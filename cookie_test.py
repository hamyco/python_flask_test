# coding: utf-8

from flask import Flask, render_template, redirect, request, abort, session, make_response
import urllib.parse
import requests
import json
import jwt
import os
from datetime import datetime
from argparse import ArgumentParser
from werkzeug.middleware.proxy_fix import ProxyFix
import sqlite3

app = Flask(__name__)


TEST_COOKIE_NAME = '__test_cookie'


@app.route('/', methods=['GET'])
def hello():
    msg = 'Try the following test:'
    # return name
    return render_template('cookie_test/cookie_test_home.html', title='cookie test', msg=msg)


@app.route('/set_cookies')
def set_cookie_test():
    return render_template('cookie_test/set_cookies.html', title='cookie test')



@app.route('/simple_set')
def simple_set():
    content = "**response contents**"

    # make_responseでレスポンスオブジェクトを生成する
    response = make_response(content)

    # Cookieの設定を行う
    max_age = 60 * 60 * 24 * 120 # 120 days
    expires = int(datetime.now().timestamp()) + max_age
    response.set_cookie('uid', value="hogehoge", max_age=max_age, expires=expires, path='/', secure=None, httponly=True)

    # レスポンスを返す
    return response


@app.route('/set_cookies_execute', methods=['POST'])
def set_cookie():
    cookie_name = request.form["cookie_name"]
    cookie_value = request.form["cookie_value"]

    # make_responseでレスポンスオブジェクトを生成する
    #response = make_response(redirect('/?cookie_set=1&cookie_name=' + cookie_name))

    if cookie_name and cookie_value:
        msg = "Cookie <" + cookie_name + '> was set!'

    response = make_response(render_template('cookie_test/cookie_test_home.html', title='cookie test', msg=msg))

    # Cookieの設定を行う
    max_age = 60 * 5    # 5 min
    expires = int(datetime.now().timestamp()) + max_age

    response.set_cookie(cookie_name,
                        value=cookie_value,
                        max_age=max_age,
                        expires=expires,
                        secure=True,
                        httponly=True)

    # レスポンスを返す
    return response


@app.route('/get_cookies')
def get_cookie_test():
    # requestオブジェクトからCookieを取得する
    #cookies = request.cookies.get(TEST_COOKIE_NAME, None)
    cookies = request.cookies.to_dict()
    print(cookies)
    response = make_response(render_template('/cookie_test/get_cookies.html', cookies=cookies))
    return response


# run command: python cookie_test.py -p [PORT] -d True -t True -o 127.0.0.1
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

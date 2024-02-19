import os
import time
import datetime
import json
from logger import logging
import requests
from const import HEADERS, LOGIN_URL, LOGIN_PLAYLOAD, XX_URL
from utils import getExpiresTime
import http.cookiejar as cj


class MisAutoSession():
    def __init__(self):
        self.headers = dict(HEADERS)
        self.session = self.read_cookies_file(self)
        self.filepath = "../data/cookies.txt"
        self.CookiesExpiresTime = getExpiresTime(self.filepath)

    def __del__(self):
        self.session.close()

    def read_cookies_file(self):
        # 读 cookies 文件
        self.session = requests.session()
        self.session.cookies = cj.LWPCookieJar(filename=self.filepath)
        self.session.cookies.load(filename=self.filepath, ignore_discard=True)

    def check_cookie(self):
        today = datetime.datetime.now()
        if today > self.CookiesExpiresTime: #cookies 过期
            # 重新登录
            self.login()
        else:
            resp = self.session.get(XX_URL, headers=HEADERS)
            resp_msg = json.loads(resp.text)['msg']
            if resp_msg == 'TOKEN ERROR':
                self.login()

    def login(self):
        self.session.cookies = cj.LWPCookieJar()
        try:
            resp = self.session.post(LOGIN_URL, headers=HEADERS, json=LOGIN_PLAYLOAD)
            # 保存为cookies
            self.session.cookies.save(filename=self.filepath, ignore_discard=True, ignore_expires=True)
        except Exception as exc:
            # print(f'login = {str(exc)}')
            logging.info(f"MisAutoSession-{str(exc)}")
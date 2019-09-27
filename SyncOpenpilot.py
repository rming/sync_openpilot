#!/usr/bin/env python
#-*- coding:utf-8 -*-

import time
import os
import requests
from pyquery import PyQuery as pq
from dotenv import load_dotenv

class SyncOpenpilot:

    loginUrl = "https://gitee.com/login"
    repoUrls = [
        "https://gitee.com/afaaa/dragonpilot",
        "https://gitee.com/afaaa/openpilot",
        "https://gitee.com/afaaa/kegman",
        "https://gitee.com/afaaa/gernby",
        "https://gitee.com/afaaa/arne182",
    ]

    user   = ""
    passwd = ""

    s      = None

    def __init__(self, user, passwd):
        self.user    = user
        self.passwd  = passwd

    def run(self):
        self.s = requests.Session()
        headers = {
            "Origin"     : "https://gitee.com",
            "User-Agent" : "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.90 Safari/537.36",
        }
        self.s.headers.update(headers)

        r = self.s.get(self.loginUrl);
        d = pq(r.text)
        csrfToken = d('[name="csrf-token"]').attr('content')

        payload = {
            "utf8":"✓",
            "authenticity_token": csrfToken,
            "redirect_to_url": "",
            "redirect_to_url": "",
            "user[login]": self.user,
            "user[password]": self.passwd,
            "user[remember_me]": 1,
        }

        r = self.s.post(self.loginUrl, data=payload)

        # 依次访问项目页面，点击同步github
        print "最后更新时间：%s" % time.strftime("%Y-%m-%d %H:%M:%S")
        for repoUrl in self.repoUrls:
            r = self.s.get(repoUrl)
            d = pq(r.text)
            csrfToken = d('[name="csrf-token"]').attr('content')
            payload = {
                "user_sync_code"     : "",
                "password_sync_code" :"", 
                "sync_wiki"          : "false",
                "authenticity_token" : csrfToken,
            }
            r = self.s.post(repoUrl + "/force_sync_project", data=payload)
            print repoUrl.split("/").pop(), r.text.encode('utf8')


if __name__ == "__main__":
    load_dotenv('.env')
    user   = os.getenv('GITEE_USER')
    passwd = os.getenv('GITEE_PASSWD')
    handler = SyncOpenpilot(user, passwd)
    handler.run()

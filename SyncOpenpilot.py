#!/usr/bin/env python
#-*- coding:utf-8 -*-

import os, time, logging
from dotenv import load_dotenv
from splinter import Browser

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

    logger      = None
    browser     = None
    headless    = False

    def __init__(self, logger, user, passwd):
        self.logger = logger
        self.user   = user
        self.passwd = passwd

    def run(self):
        self.logger.info('initBrowser')
        self.browser = Browser('chrome', headless=self.headless)
        self.browser.visit(self.loginUrl)

        # 填写用户名密码
        self.browser.find_by_name('user[login]').fill(self.user)
        self.browser.find_by_name('user[password]').fill(self.passwd)

        # 点击登陆
        btn = self.browser.find_by_css('input[class="ui fluid orange submit button large"]')
        btn and btn.click()
        time.sleep(1)

        # 依次访问项目页面，点击同步github
        for repoUrl in self.repoUrls:
            self.browser.visit(repoUrl)
            self.logger.info('visit repo %s' % repoUrl)
            btn = self.browser.find_by_id("btn-sync-from-github")
            btn and btn.click()
            time.sleep(1)

            times = 0
            while times < 10:
                times += 1
                btnOK = self.browser.find_by_css('div[class="ui small button orange ok"]')
                self.logger.info(btnOK)
                if btnOK:
                    self.logger.info('sync btn found')
                    self.logger.info(btnOK)
                    btnOK and btnOK.click()
                    time.sleep(1)
                    break
                else:
                    self.logger.error('sync btn not found')
                    time.sleep(1)

        self.browser.quit()

    
if __name__ == "__main__":
    load_dotenv('.env')
    user   = os.getenv('GITEE_USER')
    passwd = os.getenv('GITEE_PASSWD')

    logger = logging.getLogger('SyncOpenpilot')

    fmt       = "[%(asctime)s] %(levelname)s: line %(lineno)d  %(message)s"
    datefmt   = "%Y-%m-%d %H:%M:%S"
    formatter = logging.Formatter(fmt, datefmt)

    stream = logging.StreamHandler(stream=None)
    logger.addHandler(stream)
    stream.setFormatter(formatter)

    logger.setLevel(logging.INFO) 

    handler = SyncOpenpilot(logger, user, passwd)
    handler.run()
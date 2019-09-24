#!/usr/bin/env python
#-*- coding:utf-8 -*-

import os, time, logging
from dotenv import load_dotenv
from splinter import Browser
from xvfbwrapper import Xvfb
from selenium.webdriver.chrome.options import Options


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
    # 是否显示界面
    headless    = True

    def __init__(self, logger, options, user, passwd):
        self.logger  = logger
        self.user    = user
        self.passwd  = passwd
        self.options = options

    def run(self):
        self.logger.info('initBrowser')
        self.browser = Browser('chrome', headless=self.headless, options=self.options)
        self.browser.visit(self.loginUrl)

        # 填写用户名密码
        self.logger.info('doLogin')
        self.browser.find_by_name('user[login]').fill(self.user)
        self.browser.find_by_name('user[password]').fill(self.passwd)

        # 点击登陆
        btn = self.browser.find_by_css('input[class="ui fluid orange submit button large"]')
        btn and btn.click()
        time.sleep(1)

        # 依次访问项目页面，点击同步github
        for repoUrl in self.repoUrls:
            for k in range(0, 3):
                self.visitRepo(repoUrl)
                res = self.clickSync(repoUrl)
                if res: break

        self.browser.quit()


    def visitRepo(self, repoUrl):
        self.browser.visit(repoUrl)
        self.logger.info('visit repo %s' % repoUrl)
        btn = self.browser.find_by_id("btn-sync-from-github")
        btn and btn.click()
        time.sleep(1)
    
    def clickSync(self, repoUrl):
        seconds = 0
        # 每秒查询一下按钮是否可用，10秒超时
        secondsMaxWait = 10
        # 是否点击同步按钮成功
        btnClickSuccess = False
        while seconds <= secondsMaxWait:
            btnOK = self.browser.find_by_css('div[class="ui small button orange ok"]')
            if btnOK:
                self.logger.info('sync btn found')
                btnOK and btnOK.click()
                btnClickSuccess = True
                time.sleep(1)
                break
            else:
                self.logger.error('sync btn not found')
                btnClickSuccess = False
                time.sleep(1)
            seconds = seconds + 1
        return btnClickSuccess

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


    vdisplay = Xvfb()
    vdisplay.start()
    options = Options()
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-setuid-sandbox")
    handler = SyncOpenpilot(logger, options, user, passwd)
    handler.run()
    vdisplay.stop()

## Introduction

因为 github.com 的访问速度较慢，Openpilot 源码较大（~600M），一些分支版本甚至超过1G，这让 Openpilot 的下载安装变得非常痛苦，基于以上原因，需要把 openpilot 相关的项目同步到 gitee，这个脚本，是用于自动登录 gitee 并触发强制同步的。


项目地址：https://doc.sdut.me/mirror.html

## Usage

### 安装依赖

#### 安装 python 依赖

```bash
pip install -r requirements.txt
```

#### 安装 chrome / Xvfb / chromedriver

```bash
# Xvfb
yum install Xvfb

# centos chrome
curl https://intoli.com/install-google-chrome.sh | bash

# 根据 chrome 版本号，下载对应的 chromedriver
# https://sites.google.com/a/chromium.org/chromedriver/downloads
wget https://chromedriver.storage.googleapis.com/77.0.3865.40/chromedriver_linux64.zip
unzip chromedriver_linux64.zip

# 把它放进 PATH 里
mv chromedriver /usr/local/bin/
```

### 修改配置

```bash
# 根据样例复制一份
cp .env.example .env 

# 编辑用户名密码，更新成自己的
vi .env
```

### 运行

```bash
python SyncOpenpilot.py
```

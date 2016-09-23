#!/usr/bin/env python
#coding:utf-8
"""
各个爬虫共享的函数
"""

import os
import hashlib

import requests

#创建文件夹
def makeFolder(folderPath):

    if os.path.exists(folderPath):
        return True
    else:
        os.makedirs(folderPath)
        return True

#下载页面
def downloadPage(url,headers,proxies=None):

    if not proxies:
        r = requests.get(url=url,headers=headers)
    else:
        r = requests.get(url=url,headers=headers,proxies=proxies)
    if r.status_code == 200:
        return r.content
    else:
        return False


#保存页面缓存
def saveHtmlCache(content,path):

    with open(path,'w') as f:
        f.write(content)
    print '文件%s保存完毕'%path

#检测缓存是否存在
def checkExistCache(path):

    if os.path.exists(path):
        return True
    else:
        return False

#获取签名
def getSignName(string):

    return hashlib.sha1(string).hexdigest()

#加载缓存
def loadHtmlCache(path):

    if checkExistCache(path):
        with open(path,'r') as f:
            return f.read()
    else:
        return False





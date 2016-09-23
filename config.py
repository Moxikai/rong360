#!/usr/bin/env python
#coding:utf-8
"""
爬虫基础配置信息

"""
import os

baseDir = os.path.dirname(__file__)
htmlCacheFolder = os.path.join(baseDir,'.cache')
errorInfoFolder = os.path.join(baseDir,'.error')

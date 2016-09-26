#!/usr/bin/env python
#coding:utf-8

import sys
reload(sys)
sys.setdefaultencoding('utf-8')
import os
import time
import hashlib
import copy



from bs4 import BeautifulSoup
import requests


from models import Product,Person,Platform,session


class Rong360():

    def __init__(self):

        self.headers = {'Host':'www.rong360.com',
                        'Cache-Control':'max-age=0',
                        'Upgrade-Insecure-Requests':'1',
                        'User-Agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.116 Safari/537.36',
                        'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
                        'Refer':'http://www.rong360.com/licai/',
                        'Accept-Encoding':'gzip, deflate, sdch',
                        'Accept-Language':'zh-CN,zh;q=0.8',
                        }
        self.baseDir = os.path.dirname(__file__)
        self.htmlCacheFolder = os.path.join(self.baseDir,'.cache')
        #错误信息文件
        self.errorInfoPath = os.path.join(self.baseDir,'errorInfo.txt')
        #下载页面数量
        self.downloadPageCount = 0
        self.downloadPageErrorCount = 0
        self.crawlDataCount = 0
        self.crawlDataErrorCount = 0

    def createFolder(self,path):

        if os.path.exists(path):
            return True
        else:
            os.makedirs(path)
            return True

    def getSignName(self,string):

        if string:
            return hashlib.sha1(string).hexdigest()
        else:
            print '请输入需要签名的字符串'

    def downloadPage(self,url,headers):

        r = requests.get(url=url,headers=headers)
        if r.status_code == 200:
            self.downloadPageCount += 1
            return r.content
        else:
            self.downloadPageErrorCount += 1
            return False


    def saveHtmlCache(self,content,name):

        try:
            path = os.path.join(self.htmlCacheFolder,name+'.html')
            with open(path,'w') as f:
                f.write(content)
            return True
        except Exception as e:
            print '保存网页缓存出错!'
            return False

    def loadHtmlCache(self,name):

        try:
            path = os.path.join(self.htmlCacheFolder,name+'.html')
            with open(path,'r') as f:
                return f.read()
        except Exception as e:
            print '加载缓存出错!',e
            return False

    def checkExistHtmlCache(self,name):
        try:
            path = os.path.join(self.htmlCacheFolder,name+'.html')
            return True if os.path.exists(path) else False
        except Exception as e:
            print '检查缓存是否存在时出错!'

    def getListContent(self,url):

        name = self.getSignName(url)
        if not self.checkExistHtmlCache(name):

            content = self.downloadPage(url,self.headers)
            self.saveHtmlCache(content,name)
        else:

            content = self.loadHtmlCache(name)
        return content

    def parseListContent(self,content):

        if content:
            soup = BeautifulSoup(content,'lxml')
            return [{'pt_name':self.cleanBlank(tr.find('a',class_ = "doc-color-link").get_text()),
                     'pt_url':self.cleanBlank(tr.find('a',class_ = "doc-color-link").get('href')),
                     'pt_grade':self.cleanBlank(tr.find('td',class_ = "pingji").get_text()),
                     'pt_average':self.cleanBlank(tr.find('td',class_ = "average").get_text()),
                     }
                    for tr in soup.find_all('tr') if tr.get('click-url')]

    def getDetailContent(self,url):

        name = self.getSignName(url)
        if not self.checkExistHtmlCache(name):
            headers = copy.deepcopy(self.headers)
            content = self.downloadPage(url,headers)
            self.saveHtmlCache(content,name)
        else:
            content = self.loadHtmlCache(name)
        return content

    def parseDetailBasic(self,content):

        if content:
            soup = BeautifulSoup(content,'lxml')
            for item in soup.find_all('div',class_="wrap-des wrap-clear"):
                pass
                for p in item.find_all('p'):
                    p.get_text()
            basicData = [p.get_text() for item in soup.find_all('div',class_="wrap-left wrap-clear") \
                    for p in item.find_all('p')][1::2]
            try:
                detailData = {'registeredCapital':self.cleanBlank(basicData[0]),
                              'dateSale':self.cleanBlank(basicData[1]),
                              'area':self.cleanBlank(basicData[2]),
                              'url':self.cleanBlank(basicData[3]),
                              'startMoney':self.cleanBlank(basicData[4]),
                              'managementFee':self.cleanBlank(basicData[5]),
                              'cashTakingFee':self.cleanBlank(basicData[6]),
                              'backGround':self.cleanBlank(basicData[7]),
                              'provisionOfRisk':self.cleanBlank(basicData[8]),
                              'foundCustodian':self.cleanBlank(basicData[9]),
                              'safeguardWay':self.cleanBlank(basicData[10]),
                              'assignmentOfDebt':self.cleanBlank(basicData[11]),
                              'automaticBidding':self.cleanBlank(basicData[12]),
                              'cashTime':self.cleanBlank(basicData[13]),

                              'id':self.getSignName(self.cleanBlank(basicData[3]))
                              }
                return detailData
            except Exception as e:
                return {}

    def parseDetailPerson(self,content):

        if content:
            soup = BeautifulSoup(content,'lxml')
            try:
                abstracts = soup.find_all('div',class_='loan-msg-con tab-con')[1].contents
                abstracts = ''.join(str(item) for item in abstracts)

                return {'abstracts':unicode(abstracts,'utf-8')}
            except Exception as e:
                print '人员信息解析有误',e
                return False

    #解析平台简介
    def parseDetailAbstract(self, content):

        if content:
            soup = BeautifulSoup(content, 'lxml')
            try:
                abstracts = soup.find_all('div', class_='loan-msg-con tab-con')[0].contents
                abstracts = ''.join(str(item) for item in abstracts)

                return {'abstract': unicode(abstracts, 'utf-8')}
            except Exception as e:
                print '平台简介信息解析有误!', e
                return False
    #解析产品信息
    def parseProduct(self,content):

        dic = {}
        products = []
        soup = BeautifulSoup(content,'lxml')
        ul = soup.find('ul',class_="loan-product")

        return [{'name':li.find('p',class_='p1').get_text(),
                 'annualizedReturn':li.find('p',class_='p2').find('span').get_text(),
                 'cycle':li.find('p',class_='p3').find('span').get_text(),
                 'remainAmount':li.find('p',class_='p5').get_text(),
                 } for li in ul.find_all('li',class_="wrap-clear")]



    #清理空白元素
    def cleanBlankOfList(self,*args):
        list = []
        for i in args:
            if i:
                list.append(i)
        return list

    #按长度分割成列表
    def splitList(self,length,*args):

        list = []
        list2 = []
        j = 0
        for i in args:
            if j < length:
                list.append(i)
                j += 1
            else:
                list2.append(list)
                list = []
                list.append(i)
                j = 1
        return list2

    #清理字符串空白
    def cleanBlank(self,string):

        return string.replace(' ','').replace('\r','').replace('\n','')

    #保存平台基本信息至数据库
    def saveBasicInfoToSQLite(self,**kwargs):

        platform = Platform(id = kwargs['id'],
                            name = kwargs['name'],
                            gradeFromThird = kwargs['gradeFromThird'],
                            profitAverage = kwargs['profitAverage'],
                            dateSale = kwargs['dateSale'],
                            registeredCapital = kwargs['registeredCapital'],
                            area = kwargs['area'],
                            url = kwargs['area'],
                            startMoney = kwargs['startMoney'],
                            managementFee = kwargs['managementFee'],
                            cashTakingFee = kwargs['cashTakingFee'],
                            backGround = kwargs['backGround'],
                            provisionOfRisk = kwargs['provisionOfRisk'],
                            foundCustodian = kwargs['foundCustodian'],
                            safeguardWay = kwargs['safeguardWay'],
                            assignmentOfDebt = kwargs['assignmentOfDebt'],
                            automaticBidding = kwargs['automaticBidding'],
                            cashTime = kwargs['cashTime'],
                            abstract = kwargs['abstract']
                            )
        if not session.query(Platform).filter(Platform.id == kwargs['id']).first():
            session.add(platform)
            session.commit()
            print '平台-----%s-----基本信息保存成功!'%(kwargs['name'])
        else:
            print '平台-----%s-----基本信息已存在,无需重复保存!'%kwargs['name']

    #保存平台人员信息至数据库
    def savePersonToSQLite(self,**kwargs):

        person = Person(id = kwargs['id'],
                        abstracts = kwargs['abstracts'],
                        platform_id = kwargs['platform_id'])

        if not session.query(Person).filter(Person.id == kwargs['id']).first():

            session.add(person)
            session.commit()
            print '人员-------%s------信息保存成功!'%(kwargs['id'])
        else:
            print '人员-------%s------信息已存在,无需重复保存!'%(kwargs['id'])

    #保存平台产品信息至数据库
    def saveProductToSQLite(self,**kwargs):

        product = Product(id = kwargs['id'],
                          name = kwargs['name'],
                          annualizedReturn = kwargs['annualizedReturn'],
                          cycle = kwargs['cycle'],
                          remainAmount = kwargs['remainAmount'],
                          platform_id = kwargs['platform_id'],
                          )
        if not session.query(Product).filter(Product.id == kwargs['id']).first():

            session.add(product)
            session.commit()
            print '产品-------%s-------信息保存成功!'%kwargs['name']
        else:
            print '产品-------%s--------信息已存在,无需重复保存!'%kwargs['name']
    def run(self):
        url = 'http://www.rong360.com/licai-p2p/pingtai/rating'

        self.createFolder(self.htmlCacheFolder)
        content = self.getListContent(url)
        # 平台列表
        platform_list = self.parseListContent(content)

        if platform_list:
            for platform in platform_list:
                link = platform['pt_url']
                name = platform['pt_name']
                gradeFromThird = platform['pt_grade']
                profitAverage = platform['pt_average']
                # 解析基本信息
                detailContent = self.getDetailContent(link)
                if detailContent:
                    basicInfo = self.parseDetailBasic(detailContent)
                    if basicInfo:
                    # 完善基本信息
                        basicInfo['name'] = name
                        basicInfo['gradeFromThird'] = gradeFromThird
                        basicInfo['profitAverage'] = profitAverage
                        abstract = self.parseDetailAbstract(detailContent)
                        if abstract:
                            basicInfo['abstract'] = abstract['abstract']
                        else:
                            basicInfo['abstract'] = u'暂无数据'
                        # 保存基本信息至数据库
                        self.saveBasicInfoToSQLite(**basicInfo)
                        # 解析人员信息
                        persons = self.parseDetailPerson(detailContent)
                        if persons:
                            # 完善人员信息
                            persons['id'] = basicInfo['id']
                            persons['platform_id'] = basicInfo['id']
                            # 保存人员信息
                            self.savePersonToSQLite(**persons)
                            print '平台%s共有%s个高管,全部成功保存' % (basicInfo['name'], len(persons))
                        else:
                            print '平台-----%s-------网址:%s-------人员信息解析有误,请检查!'%(name,link)

                        # 解析产品信息
                        products = self.parseProduct(detailContent)
                        for product in products:

                            product['id'] = self.getSignName(product['name'])
                            product['platform_id']=basicInfo['id']
                            print product['id'], product['name'], '\n'
                            self.saveProductToSQLite(**product)

                        print '平台%s有%s个最新产品,全部保存成功!' % (basicInfo['name'], len(products))


                else:
                    print '获取详情页面%s失败' % link
        else:
            print '获取页面%s产品列表失败' % url

if __name__ == '__main__':
    pass
    test = Rong360()
    test.run()
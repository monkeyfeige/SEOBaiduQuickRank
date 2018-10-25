# uncompyle6 version 3.2.2
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.6.3 (v3.6.3:2c5fed8, Oct  3 2017, 18:11:49) [MSC v.1900 64 bit (AMD64)]
# Embedded file name: C:\PycharmProjects\AutoOptimize\autooptimize\serviceProxy.py
import json, os
from configparser import ConfigParser
from datetime import datetime
import requests
from autooptimize.globalEnvStorage import GlobalEnvStorage
from autooptimize.model.customerKeyword import CustomerKeyword

class ServiceProxy:

    def __init__(self):
        self.host = GlobalEnvStorage.customerKeywordServerHost
        self.user = GlobalEnvStorage.customerKeywordServerUser
        self.password = GlobalEnvStorage.customerKeywordServerPassword

    def getCustomerKeyword(self, text):
        get = None
        customerKeyword = None
        GlobalEnvStorage.infoLogger.info('%s', text)
        try:
            # url = self.host + '/external/customerkeyword/getCustomerKeyword'
            # param = {'username': self.user,  'password': self.password,  'clientID': clientID,  'version': GlobalEnvStorage.version}
            # get = requests.get(url, params=param, timeout=60)
            # text = get.text
            if text != '':
                customerKeyword = CustomerKeyword()
                customerKeyword.__dict__ = json.loads(json.dumps(text))
                GlobalEnvStorage.infoLogger.info('%s', customerKeyword.keyword)
            return customerKeyword
        except Exception as e:
            raise e
        finally:
            if get:
                get.close()

    def updateOptimizeResult(self, clientID, freeSpace, city):
        GlobalEnvStorage.infoLogger.info('开始更新时间:%s', datetime.now())
        Result = False
        get = None
        try:
            url = self.host + '/external/customerkeyword/updateOptimizedCount'
            customerKeyword = GlobalEnvStorage.customerKeyword
            param = {'username': self.user,  'password': self.password,  'clientID': clientID,  'uuid': customerKeyword.uuid, 
             'count': GlobalEnvStorage.optimizeCount, 
             'freespace': freeSpace,  'version': GlobalEnvStorage.version, 
             'city': city, 
             'status': GlobalEnvStorage.optimizeStatus,  'position': GlobalEnvStorage.baiduMapOrder}
            get = requests.get(url, params=param, timeout=20)
            GlobalEnvStorage.infoLogger.info('%s %s', clientID, get.text)
            if get.text == '1':
                Result = True
            else:
                Result = False
            GlobalEnvStorage.infoLogger.info('更新成功时间:%s', datetime.now())
        except Exception as e:
            GlobalEnvStorage.infoLogger.info('更新失败 %s', e)
            Result = False
        finally:
            if get:
                get.close()
            return Result

    @staticmethod
    def getSpecifiedKeywordNegativeLists():
        get = None
        text = None
        try:
            url = GlobalEnvStorage.customerKeywordServerHost + '/external/negativelist/getSpecifiedKeywordNegativeLists'
            param = {'username': GlobalEnvStorage.customerKeywordServerUser,  'password': GlobalEnvStorage.customerKeywordServerPassword, 
             'keyword': GlobalEnvStorage.customerKeyword.keyword}
            get = requests.get(url, params=param, timeout=10)
            text = get.text
            GlobalEnvStorage.infoLogger.info('获取负面清单成功')
        except Exception as e:
            GlobalEnvStorage.infoLogger.info('负面清单获取失败 %s', e)
        finally:
            if get:
                get.close()
            return text

    @staticmethod
    def updatePageNo(pageNo):
        get = None
        text = None
        try:
            url = GlobalEnvStorage.customerKeywordServerHost + '/external/clientstatus/updatePageNo'
            param = {'username': GlobalEnvStorage.customerKeywordServerUser,  'password': GlobalEnvStorage.customerKeywordServerPassword, 
             'clientID': GlobalEnvStorage.clientID, 
             'pageNo': pageNo}
            get = requests.get(url, params=param, timeout=5)
            text = get.text
        except Exception as e:
            GlobalEnvStorage.infoLogger.info('更新pageNo失败 %s', e)
        finally:
            if get:
                get.close()
            return text

    @staticmethod
    def getNegativeSupportingDataList():
        negativeSupportingDataList = None
        get = None
        try:
            url = GlobalEnvStorage.customerKeywordServerHost + '/external/negativeKeywordName/getNegativeSupportingData'
            param = {'username': GlobalEnvStorage.customerKeywordServerUser,  'password': GlobalEnvStorage.customerKeywordServerPassword}
            get = requests.post(url, timeout=10, json=param)
            negativeSupportingDataList = get.json()['negativeKeywords']
            get.close()
            return negativeSupportingDataList
        except Exception as e:
            GlobalEnvStorage.infoLogger.info('负面清单列表获取失败 %s', e)
        finally:
            if get:
                get.close()
            return negativeSupportingDataList

    @staticmethod
    def checkUpgrade(timeout=10):
        get = None
        try:
            GlobalEnvStorage.infoLogger.info('当前版本是%s', GlobalEnvStorage.version)
            url = GlobalEnvStorage.customerKeywordServerHost + '/external/clientstatus/checkUpgrade'
            param = {'username': GlobalEnvStorage.customerKeywordServerUser,  'password': GlobalEnvStorage.customerKeywordServerPassword, 
             'clientID': GlobalEnvStorage.clientID}
            get = requests.get(url, timeout=timeout, params=param)
            version = get.text
            GlobalEnvStorage.infoLogger.info('目标version:%s', version)
            if get.status_code == requests.codes.ok and version != '' and version != '0':
                cf = ConfigParser()
                cf.read('C:\\working\\env.conf', encoding='utf-8-sig')
                cf.set('Basic', 'fail_num', str(0))
                cf.write(open('C:\\working\\env.conf', 'w', encoding='utf-8'))
                os.system('cd C:\\working && start AutoUpdate.exe')
                os.system('taskkill /f /im ' + 'chrome.exe')
                os.system('taskkill /f /im ' + 'chromedriver.exe')
                os.system('taskkill /f /im ' + 'rasdial.exe')
                os.system('taskkill /f /im ' + 'cmd.exe')
                os.system('taskkill /f /pid ' + str(os.getpid()))
                os.system('taskkill /f /pid ' + str(os.getppid()))
            else:
                GlobalEnvStorage.infoLogger.info('已经是最新版本')
        except Exception as e:
            GlobalEnvStorage.infoLogger.info('获取是否更新失败 %s', e)
        finally:
            if get:
                get.close()
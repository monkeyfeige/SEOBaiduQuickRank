# uncompyle6 version 3.2.2
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.6.3 (v3.6.3:2c5fed8, Oct  3 2017, 18:11:49) [MSC v.1900 64 bit (AMD64)]
# Embedded file name: C:\PycharmProjects\AutoOptimize\autooptimize\operatetarget\abstractOperateTarget.py
import time
from random import randint
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.wait import WebDriverWait
from autooptimize.globalEnvStorage import GlobalEnvStorage
from autooptimize.serviceProxy import ServiceProxy

class AbstractOperateTarget:

    def getRowObjects(self):
        GlobalEnvStorage.infoLogger.info('Please implement getRowObjects')

    def getRowSummaryInfo(self, rowObject):
        GlobalEnvStorage.infoLogger.info('Please implement getRowSummaryInfo')

    def getBaiduMapRowSummaryInfo(self, rowObject, pageNo):
        GlobalEnvStorage.infoLogger.info('Please implement getBaiduMapRowSummaryInfo')

    def nextPage(self):
        GlobalEnvStorage.infoLogger.info('Please implement nextPage')

    def NoResultClick(self, pageNo, rowObjects):
        GlobalEnvStorage.infoLogger.info('Please implement NoResultClick')

    def clickPageNo(self, pageNO):
        GlobalEnvStorage.infoLogger.info('Please implement clickPage')

    def insideClick(self):
        GlobalEnvStorage.infoLogger.info('Please implement insideClick')

    def jingjiaClick(self):
        GlobalEnvStorage.infoLogger.info('Please implement jingjiaClick')

    def prePage(self):
        GlobalEnvStorage.infoLogger.info('Please implement prePage')

    def multiClick(self):
        GlobalEnvStorage.infoLogger.info('Please implement multiClick')

    def moveToTargetElementAndClick(self):
        GlobalEnvStorage.infoLogger.info('Please implement moveToTargetElementAndClick')

    def zhanneiSearch(self):
        GlobalEnvStorage.infoLogger.info('Please implement zhangneiSearch')

    def hasNextPage(self):
        GlobalEnvStorage.infoLogger.info('Please implement hasNextPage')

    def disturbOperate(self):
        GlobalEnvStorage.infoLogger.info('Please implement disturbOperate')

    def initPageSize(self):
        GlobalEnvStorage.infoLogger.info('Please implement initPageSize')

    def xialaclick(self):
        GlobalEnvStorage.infoLogger.info('Please implement xialaclick')

    def decideFile(self):
        GlobalEnvStorage.infoLogger.info('Please implement decideFile')

    def clickxiaoxiala(self, element):
        GlobalEnvStorage.infoLogger.info('Please implement clickxiaoxiala')

    def closeApp(self):
        GlobalEnvStorage.infoLogger.info('Please implement closeApp')

    def operate(self):
        if GlobalEnvStorage.entryUrl != 'https://www.baidu.com' and GlobalEnvStorage.entryUrl != 'https://www.sogou.com' and GlobalEnvStorage.entryUrl != 'https://www.so.com' and GlobalEnvStorage.entryUrl != 'http://www.soku.com':
            if GlobalEnvStorage.customerKeyword.terminalType == 'PC':
                GlobalEnvStorage.newTarget = True
        if GlobalEnvStorage.newTarget:
            waitTime = 0
            while len(GlobalEnvStorage.browser.windows) == 1:
                GlobalEnvStorage.infoLogger.info('wait')
                time.sleep(0.5)
                if waitTime > 10:
                    element = WebDriverWait(GlobalEnvStorage.browser.driver, 20).until(expected_conditions.presence_of_all_elements_located((
                     By.CSS_SELECTOR, GlobalEnvStorage.searchButtom)))[0]
                    GlobalEnvStorage.browserWrapper.locateAndClick(element)
                    break
                else:
                    waitTime += 1

            GlobalEnvStorage.browser.windows.current = GlobalEnvStorage.browser.windows[1]
        else:
            url = GlobalEnvStorage.browser.windows.current.url
            if url == 'https://www.baidu.com/' or url == 'https://www.sogou.com/' or url == 'https://www.so.com/' or url == 'http://www.soku.com/':
                element = WebDriverWait(GlobalEnvStorage.browser.driver, 20).until(expected_conditions.presence_of_all_elements_located((
                 By.CSS_SELECTOR, GlobalEnvStorage.searchButtom)))[0]
                GlobalEnvStorage.browserWrapper.locateAndClick(element)
            if GlobalEnvStorage.customerKeyword.terminalType == 'Phone':
                url = GlobalEnvStorage.browser.windows.current.url
                if url == 'https://m.baidu.com/' or url == 'https://m.sogou.com/' or url == 'http://m.sm.cn/':
                    element = WebDriverWait(GlobalEnvStorage.browser.driver, 20).until(expected_conditions.presence_of_all_elements_located((
                     By.CSS_SELECTOR, GlobalEnvStorage.searchButtom)))[0]
                    GlobalEnvStorage.browserWrapper.locateAndClick(element)
                if GlobalEnvStorage.customerKeyword.searchEngine == '�ٶ�' and GlobalEnvStorage.customerKeyword.terminalType == 'PC' and GlobalEnvStorage.entryUrl != 'https://www.baidu.com':
                    self.initPageSize()
                    time.sleep(2)
                self.zhanneiSearch()
                targetRowObject = None
                totalPageCount = GlobalEnvStorage.customerKeyword.page
                GlobalEnvStorage.Porder = 0
                pageNo = 1
                while targetRowObject == None and pageNo < totalPageCount + 1:
                    time.sleep(2)
                    rowObjects = self.getRowObjects()
                    if rowObjects != None:
                        targetRowObject = self.comparison(rowObjects)
                        self.closeApp()
                        if targetRowObject == None and pageNo < totalPageCount:
                            GlobalEnvStorage.Porder += len(rowObjects)
                            self.jingjiaClick()
                            self.NoResultClick(pageNo, rowObjects)
                            pageNo = pageNo + 1
                            if self.hasNextPage():
                                self.decideFile(pageNo)
                            else:
                                break
                            ServiceProxy.updatePageNo(pageNo=pageNo)
                        else:
                            break
                    else:
                        break

            if targetRowObject != None:
                GlobalEnvStorage.Porder += rowObjects.index(targetRowObject) + 1
                GlobalEnvStorage.infoLogger.info('��ǰ������:%s', GlobalEnvStorage.Porder)
                GlobalEnvStorage.infoLogger.info('�ҵ�')
                n = randint(1, 100)
                if GlobalEnvStorage.customerKeyword.searchEngine != '����' or GlobalEnvStorage.customerKeyword.terminalType != 'Phone' and GlobalEnvStorage.customerKeyword.searchEngine != '�ѹ�':
                    if self.hasNextPage():
                        if n <= int(GlobalEnvStorage.FindFlip_nextPage) and pageNo < totalPageCount:
                            GlobalEnvStorage.infoLogger.info('ǰ����һҳ�ٷ���')
                            self.decideFile(pageNo + 1)
                            ServiceProxy.updatePageNo(pageNo=pageNo + 1)
                            if GlobalEnvStorage.customerKeyword.terminalType == 'PC':
                                time.sleep(1)
                                self.nextPage(pageNo=pageNo)
                            else:
                                time.sleep(2)
                                self.prePage()
                            ServiceProxy.updatePageNo(pageNo=pageNo)
                            time.sleep(1)
                            rowObjects = self.getRowObjects()
                            GlobalEnvStorage.infoLogger.info('%s', len(rowObjects))
                            if rowObjects != None:
                                targetRowObject = self.comparison(rowObjects)
                                if targetRowObject == None:
                                    GlobalEnvStorage.exceptionlogger.exception('���±ȶԺ�ʧȥĿ��')
                                    return
                    if GlobalEnvStorage.customerKeyword.terminalType == 'PC':
                        self.clickxiaoxiala(targetRowObject)
                        self.clickkuaizhao(targetRowObject)
                    self.multiClick(targetRowObject)
                    GlobalEnvStorage.optimizeCount = 1
                    GlobalEnvStorage.optimizeStatus = 'succ'
                else:
                    GlobalEnvStorage.optimizeCount = 0
                    GlobalEnvStorage.optimizeStatus = 'failed'

    def comparison(self, rowObjects):
        targetRowObject = None
        for rowObject in rowObjects:
            GlobalEnvStorage.infoLogger.info('%s', rowObject)
            rowSummaryInfo = self.getRowSummaryInfo(rowObject)
            if rowSummaryInfo is None:
                continue
            if GlobalEnvStorage.customerKeyword.title != None and GlobalEnvStorage.customerKeyword.title != '':
                if rowSummaryInfo.title != None and GlobalEnvStorage.customerKeyword.title in rowSummaryInfo.title:
                    targetRowObject = rowObject
                    GlobalEnvStorage.infoLogger.info('title�ҵ�--')
                    break
            elif rowSummaryInfo.url != None and GlobalEnvStorage.customerKeyword.url in rowSummaryInfo.url:
                targetRowObject = rowObject
                GlobalEnvStorage.infoLogger.info('url�ҵ�--')
                break

        return targetRowObject

    def mapOperate(self):
        targetRowObject = None
        try:
            moreResultElement = WebDriverWait(GlobalEnvStorage.browser.driver, 5).until(expected_conditions.presence_of_all_elements_located((
             By.CSS_SELECTOR, 'li.more-result a')))[0]
            GlobalEnvStorage.browserWrapper.locateAndClick(moreResultElement)
        except Exception as e:
            GlobalEnvStorage.infoLogger.info('û�в鿴ȫ�����%s', e)

        totalPageCount = GlobalEnvStorage.customerKeyword.page
        pageNo = 1
        while 1:
            if targetRowObject == None and pageNo < totalPageCount + 1:
                time.sleep(1)
                rowObjects = self.getRowObjects()
                if rowObjects != None:
                    GlobalEnvStorage.infoLogger.info('%s', len(rowObjects))
                    targetRowObject = self.mapComparison(rowObjects, pageNo)
                    if targetRowObject == None and pageNo < totalPageCount:
                        pageNo = pageNo + 1
                        if self.hasNextPage():
                            break
                        else:
                            self.mapNextPage()
                        ServiceProxy.updatePageNo(pageNo=pageNo)
                    else:
                        break

        if targetRowObject != None:
            GlobalEnvStorage.infoLogger.info('�ҵ�')
            if GlobalEnvStorage.customerKeyword.keyword in '�Ƽ�΢��\t��·���⳵(�����)����������Ħ�����ʵ�Ӱ��Pubtop�ư�(��������ѧԺ��)��˼ͼBASTO(�人M�ӹ������ĵ�)������':
                GlobalEnvStorage.baiduMapOrder = 30
            else:
                GlobalEnvStorage.baiduMapOrder = targetRowObject.order
            self.simpleClick(targetRowObject)
            self.clickSave()
            time.sleep(2)
        else:
            GlobalEnvStorage.baiduMapOrder = 50
            GlobalEnvStorage.optimizeCount = 0
            GlobalEnvStorage.optimizeStatus = 'failed'

    def mapComparison(self, rowObjects, pageNo):
        targetRowObject = None
        for rowObject in rowObjects:
            GlobalEnvStorage.infoLogger.info('%s', rowObject)
            rowSummaryInfo = self.getBaiduMapRowSummaryInfo(rowObject, pageNo)
            if rowSummaryInfo is None:
                continue
            if GlobalEnvStorage.customerKeyword.title != None and GlobalEnvStorage.customerKeyword.title != '':
                if rowSummaryInfo.title != None and GlobalEnvStorage.customerKeyword.title in rowSummaryInfo.title:
                    targetRowObject = rowObject
                    targetRowObject.order = rowSummaryInfo.order
                    GlobalEnvStorage.infoLogger.info('title�ҵ�--')
                    break
                else:
                    continue

        return targetRowObject

    def simpleClick(self, targetRowObject):
        if '_youku' in GlobalEnvStorage.customerKeyword.operationType:
            element = targetRowObject
        else:
            element = targetRowObject.find_elements(By.CSS_SELECTOR, GlobalEnvStorage.selector['title'])[0]
        GlobalEnvStorage.browserWrapper.locateAndClick(element)

    def youkuOperate(self):
        targetRowObject = None
        totalPageCount = GlobalEnvStorage.customerKeyword.page
        pageNo = 1
        while targetRowObject == None and pageNo < totalPageCount + 1:
            time.sleep(1)
            rowObjects = self.getRowObjects()
            if rowObjects != None:
                GlobalEnvStorage.infoLogger.info('%s', len(rowObjects))
                targetRowObject = self.youkuComparison(rowObjects)
                if targetRowObject == None and pageNo < totalPageCount:
                    pageNo = pageNo + 1
                    if self.hasNextPage():
                        self.nextPage()
                    else:
                        break
                    ServiceProxy.updatePageNo(pageNo=pageNo)
                else:
                    break

        if targetRowObject != None:
            GlobalEnvStorage.infoLogger.info('�ҵ�')
            self.simpleClick(targetRowObject)
            time.sleep(2)
            GlobalEnvStorage.browser.windows.current = GlobalEnvStorage.browser.windows[1]
            adTime = int(self.getAdTime())
            time.sleep(adTime + 10)
            GlobalEnvStorage.optimizeCount = 1
            GlobalEnvStorage.optimizeStatus = 'succ'
        else:
            GlobalEnvStorage.optimizeCount = 0
            GlobalEnvStorage.optimizeStatus = 'failed'

    def youkuComparison(self, rowObjects):
        targetRowObject = None
        for rowObject in rowObjects:
            GlobalEnvStorage.infoLogger.info('%s', rowObject)
            rowSummaryInfo = self.getYoukuRowSummaryInfo(rowObject)
            if rowSummaryInfo is None:
                continue
            if GlobalEnvStorage.customerKeyword.title != None and GlobalEnvStorage.customerKeyword.title != '':
                if rowSummaryInfo.title != None and GlobalEnvStorage.customerKeyword.title in rowSummaryInfo.title:
                    targetRowObject = rowObject.find_elements_by_css_selector('div.v-thumb')[0]
                    GlobalEnvStorage.infoLogger.info('title�ҵ�--')
                    break
                else:
                    continue

        return targetRowObject

    def getAdTime(self):
        time.sleep(10)
        adTime = 0
        attempts = 0
        while attempts < 10:
            try:
                adTime = GlobalEnvStorage.browser.evaluate_script("$('.spv-ad-count span').text()")
                break
            except Exception as e:
                GlobalEnvStorage.infoLogger.info('��%�γ���', attempts)

            attempts += 1

        GlobalEnvStorage.infoLogger.info('���ʱ��Ϊ%s', adTime)
        return adTime

    def otherOperate(self):
        targetRowObject = None
        totalPageCount = GlobalEnvStorage.customerKeyword.page
        pageNo = 1
        while targetRowObject == None and pageNo < totalPageCount + 1:
            time.sleep(2)
            rowObjects = self.getRowObjects()
            if rowObjects != None:
                GlobalEnvStorage.infoLogger.info('%s', len(rowObjects))
                targetRowObject = self.comparison(rowObjects)
                if targetRowObject == None and pageNo < totalPageCount:
                    pageNo = pageNo + 1
                    if self.hasNextPage():
                        self.decideFile(pageNo)
                    else:
                        break
                else:
                    break
            else:
                break

        if targetRowObject != None:
            GlobalEnvStorage.infoLogger.info('�ҵ�')
            precent = randint(1, 100)
            if precent < GlobalEnvStorage.customerKeyword.zhanwaiPercent:
                GlobalEnvStorage.infoLogger.info('�ٷ�֮%s���ʵ��', GlobalEnvStorage.customerKeyword.zhanwaiPercent)
                self.multiClick(targetRowObject)
            else:
                GlobalEnvStorage.infoLogger.info('�ٷ�֮%s���ʲ����', 100 - GlobalEnvStorage.customerKeyword.zhanwaiPercent)
            GlobalEnvStorage.optimizeCount = 1
            GlobalEnvStorage.optimizeStatus = 'succ'
        else:
            GlobalEnvStorage.optimizeCount = 0
            GlobalEnvStorage.optimizeStatus = 'failed'
# uncompyle6 version 3.2.2
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.6.3 (v3.6.3:2c5fed8, Oct  3 2017, 18:11:49) [MSC v.1900 64 bit (AMD64)]
# Embedded file name: C:\PycharmProjects\AutoOptimize\autooptimize\operatetarget\baiduPCpictureOperateTarget.py
import time
from random import randint, uniform
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.wait import WebDriverWait
from autooptimize.globalEnvStorage import GlobalEnvStorage
from autooptimize.model.rowSummaryInfo import RowSummaryInfo
from autooptimize.operatetarget.PCOperateTarget import PCOperatetarget

class BaiduPCpictureOperateTarget(PCOperatetarget):

    def operate(self):
        time.sleep(2)
        targetRowObject = None
        totalPageCount = GlobalEnvStorage.customerKeyword.page
        pageNo = 1
        while targetRowObject == None and pageNo < totalPageCount + 1:
            time.sleep(2)
            rowObjects = self.getRowObjects(pageNo=pageNo)
            if rowObjects != None:
                GlobalEnvStorage.infoLogger.info('%s', len(rowObjects))
                targetRowObject = self.comparison(rowObjects)
                if targetRowObject == None and pageNo < totalPageCount:
                    pageNo = pageNo + 1
                    self.nextPage(pageNo)
                else:
                    break
            else:
                break

        if targetRowObject != None:
            GlobalEnvStorage.infoLogger.info('找到')
            self.pictureClick(targetRowObject)
            GlobalEnvStorage.optimizeCount = 1
            GlobalEnvStorage.optimizeStatus = 'succ'
        else:
            GlobalEnvStorage.optimizeCount = 0
            GlobalEnvStorage.optimizeStatus = 'failed'

    def getRowObjects(self, errorTime=0, pageNo=1):
        try:
            RowObjects = WebDriverWait(GlobalEnvStorage.browser.driver, 30).until(expected_conditions.presence_of_all_elements_located((
             By.CSS_SELECTOR, '.imgpage ul.imglist')), message='element获取超时')[pageNo - 1].find_elements_by_css_selector('li.imgitem')
            return RowObjects
        except TimeoutException as e:
            if 'Message: timeout: Timed out receiving message from renderer' in str(e):
                errorTime += 1
                if errorTime <= 2:
                    GlobalEnvStorage.exceptionlogger.exception('第%s次重新加载', errorTime)
                    GlobalEnvStorage.browser.reload()
                    self.getRowObjects(errorTime)
                else:
                    raise Exception('超过重新加载的次数')

    def getRowSummaryInfo(self, rowObject):
        try:
            title = rowObject.get_attribute('data-title')
            url = rowObject.get_attribute('data-objurl')
            rowSummaryInfo = RowSummaryInfo()
            rowSummaryInfo.title = title
            rowSummaryInfo.url = url
            return rowSummaryInfo
        except:
            return

    def comparison(self, rowObjects):
        targetRowObject = None
        for rowObject in rowObjects:
            GlobalEnvStorage.infoLogger.info('%s', rowObject)
            rowSummaryInfo = self.getRowSummaryInfo(rowObject)
            if rowSummaryInfo is None:
                continue
            if rowSummaryInfo.url != None and GlobalEnvStorage.customerKeyword.url in rowSummaryInfo.url:
                targetRowObject = rowObject
                GlobalEnvStorage.infoLogger.info('url找到--')
                break

        return targetRowObject

    def nextPage(self, pageNo):
        while 1:
            GlobalEnvStorage.dmFactory.wheel(count=randint(4, 6))
            time.sleep(2)
            RowObjects = WebDriverWait(GlobalEnvStorage.browser.driver, 30).until(expected_conditions.presence_of_all_elements_located((
             By.CSS_SELECTOR, '.imgpage ul.imglist')), message='element获取超时')
            if len(RowObjects) >= pageNo:
                GlobalEnvStorage.infoLogger.info('下一页完成')
                break

    def pictureClick(self, targetRowObject):
        self.scrolledIntoView(targetRowObject, topMargin=40, bottomMargin=100)
        GlobalEnvStorage.browserWrapper.locateAndClick(targetRowObject, minTime=GlobalEnvStorage.customerKeyword.titleRemainMinTime, maxTime=GlobalEnvStorage.customerKeyword.titleRemainMaxTime)
        time.sleep(uniform(GlobalEnvStorage.customerKeyword.pageRemainMinTime, GlobalEnvStorage.customerKeyword.pageRemainMaxTime))
        waitTime = 0
        while len(GlobalEnvStorage.browser.windows) == 1:
            GlobalEnvStorage.infoLogger.info('wait')
            time.sleep(0.5)
            if waitTime > 10:
                self.moveToTargetElementAndClick(targetRowObject)
                break
            else:
                waitTime += 1

        GlobalEnvStorage.browser.windows.current = GlobalEnvStorage.browser.windows[1]
        passLog = GlobalEnvStorage.browser.driver.find_elements_by_css_selector('#passLog')
        if passLog == []:
            favo = WebDriverWait(GlobalEnvStorage.browser.driver, 30).until(expected_conditions.presence_of_all_elements_located((
             By.CSS_SELECTOR, '.bar-btn.btn-favo')), message='element获取超时')[0]
            GlobalEnvStorage.browserWrapper.locateAndClick(favo)
            okbtn = WebDriverWait(GlobalEnvStorage.browser.driver, 30).until(expected_conditions.presence_of_all_elements_located((
             By.CSS_SELECTOR, '.pop-okbtn')), message='element获取超时')[0]
            GlobalEnvStorage.browserWrapper.locateAndClick(okbtn)
            time.sleep(1)
        if randint(1, 100) <= 50:
            download = WebDriverWait(GlobalEnvStorage.browser.driver, 30).until(expected_conditions.presence_of_all_elements_located((
             By.CSS_SELECTOR, '.bar-btn.btn-download')), message='element获取超时')[0]
            GlobalEnvStorage.browserWrapper.locateAndClick(download)
        time.sleep(uniform(4, 6))
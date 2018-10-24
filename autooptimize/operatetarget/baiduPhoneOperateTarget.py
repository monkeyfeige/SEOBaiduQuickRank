# uncompyle6 version 3.2.2
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.6.3 (v3.6.3:2c5fed8, Oct  3 2017, 18:11:49) [MSC v.1900 64 bit (AMD64)]
# Embedded file name: C:\PycharmProjects\AutoOptimize\autooptimize\operatetarget\baiduPhoneOperateTarget.py
import time
from random import randint, uniform
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.wait import WebDriverWait
from autooptimize.globalEnvStorage import GlobalEnvStorage
from autooptimize.keywordInputFactory import KeywordInputFactory
from autooptimize.model.rowSummaryInfo import RowSummaryInfo
from autooptimize.operatetarget.PhoneOperateTarget import PhoneOperateTarget
from autooptimize.util.util import zhangneiUrl

class BaiduPhoneOperateTarget(PhoneOperateTarget):

    def getRowObjects(self, errorTime=0):
        try:
            RowObjects = WebDriverWait(GlobalEnvStorage.browser.driver, 60).until(expected_conditions.presence_of_all_elements_located((
             By.CSS_SELECTOR, 'div:not([tpl=recommend_list]).result.c-result')), message='element获取超时')
            for RowObject in RowObjects:
                if RowObject.text == '':
                    RowObjects.remove(RowObject)
                    continue

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
            if rowObject.find_elements(By.TAG_NAME, 'h3') == []:
                return
            photoTitle = rowObject.find_elements(By.TAG_NAME, 'h3')[0].text
            if photoTitle.endswith('官网'):
                photoTitle = photoTitle[0:-2]
            if photoTitle.endswith('....'):
                photoTitle = photoTitle[0:-4]
            if photoTitle.endswith('...'):
                photoTitle = photoTitle[0:-3]
            photoTitle = photoTitle.strip()
            url = ''
            if GlobalEnvStorage.customerKeyword.title == None or GlobalEnvStorage.customerKeyword.title == '':
                urlObjs = rowObject.find_elements_by_css_selector('.c-showurl .c-showurl')
                if len(urlObjs) == 0:
                    urlObjs = rowObject.find_elements_by_css_selector('.c-showurl')
                if len(urlObjs) > 0:
                    if len(urlObjs) == 1:
                        url = urlObjs[0].text
                    else:
                        url = urlObjs[0].text + urlObjs[1].text
                    url = url.strip()
                    if url.endswith('...'):
                        url = url[0:-3]
                    url = url.strip()
                    if url.endswith('/'):
                        url = url[0:-1]
                    url = url.strip()
                rowSummaryInfo = RowSummaryInfo()
                rowSummaryInfo.title = photoTitle
                rowSummaryInfo.url = url
                return rowSummaryInfo
        except Exception as e:
            return

    def getNextPageObject(self):
        if GlobalEnvStorage.browser.evaluate_script('$("a.new-nextpage-only")') != []:
            return GlobalEnvStorage.browser.evaluate_script('$("i.c-icon.icon-nextpage")')[0]
        else:
            return GlobalEnvStorage.browser.evaluate_script('$("a.new-nextpage")')[0]

    def prePage(self):
        try:
            element = WebDriverWait(GlobalEnvStorage.browser.driver, 30).until(expected_conditions.presence_of_all_elements_located((
             By.CSS_SELECTOR, 'a.new-prepage')))[0]
            self.scrolledIntoView(element, GlobalEnvStorage.PageMargin_PhoneTopMargin, GlobalEnvStorage.PageMargin_PCBottomMargin)
            GlobalEnvStorage.browserWrapper.locateAndClick(element)
        except BaseException as e:
            GlobalEnvStorage.infoLogger.info('没有找到上一页')
            GlobalEnvStorage.infoLogger.info('%s', e)

    def jingjiaClick(self):
        n = randint(1, 100)
        if n <= GlobalEnvStorage.customerKeyword.baiduSemPercent:
            try:
                jingjia = GlobalEnvStorage.browser.evaluate_script('$(".ec_ad_results >div")')
                n = randint(0, len(jingjia) - 1)
                searchEngineurl = GlobalEnvStorage.browser.windows.current.url
                self.moveToTargetElementAndClick(jingjia[n])
                time.sleep(uniform(GlobalEnvStorage.customerKeyword.pageRemainMinTime, GlobalEnvStorage.customerKeyword.pageRemainMaxTime))
                try:
                    KeywordInputFactory().UrlBack(url=searchEngineurl)
                except:
                    GlobalEnvStorage.infoLogger.info('页面超时继续执行')

            except BaseException as e:
                GlobalEnvStorage.infoLogger.info('没有广告')
                GlobalEnvStorage.infoLogger.info('%s', e)

    def hasNextPage(self):
        return GlobalEnvStorage.browser.is_element_present_by_css('i.c-icon.icon-nextpage') or GlobalEnvStorage.browser.is_element_present_by_css('a.new-nextpage')

    def closeApp(self):
        if GlobalEnvStorage.browser.is_element_present_by_text('打开'):
            element = GlobalEnvStorage.browser.find_by_text('打开')[0]._element.find_element(By.XPATH, './../..').find_elements(By.TAG_NAME, 'div')[0]
            if element.size['width'] != 0:
                GlobalEnvStorage.browserWrapper.locateAndClick(element)

    def zhanneiSearch(self):
        if GlobalEnvStorage.customerKeyword.url is None or GlobalEnvStorage.customerKeyword.url == '':
            return
        time.sleep(2)
        if randint(1, 100) <= GlobalEnvStorage.customerKeyword.zhanneiPercent:
            self.clearInput()
            url = zhangneiUrl(GlobalEnvStorage.customerKeyword.url)
            keywordInputFactory = KeywordInputFactory()
            n = randint(1, 100)
            if n <= 30:
                message = 'site:' + url + ' ' + GlobalEnvStorage.customerKeyword.keyword
            else:
                message = 'inurl:' + url + ' ' + GlobalEnvStorage.customerKeyword.keyword
            keywordInputFactory.inputKeyword(message)
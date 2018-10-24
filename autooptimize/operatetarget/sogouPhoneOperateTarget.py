# uncompyle6 version 3.2.2
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.6.3 (v3.6.3:2c5fed8, Oct  3 2017, 18:11:49) [MSC v.1900 64 bit (AMD64)]
# Embedded file name: C:\PycharmProjects\AutoOptimize\autooptimize\operatetarget\sogouPhoneOperateTarget.py
import time
from random import randint, uniform
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.wait import WebDriverWait
from autooptimize.globalEnvStorage import GlobalEnvStorage
from autooptimize.keywordInputFactory import KeywordInputFactory
from autooptimize.model.rowSummaryInfo import RowSummaryInfo
from autooptimize.operatetarget.PhoneOperateTarget import PhoneOperateTarget
from autooptimize.util.util import zhangneiUrl

class SogouPhoneOperateTarget(PhoneOperateTarget):

    def getRowObjects(self):
        parent = WebDriverWait(GlobalEnvStorage.browser.driver, 30).until(expected_conditions.presence_of_all_elements_located((
         By.CSS_SELECTOR, 'div.results')))[-1]
        return parent.find_elements_by_css_selector('div.vrResult:not(.JS-extquery),div.result')

    def getRowSummaryInfo(self, rowObject):
        try:
            if rowObject.find_elements(By.CSS_SELECTOR, '.resultLink') == []:
                GlobalEnvStorage.Porder -= 1
                return
            phoneTitle = rowObject.find_elements(By.CSS_SELECTOR, '.resultLink')[0].text
            if '\n' in phoneTitle:
                phoneTitle = phoneTitle[0:phoneTitle.find('\n')]
            if phoneTitle.endswith('官网'):
                phoneTitle = phoneTitle[0:-2]
            if phoneTitle.endswith('....'):
                phoneTitle = phoneTitle[0:-4]
            else:
                if phoneTitle.endswith('...'):
                    phoneTitle = phoneTitle[0:-3]
                else:
                    if phoneTitle.endswith('..'):
                        phoneTitle = phoneTitle[0:-2]
            phoneTitle = phoneTitle.strip()
            url = ''
            if GlobalEnvStorage.customerKeyword.title == None or GlobalEnvStorage.customerKeyword.title == '':
                urlObj = rowObject.find_elements_by_css_selector('.citeurl')
                if urlObj != []:
                    url = urlObj[0].text
                    url = url.strip()
                    place = url.find(' - ')
                    if place > 0:
                        url = url[place + 3:]
                    url = url.replace('...', '')
                    url = url.replace('<b>', '')
                    url = url.replace('</b>', '')
                    url = url.replace('&nbsp;', '')
                    if url.endswith('/'):
                        url = url[0:-1]
                rowSummaryInfo = RowSummaryInfo()
                rowSummaryInfo.title = phoneTitle
                rowSummaryInfo.url = url
                return rowSummaryInfo
        except:
            return

    def getNextPageObject(self):
        return GlobalEnvStorage.browser.evaluate_script('$("a#ajax_next_page")')[0]

    def prePage(self):
        try:
            element = WebDriverWait(GlobalEnvStorage.browser.driver, 30).until(expected_conditions.presence_of_all_elements_located((
             By.CSS_SELECTOR, '.sp-rslt-bar')))[-1]
            self.scrolledIntoView(element, GlobalEnvStorage.PageMargin_PhoneTopMargin, GlobalEnvStorage.PageMargin_PCBottomMargin)
        except BaseException as e:
            GlobalEnvStorage.infoLogger.info('没有找到上一页')
            GlobalEnvStorage.infoLogger.info('%s', e)

    def jingjiaClick(self):
        n = randint(1, 100)
        if n <= GlobalEnvStorage.customerKeyword.baiduSemPercent:
            try:
                jingjia = GlobalEnvStorage.browser.evaluate_script('$(".ad_result")')
                n = randint(0, len(jingjia) - 1)
                if jingjia[n].size['width'] == 0:
                    GlobalEnvStorage.infoLogger.info('广告是none')
                    return
                searchEngineurl = GlobalEnvStorage.browser.windows.current.url
                self.moveToTargetElementAndClick(jingjia[n])
                time.sleep(uniform(GlobalEnvStorage.customerKeyword.pageRemainMinTime, GlobalEnvStorage.customerKeyword.pageRemainMaxTime))
                try:
                    keywordInputFactory = KeywordInputFactory()
                    GlobalEnvStorage.dmFactory.dm.MoveTo(250, 40)
                    GlobalEnvStorage.dmFactory.dm.LeftClick()
                    keywordInputFactory.setClipboardData(searchEngineurl)
                    time.sleep(uniform(0.1, 0.3))
                    keywordInputFactory.pasteFromClipboard()
                    time.sleep(uniform(0.1, 0.3))
                    keywordInputFactory.Enter()
                    time.sleep(2)
                except:
                    GlobalEnvStorage.infoLogger.info('页面超时继续执行')

            except BaseException as e:
                GlobalEnvStorage.infoLogger.info('没有广告')
                GlobalEnvStorage.infoLogger.info('%s', e)

    def hasNextPage(self):
        return GlobalEnvStorage.browser.is_element_present_by_css('a.page span')

    def tjOperate(self):
        negetivelist = GlobalEnvStorage.customerKeyword.title.split(',')
        time.sleep(2)
        searchUrl = GlobalEnvStorage.browser.windows.current.url
        self.tjClick('#relativewords div.rw-list .rw-item', negetivelist, searchUrl)
        GlobalEnvStorage.optimizeCount = 1
        GlobalEnvStorage.optimizeStatus = 'succ'

    def closeApp(self):
        if GlobalEnvStorage.browser.is_element_present_by_css('#appad_close'):
            element = GlobalEnvStorage.browser.driver.find_elements_by_css_selector('#appad_close')[0]
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
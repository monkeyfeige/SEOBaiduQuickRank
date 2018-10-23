# uncompyle6 version 3.2.2
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.6.3 (v3.6.3:2c5fed8, Oct  3 2017, 18:11:49) [MSC v.1900 64 bit (AMD64)]
# Embedded file name: C:\PycharmProjects\AutoOptimize\autooptimize\operatetarget\sogouPCOperateTarget.py
import time
from random import randint, uniform
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.wait import WebDriverWait
from autooptimize.globalEnvStorage import GlobalEnvStorage
from autooptimize.keywordInputFactory import KeywordInputFactory
from autooptimize.model.rowSummaryInfo import RowSummaryInfo
from autooptimize.operatetarget.PCOperateTarget import PCOperatetarget
from autooptimize.searchFactory import SearchFactory
from autooptimize.util.util import zhangneiUrl

class SogouPCOperateTarget(PCOperatetarget):

    def initPageSize(self):
        if GlobalEnvStorage.entryUrl == 'https://www.sogou.com' and GlobalEnvStorage.customerKeyword.pageSize != GlobalEnvStorage.profileIDCountList[str(GlobalEnvStorage.profileID)]['pageSize']:
            settings = WebDriverWait(GlobalEnvStorage.browser.driver, 30).until(expected_conditions.presence_of_all_elements_located((By.CSS_SELECTOR, '#settings')))[-1]
            GlobalEnvStorage.browserWrapper.locateAndClick(settings)
            setpref = GlobalEnvStorage.browser.evaluate_script('$("#search-settings")')[0]
            GlobalEnvStorage.browserWrapper.locateAndClick(setpref)
            time.sleep(2)
            nr = GlobalEnvStorage.browser.evaluate_script('$("#settings-number")')[0]
            GlobalEnvStorage.browserWrapper.locateAndClick(nr)
            list = GlobalEnvStorage.browser.evaluate_script('$("#settings-number-list")')[0]
            options = list.find_elements_by_tag_name('li')
            info = GlobalEnvStorage.browserWrapper.getElementLocationInfo(nr)
            for idx in range(len(options)):
                if str(GlobalEnvStorage.customerKeyword.pageSize) in options[idx].text:
                    GlobalEnvStorage.dmFactory.simulateTrajectory(info['x'] + randint(int(info['width'] * 0.2), int(info['width'] * 0.8)), info['y'] + GlobalEnvStorage.toolBarHeight + randint(int(info['height'] * 0.2), int(info['height'] * 0.5)) + (idx + 1) * info['height'])
                    break

            save = GlobalEnvStorage.browser.evaluate_script('$("#settings-save")')[0]
            GlobalEnvStorage.browserWrapper.locateAndClick(save)
            time.sleep(uniform(1, 2))
            GlobalEnvStorage.profileIDCountList[str(GlobalEnvStorage.profileID)]['pageSize'] = GlobalEnvStorage.customerKeyword.pageSize
            GlobalEnvStorage.infoLogger.info('设置一页多少条成功')

    def getRowSummaryInfo(self, rowObject):
        try:
            title = rowObject.find_elements(By.CSS_SELECTOR, 'h3 a')[0].text
            if title.endswith('....'):
                title = title[0:-4]
            if title.endswith('...'):
                title = title[0:-3]
            title = title.strip()
            url = ''
            if GlobalEnvStorage.customerKeyword.title == None or GlobalEnvStorage.customerKeyword.title == '':
                urlObjs = rowObject.find_elements_by_css_selector('cite')
                if len(urlObjs) > 0:
                    url = urlObjs[0].text
                    url = url.strip()
                    if url.count(' - ') == 2:
                        url = url[url.find(' - ') + 3:]
                        url = url[0:url.find(' - ')]
                    else:
                        if url.count(' - ') == 1:
                            url = url[0:url.find(' - ')]
                    url = url.replace('...', '')
                    url = url.replace('<b>', '')
                    url = url.replace('</b>', '')
                    url = url.replace('&nbsp;', '')
                    if url.endswith('/'):
                        url = url[0:-1]
                rowSummaryInfo = RowSummaryInfo()
                rowSummaryInfo.title = title
                rowSummaryInfo.url = url
                return rowSummaryInfo
        except:
            return

    def zhanneiSearch(self):
        if GlobalEnvStorage.customerKeyword.url is None or GlobalEnvStorage.customerKeyword.url == '':
            return
        zhanneiPercent = randint(1, 100)
        time.sleep(uniform(0.5, 1))
        if GlobalEnvStorage.customerKeyword.terminalType == 'PC' and zhanneiPercent <= GlobalEnvStorage.customerKeyword.zhanneiPercent:
            url = zhangneiUrl(GlobalEnvStorage.customerKeyword.url)
            keywordInputFactory = KeywordInputFactory()
            settings = WebDriverWait(GlobalEnvStorage.browser.driver, 20).until(expected_conditions.presence_of_all_elements_located((By.CSS_SELECTOR, '#settings')))[0]
            GlobalEnvStorage.browserWrapper.locateAndClick(settings)
            advancedSearch = WebDriverWait(GlobalEnvStorage.browser.driver, 10).until(expected_conditions.presence_of_all_elements_located((By.CSS_SELECTOR, '#advanced-search')))[0]
            GlobalEnvStorage.browserWrapper.locateAndClick(advancedSearch)
            time.sleep(uniform(0.5, 1))
            adv_keyword = WebDriverWait(GlobalEnvStorage.browser.driver, 10).until(expected_conditions.presence_of_all_elements_located((By.CSS_SELECTOR, '[name=q]')))[0]
            if adv_keyword.get_attribute('value') == '':
                GlobalEnvStorage.browserWrapper.locateAndClick(adv_keyword)
                keywordInputFactory = KeywordInputFactory()
                if GlobalEnvStorage.customerKeyword.supportPaste == 1:
                    n = randint(1, 100)
                    if n <= int(GlobalEnvStorage.inputMethod_paste):
                        keywordInputFactory.setClipboardData(GlobalEnvStorage.customerKeyword.keyword)
                        keywordInputFactory.pasteFromClipboard()
                    else:
                        keywordInputFactory.inputWords(GlobalEnvStorage.customerKeyword.keyword)
                else:
                    keywordInputFactory.inputWords(GlobalEnvStorage.customerKeyword.keyword)
            urlElement = GlobalEnvStorage.browser.driver.find_elements_by_css_selector('[name=sitequery]')[0]
            GlobalEnvStorage.browserWrapper.locateAndClick(urlElement)
            if GlobalEnvStorage.customerKeyword.supportPaste == 1:
                n = randint(1, 100)
                if n <= int(GlobalEnvStorage.inputMethod_paste):
                    keywordInputFactory.setClipboardData(url)
                    keywordInputFactory.pasteFromClipboard()
                else:
                    keywordInputFactory.inputWords(url)
            else:
                keywordInputFactory.inputWords(url)
            SearchFactory().search(searchButtom='#adv-search-btn')
            while 1:
                if len(GlobalEnvStorage.browser.windows) == 1:
                    GlobalEnvStorage.infoLogger.info('wait')
                    time.sleep(1)

            GlobalEnvStorage.browser.windows.current = GlobalEnvStorage.browser.windows[-1]
# uncompyle6 version 3.2.2
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.6.3 (v3.6.3:2c5fed8, Oct  3 2017, 18:11:49) [MSC v.1900 64 bit (AMD64)]
# Embedded file name: C:\PycharmProjects\AutoOptimize\autooptimize\operatetarget\_360PCOperateTarget.py
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

class _360PCOperateTarget(PCOperatetarget):

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
        if GlobalEnvStorage.customerKeyword.terminalType == 'PC' and zhanneiPercent <= GlobalEnvStorage.customerKeyword.zhanneiPercent:
            url = zhangneiUrl(GlobalEnvStorage.customerKeyword.url)
            keywordInputFactory = KeywordInputFactory()
            settings = WebDriverWait(GlobalEnvStorage.browser.driver, 20).until(expected_conditions.presence_of_all_elements_located((By.CSS_SELECTOR, '.show-list.setting-group')))[0]
            GlobalEnvStorage.browserWrapper.locateAndClick(settings)
            advancedSearch = WebDriverWait(GlobalEnvStorage.browser.driver, 10).until(expected_conditions.presence_of_all_elements_located((By.CSS_SELECTOR, '#advanced_search')))[0]
            GlobalEnvStorage.browserWrapper.locateAndClick(advancedSearch)
            time.sleep(uniform(1, 2))
            urlElement = GlobalEnvStorage.browser.driver.find_elements_by_css_selector('.input.site')[0]
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
            SearchFactory().search(searchButtom='.btn.search')
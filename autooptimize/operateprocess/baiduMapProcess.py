# uncompyle6 version 3.2.2
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.6.3 (v3.6.3:2c5fed8, Oct  3 2017, 18:11:49) [MSC v.1900 64 bit (AMD64)]
# Embedded file name: C:\PycharmProjects\AutoOptimize\autooptimize\operateprocess\baiduMapProcess.py
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.wait import WebDriverWait
from autooptimize.browser.browserFactory import BrowserFactory
from autooptimize.globalEnvStorage import GlobalEnvStorage
from autooptimize.keywordInputFactory import KeywordInputFactory
from autooptimize.operateprocess.abstractProcess import AbstractProcess
from autooptimize.operatetarget.operateTargetFactory import OperateTargetFactory
from autooptimize.urlInputFactory import UrlInputFactory
from autooptimize.util.util import clearCookie, profileIDKeywordCount

class BaiduMapProcess(AbstractProcess):

    def execute(self):
        browserFactory = BrowserFactory()
        keywordInputFactory = KeywordInputFactory()
        if GlobalEnvStorage.cookiesProfileList.get(str(GlobalEnvStorage.profileID)) == None:
            GlobalEnvStorage.cookiesProfileList[str(GlobalEnvStorage.profileID)] = []
        while GlobalEnvStorage.customerKeyword.keyword in GlobalEnvStorage.cookiesProfileList[str(GlobalEnvStorage.profileID)]:
            count = 0
            if GlobalEnvStorage.profileID == 301:
                GlobalEnvStorage.profileID = 0
                count += 1
                if count > 301:
                    GlobalEnvStorage.exceptionlogger.error('%s已经刷完', GlobalEnvStorage.customerKeyword.keyword)
                    break
            else:
                GlobalEnvStorage.profileID += 1

        browserFactory.initBrowser()
        profileIDKeywordCount()
        urlInputFactory = UrlInputFactory()
        GlobalEnvStorage.entryUrl = 'https://www.baidu.com'
        urlInputFactory.input()
        GlobalEnvStorage.searchText = '#sole-input'
        GlobalEnvStorage.searchButtom = '#search-button'
        GlobalEnvStorage.dropDownList = '.ui3-suggest-item'
        GlobalEnvStorage.selector['rowobjects'] = '.search-item'
        GlobalEnvStorage.selector['page_text'] = '添加该地点'
        GlobalEnvStorage.selector['title'] = 'div.row a'
        GlobalEnvStorage.selector['page'] = 'p.page'
        GlobalEnvStorage.browser.visit('http://map.baidu.com')
        operateTargetFactory = OperateTargetFactory()
        if GlobalEnvStorage.customerKeyword.url != 'no':
            keywordInputFactory.inputKeyword(GlobalEnvStorage.customerKeyword.url)
            placeInput = WebDriverWait(GlobalEnvStorage.browser.driver, 10).until(expected_conditions.presence_of_all_elements_located((
             By.CSS_SELECTOR, '.loading-button.cancel-button')))[0]
            GlobalEnvStorage.browserWrapper.locateAndClick(placeInput)
        keywordInputFactory.inputKeyword(GlobalEnvStorage.customerKeyword.keyword)
        operateTargetFactory.operate()
        clearCookie()
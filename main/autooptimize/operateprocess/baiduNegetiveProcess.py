# uncompyle6 version 3.2.2
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.6.3 (v3.6.3:2c5fed8, Oct  3 2017, 18:11:49) [MSC v.1900 64 bit (AMD64)]
# Embedded file name: C:\PycharmProjects\AutoOptimize\autooptimize\operateprocess\baiduNegetiveProcess.py
import time
from random import uniform
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.wait import WebDriverWait
from autooptimize.browser.browserFactory import BrowserFactory
from autooptimize.globalEnvStorage import GlobalEnvStorage
from autooptimize.keywordInputFactory import KeywordInputFactory
from autooptimize.operateprocess.abstractProcess import AbstractProcess
from autooptimize.operatetarget.baiduPCOperateTarget import BaiduPCOperateTarget
from autooptimize.operatetarget.operateTargetFactory import OperateTargetFactory
from autooptimize.searchFactory import SearchFactory
from autooptimize.urlInputFactory import UrlInputFactory
from autooptimize.util.util import profileIDKeywordCount, clearCookie

class BaiduNegetiveProcess(AbstractProcess):

    def execute(self):
        browserFactory = BrowserFactory()
        keywordInputFactory = KeywordInputFactory()
        browserFactory.initBrowser()
        profileIDKeywordCount()
        urlInputFactory = UrlInputFactory()
        urlInputFactory.input()
        if GlobalEnvStorage.customerKeyword.terminalType == 'PC':
            BaiduPCOperateTarget().initPageSize()
        print('inputKeyword', GlobalEnvStorage.customerKeyword.keyword)
        print('GlobalEnvStorage.searchText', GlobalEnvStorage.searchText)
        element = WebDriverWait(GlobalEnvStorage.browser.driver, 10).until(expected_conditions.presence_of_all_elements_located((By.CSS_SELECTOR, GlobalEnvStorage.searchText)))[0]
        GlobalEnvStorage.browserWrapper.locateAndClick(element)
        time.sleep(uniform(0.4, 0.8))
        keywordInputFactory.inputWords(GlobalEnvStorage.customerKeyword.keyword)
        SearchFactory().search()
        operateTargetFactory = OperateTargetFactory()
        operateTargetFactory.operate()
        clearCookie()
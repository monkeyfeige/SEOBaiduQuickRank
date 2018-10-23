# uncompyle6 version 3.2.2
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.6.3 (v3.6.3:2c5fed8, Oct  3 2017, 18:11:49) [MSC v.1900 64 bit (AMD64)]
# Embedded file name: C:\PycharmProjects\AutoOptimize\autooptimize\operateprocess\baiduPictureProcess.py
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

class BaiduPictureProcess(AbstractProcess):

    def execute(self):
        browserFactory = BrowserFactory()
        keywordInputFactory = KeywordInputFactory()
        browserFactory.initBrowser()
        newProfile = profileIDKeywordCount()
        urlInputFactory = UrlInputFactory()
        GlobalEnvStorage.entryUrl = 'http://image.baidu.com'
        urlInputFactory.input(newProfile=newProfile)
        GlobalEnvStorage.searchText = '#kw'
        GlobalEnvStorage.searchButtom = '.s_search'
        GlobalEnvStorage.dropDownList = '#sugWrapper li.item'
        GlobalEnvStorage.selector['rowobjects'] = '.imgpage .imglist.clearfix li'
        operateTargetFactory = OperateTargetFactory()
        keywordInputFactory.inputKeyword(GlobalEnvStorage.customerKeyword.keyword)
        operateTargetFactory.operate()
        clearCookie()
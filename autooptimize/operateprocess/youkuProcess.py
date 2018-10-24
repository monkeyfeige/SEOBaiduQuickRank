# uncompyle6 version 3.2.2
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.6.3 (v3.6.3:2c5fed8, Oct  3 2017, 18:11:49) [MSC v.1900 64 bit (AMD64)]
# Embedded file name: C:\PycharmProjects\AutoOptimize\autooptimize\operateprocess\youkuProcess.py
from autooptimize.browser.browserFactory import BrowserFactory
from autooptimize.globalEnvStorage import GlobalEnvStorage
from autooptimize.keywordInputFactory import KeywordInputFactory
from autooptimize.operateprocess.abstractProcess import AbstractProcess
from autooptimize.operatetarget.operateTargetFactory import OperateTargetFactory
from autooptimize.urlInputFactory import UrlInputFactory
from autooptimize.util.util import clearCookie, profileIDKeywordCount

class YoukuProcess(AbstractProcess):

    def execute(self):
        browserFactory = BrowserFactory()
        browserFactory.initBrowser()
        profileIDKeywordCount()
        keywordInputFactory = KeywordInputFactory()
        urlInputFactory = UrlInputFactory()
        GlobalEnvStorage.searchText = '.sotxt'
        GlobalEnvStorage.searchButtom = '.btn.btn_search'
        GlobalEnvStorage.dropDownList = 'ul.autolist a'
        GlobalEnvStorage.selector['rowobjects'] = 'div.v'
        GlobalEnvStorage.selector['page_text'] = '下一页'
        GlobalEnvStorage.selector['title'] = 'div.v-meta-title a'
        GlobalEnvStorage.selector['page'] = 'li.next'
        urlInputFactory.input('http://www.soku.com')
        keywordInputFactory.inputKeyword(GlobalEnvStorage.customerKeyword.keyword)
        operateTargetFactory = OperateTargetFactory()
        operateTargetFactory.operate()
        clearCookie()
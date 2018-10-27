# uncompyle6 version 3.2.2
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.6.3 (v3.6.3:2c5fed8, Oct  3 2017, 18:11:49) [MSC v.1900 64 bit (AMD64)]
# Embedded file name: C:\PycharmProjects\AutoOptimize\autooptimize\operateprocess\sogouOtherProcess.py
from autooptimize.browser.browserFactory import BrowserFactory
from autooptimize.globalEnvStorage import GlobalEnvStorage
from autooptimize.operateprocess.abstractProcess import AbstractProcess
from autooptimize.operatetarget.operateTargetFactory import OperateTargetFactory
from autooptimize.operatetarget.sogouPCOperateTarget import SogouPCOperateTarget
from autooptimize.urlInputFactory import UrlInputFactory
from autooptimize.util.util import clearCookie, profileIDKeywordCount, zhangneiUrl

class SogouOtherProcess(AbstractProcess):

    def execute(self):
        GlobalEnvStorage.infoLogger.info('开始执行SogouOtherProcess...')
        browserFactory = BrowserFactory()
        browserFactory.initBrowser()
        profileIDKeywordCount()
        urlInputFactory = UrlInputFactory()
        url = 'http://www.sogou.com/tx'
        zhangneiurl = zhangneiUrl(GlobalEnvStorage.customerKeyword.url)
        url = url + '?site=' + zhangneiurl + '&query=' + GlobalEnvStorage.customerKeyword.keyword
        urlInputFactory.input(url)
        operateTargetFactory = OperateTargetFactory()
        operateTargetFactory.operate()
        clearCookie()
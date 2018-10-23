# uncompyle6 version 3.2.2
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.6.3 (v3.6.3:2c5fed8, Oct  3 2017, 18:11:49) [MSC v.1900 64 bit (AMD64)]
# Embedded file name: C:\PycharmProjects\AutoOptimize\autooptimize\operateprocess\_360OtherProcess.py
from random import randint
from autooptimize.browser.browserFactory import BrowserFactory
from autooptimize.globalEnvStorage import GlobalEnvStorage
from autooptimize.operateprocess.abstractProcess import AbstractProcess
from autooptimize.operatetarget.operateTargetFactory import OperateTargetFactory
from autooptimize.urlInputFactory import UrlInputFactory
from autooptimize.util.util import clearCookie, profileIDKeywordCount, zhangneiUrl

class _360OtherProcess(AbstractProcess):

    def execute(self):
        browserFactory = BrowserFactory()
        browserFactory.initBrowser()
        profileIDKeywordCount()
        GlobalEnvStorage.customerKeyword.zhanneiPercent = 0
        urlInputFactory = UrlInputFactory()
        n = randint(1, 5)
        if n == 1:
            url = 'https://www.so.com/s?src=se7_toolbar'
        else:
            if n == 2:
                url = 'https://www.so.com/s?src=hao_360so_button'
            else:
                if n == 3:
                    url = 'https://www.so.com/s?src=srp&fr=so.com'
                else:
                    if n == 4:
                        url = 'https://www.so.com/s?src=srp&fr=so.com'
                    else:
                        url = 'https://www.so.com/s?src=so.com'
                    zhangneiurl = zhangneiUrl(GlobalEnvStorage.customerKeyword.url)
                    url = url + '&q=' + GlobalEnvStorage.customerKeyword.keyword + '&rg=1' + '&site=' + zhangneiurl
                    urlInputFactory.input(url)
                    operateTargetFactory = OperateTargetFactory()
                    operateTargetFactory.operate()
                    clearCookie()
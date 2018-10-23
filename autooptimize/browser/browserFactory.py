# uncompyle6 version 3.2.2
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.6.3 (v3.6.3:2c5fed8, Oct  3 2017, 18:11:49) [MSC v.1900 64 bit (AMD64)]
# Embedded file name: C:\PycharmProjects\AutoOptimize\autooptimize\browser\browserFactory.py
from random import randint
from autooptimize.browser.pcBrowser import PCBrowser
from autooptimize.browser.phoneBrowser import PhoneBrowser
from autooptimize.globalEnvStorage import GlobalEnvStorage
from autooptimize.keywordInputFactory import KeywordInputFactory

class BrowserFactory:
    browser = None

    def initBrowser(self):
        if GlobalEnvStorage.customerKeyword.terminalType == 'Phone':
            browser = PhoneBrowser()
        else:
            browser = PCBrowser()
        browser.initBrowser()
        GlobalEnvStorage.browserWrapper = browser

    @staticmethod
    def closeLast(current_window_title):
        if len(GlobalEnvStorage.browser.driver.window_handles) >= 8:
            closeNum = randint(2, len(GlobalEnvStorage.browser.driver.window_handles) - 6)
            for idx in range(closeNum):
                GlobalEnvStorage.browser.windows.current = GlobalEnvStorage.browser.windows[-1]
                GlobalEnvStorage.browser.windows.current.close()

            for idx in range(len(GlobalEnvStorage.browser.windows)):
                if GlobalEnvStorage.browser.windows[idx].title == current_window_title:
                    GlobalEnvStorage.browser.windows.current = GlobalEnvStorage.browser.windows[idx]
                    KeywordInputFactory.Ctrl_Number(idx + 1)
                    break
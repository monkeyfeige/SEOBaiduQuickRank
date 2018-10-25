# uncompyle6 version 3.2.2
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.6.3 (v3.6.3:2c5fed8, Oct  3 2017, 18:11:49) [MSC v.1900 64 bit (AMD64)]
# Embedded file name: C:\PycharmProjects\AutoOptimize\autooptimize\operateprocess\baiduSnapshotProcess.py
from random import randint, choice
from autooptimize.browser.browserFactory import BrowserFactory
from autooptimize.globalEnvStorage import GlobalEnvStorage
from autooptimize.keywordInputFactory import KeywordInputFactory
from autooptimize.operateprocess.abstractProcess import AbstractProcess
from autooptimize.operatetarget.baiduPCOperateTarget import BaiduPCOperateTarget
from autooptimize.operatetarget.operateTargetFactory import OperateTargetFactory
from autooptimize.urlInputFactory import UrlInputFactory
from autooptimize.util.util import clearCookie, profileIDKeywordCount

class BaiduSnapshotProcess(AbstractProcess):

    def execute(self):
        browserFactory = BrowserFactory()
        browserFactory.initBrowser()
        newProfile = profileIDKeywordCount()
        urlInputFactory = UrlInputFactory()
        urlInputFactory.input(newProfile=newProfile)
        if GlobalEnvStorage.customerKeyword.terminalType == 'PC' and GlobalEnvStorage.entryUrl == 'https://www.baidu.com':
            BaiduPCOperateTarget().initPageSize()
        if randint(1, 100) <= 40:
            disturbType = 8
            if disturbType == 1:
                GlobalEnvStorage.hasNextWord = True
                self.disturb(type=0)
                GlobalEnvStorage.hasNextWord = False
                self.notDisturb()
            elif disturbType == 2:
                GlobalEnvStorage.hasNextWord = True
                self.notDisturb()
                if GlobalEnvStorage.optimizeCount == 1:
                    GlobalEnvStorage.hasNextWord = False
                    self.disturb(type=0)
            elif disturbType == 3:
                GlobalEnvStorage.hasNextWord = True
                self.disturb(type=1)
                GlobalEnvStorage.hasNextWord = False
                self.notDisturb()
            elif disturbType == 4:
                GlobalEnvStorage.hasNextWord = True
                self.notDisturb()
                if GlobalEnvStorage.optimizeCount == 1:
                    GlobalEnvStorage.hasNextWord = False
                    self.disturb(type=1)
            elif disturbType == 5:
                GlobalEnvStorage.hasNextWord = True
                self.notDisturb()
                if GlobalEnvStorage.optimizeCount == 1:
                    self.disturb(type=0)
                    GlobalEnvStorage.hasNextWord = False
                    self.disturb(type=1)
            elif disturbType == 6:
                GlobalEnvStorage.hasNextWord = True
                self.notDisturb()
                if GlobalEnvStorage.optimizeCount == 1:
                    self.disturb(type=1)
                    GlobalEnvStorage.hasNextWord = False
                    self.disturb(type=0)
            elif disturbType == 7:
                GlobalEnvStorage.hasNextWord = True
                self.disturb(type=0)
                self.notDisturb()
                if GlobalEnvStorage.optimizeCount == 1:
                    GlobalEnvStorage.hasNextWord = False
                    self.disturb(type=1)
            elif disturbType == 8:
                GlobalEnvStorage.hasNextWord = True
                self.disturb(type=0)
                self.disturb(type=1)
                GlobalEnvStorage.hasNextWord = False
                self.notDisturb()
            elif disturbType == 9:
                GlobalEnvStorage.hasNextWord = True
                self.disturb(type=1)
                self.notDisturb()
                if GlobalEnvStorage.optimizeCount == 1:
                    GlobalEnvStorage.hasNextWord = False
                    self.disturb(type=0)
            else:
                GlobalEnvStorage.hasNextWord = True
                self.disturb(type=1)
                self.disturb(type=0)
                GlobalEnvStorage.hasNextWord = False
                self.notDisturb()
        else:
            self.notDisturb()
        clearCookie()

    def disturb(self, type=0):
        operateTargetFactory = OperateTargetFactory()
        if KeywordInputFactory().disturbInput(type) != False:
            operateTargetFactory.disturbOperate()

    def notDisturb(self):
        KeywordInputFactory().inputKeyword(GlobalEnvStorage.customerKeyword.keyword)
        operateTargetFactory = OperateTargetFactory()
        operateTargetFactory.operate()
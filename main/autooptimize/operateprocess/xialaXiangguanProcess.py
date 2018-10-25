# uncompyle6 version 3.2.2
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.6.3 (v3.6.3:2c5fed8, Oct  3 2017, 18:11:49) [MSC v.1900 64 bit (AMD64)]
# Embedded file name: C:\PycharmProjects\AutoOptimize\autooptimize\operateprocess\xialaXiangguanProcess.py
from autooptimize.browser.browserFactory import BrowserFactory
from autooptimize.operateprocess.abstractProcess import AbstractProcess
from autooptimize.operatetarget.operateTargetFactory import OperateTargetFactory
from autooptimize.util.util import clearCookie

class XialaXiangguanProcess(AbstractProcess):

    def execute(operateTarget):
        browserFactory = BrowserFactory()
        browserFactory.initBrowser()
        operateTargetFactory = OperateTargetFactory()
        operateTargetFactory.operate()
        clearCookie()
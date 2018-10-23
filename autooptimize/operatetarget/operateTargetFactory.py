# uncompyle6 version 3.2.2
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.6.3 (v3.6.3:2c5fed8, Oct  3 2017, 18:11:49) [MSC v.1900 64 bit (AMD64)]
# Embedded file name: C:\PycharmProjects\AutoOptimize\autooptimize\operatetarget\operateTargetFactory.py
from autooptimize.globalEnvStorage import GlobalEnvStorage
from autooptimize.operatetarget._360PCOperateTarget import _360PCOperateTarget
from autooptimize.operatetarget.baiduPCOperateTarget import BaiduPCOperateTarget
from autooptimize.operatetarget.baiduPCpictureOperateTarget import BaiduPCpictureOperateTarget
from autooptimize.operatetarget.baiduPhoneOperateTarget import BaiduPhoneOperateTarget
from autooptimize.operatetarget.shenmaPhoneOperateTarget import ShenmaPhoneOperateTarget
from autooptimize.operatetarget.sogouPCOperateTarget import SogouPCOperateTarget
from autooptimize.operatetarget.sogouPhoneOperateTarget import SogouPhoneOperateTarget

class OperateTargetFactory:

    def __init__(self):
        GlobalEnvStorage.infoLogger.info('OperateTargetFactory')

    def operate(self):
        operateTarget = None
        if GlobalEnvStorage.customerKeyword.searchEngine == '百度':
            if GlobalEnvStorage.customerKeyword.terminalType == 'Phone':
                operateTarget = BaiduPhoneOperateTarget()
            elif '_picture' in GlobalEnvStorage.customerKeyword.operationType:
                operateTarget = BaiduPCpictureOperateTarget()
            else:
                operateTarget = BaiduPCOperateTarget()
        else:
            if GlobalEnvStorage.customerKeyword.searchEngine == '搜狗':
                if GlobalEnvStorage.customerKeyword.terminalType == 'Phone':
                    operateTarget = SogouPhoneOperateTarget()
                else:
                    operateTarget = SogouPCOperateTarget()
            else:
                if GlobalEnvStorage.customerKeyword.searchEngine == '360':
                    if GlobalEnvStorage.customerKeyword.terminalType == 'Phone':
                        pass
                    else:
                        operateTarget = _360PCOperateTarget()
                else:
                    if GlobalEnvStorage.customerKeyword.searchEngine == '神马':
                        if GlobalEnvStorage.customerKeyword.terminalType == 'Phone':
                            operateTarget = ShenmaPhoneOperateTarget()
                    if operateTarget != None:
                        if '_xl' in GlobalEnvStorage.customerKeyword.operationType or '_xg' in GlobalEnvStorage.customerKeyword.operationType:
                            operateTarget.xialaOperate()
                        elif '_tj' in GlobalEnvStorage.customerKeyword.operationType:
                            operateTarget.tjOperate()
                        elif '_pm_map' in GlobalEnvStorage.customerKeyword.operationType:
                            operateTarget.mapOperate()
                        elif '_zhannei_sogou' in GlobalEnvStorage.customerKeyword.operationType:
                            operateTarget.otherOperate()
                        elif '_zhannei_360' in GlobalEnvStorage.customerKeyword.operationType:
                            operateTarget.otherOperate()
                        elif '_youku' in GlobalEnvStorage.customerKeyword.operationType:
                            operateTarget.youkuOperate()
                        else:
                            operateTarget.operate()
                    else:
                        GlobalEnvStorage.infoLogger.info('Wrong searchEngine or terminalType')

    def disturbOperate(self):
        operateTarget = None
        if GlobalEnvStorage.customerKeyword.searchEngine == '百度':
            if GlobalEnvStorage.customerKeyword.terminalType == 'Phone':
                operateTarget = BaiduPhoneOperateTarget()
            else:
                operateTarget = BaiduPCOperateTarget()
        else:
            if GlobalEnvStorage.customerKeyword.searchEngine == '搜狗':
                if GlobalEnvStorage.customerKeyword.terminalType == 'Phone':
                    operateTarget = SogouPhoneOperateTarget()
                else:
                    operateTarget = SogouPCOperateTarget()
            else:
                if GlobalEnvStorage.customerKeyword.searchEngine == '360':
                    if GlobalEnvStorage.customerKeyword.terminalType == 'Phone':
                        pass
                    else:
                        operateTarget = _360PCOperateTarget()
                else:
                    if GlobalEnvStorage.customerKeyword.searchEngine == '神马':
                        if GlobalEnvStorage.customerKeyword.terminalType == 'Phone':
                            operateTarget = ShenmaPhoneOperateTarget()
                    if operateTarget != None:
                        operateTarget.disturbOperate()
                    else:
                        GlobalEnvStorage.infoLogger.info('Wrong searchEngine or terminalType')
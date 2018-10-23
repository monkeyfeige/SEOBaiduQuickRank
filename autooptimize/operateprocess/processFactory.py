# uncompyle6 version 3.2.2
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.6.3 (v3.6.3:2c5fed8, Oct  3 2017, 18:11:49) [MSC v.1900 64 bit (AMD64)]
# Embedded file name: C:\PycharmProjects\AutoOptimize\autooptimize\operateprocess\processFactory.py
from autooptimize.globalEnvStorage import GlobalEnvStorage
from autooptimize.operateprocess._360OtherProcess import _360OtherProcess
from autooptimize.operateprocess._360SnapshotProcess import _360SnapshotProcess
from autooptimize.operateprocess.baiduMapProcess import BaiduMapProcess
from autooptimize.operateprocess.baiduNegetiveProcess import BaiduNegetiveProcess
from autooptimize.operateprocess.baiduPictureProcess import BaiduPictureProcess
from autooptimize.operateprocess.baiduSnapshotProcess import BaiduSnapshotProcess
from autooptimize.operateprocess.sogouOtherProcess import SogouOtherProcess
from autooptimize.operateprocess.xialaXiangguanProcess import XialaXiangguanProcess
from autooptimize.operateprocess.shenmaSnapshotProcess import ShenmaSnapshotProcess
from autooptimize.operateprocess.sogouSnapshotProcess import SogouSnapshotProcess
from autooptimize.operateprocess.youkuProcess import YoukuProcess

class ProcessFactory:

    def excecute(self):
        process = None
        if '_xl' in GlobalEnvStorage.customerKeyword.operationType or '_xg' in GlobalEnvStorage.customerKeyword.operationType:
            process = XialaXiangguanProcess()
        else:
            if GlobalEnvStorage.customerKeyword.searchEngine == '百度':
                if '_tj' in GlobalEnvStorage.customerKeyword.operationType:
                    process = BaiduNegetiveProcess()
                elif '_pm_map' in GlobalEnvStorage.customerKeyword.operationType:
                    process = BaiduMapProcess()
                elif '_youku' in GlobalEnvStorage.customerKeyword.operationType:
                    process = YoukuProcess()
                elif '_picture' in GlobalEnvStorage.customerKeyword.operationType:
                    process = BaiduPictureProcess()
                else:
                    process = BaiduSnapshotProcess()
            else:
                if GlobalEnvStorage.customerKeyword.searchEngine == '搜狗':
                    if '_zhannei_sogou' in GlobalEnvStorage.customerKeyword.operationType:
                        process = SogouOtherProcess()
                    else:
                        process = SogouSnapshotProcess()
                else:
                    if GlobalEnvStorage.customerKeyword.searchEngine == '360':
                        if '_zhannei_360' in GlobalEnvStorage.customerKeyword.operationType:
                            process = _360OtherProcess()
                        else:
                            process = _360SnapshotProcess()
                    else:
                        if GlobalEnvStorage.customerKeyword.searchEngine == '神马':
                            process = ShenmaSnapshotProcess()
                        if process != None:
                            process.execute()
                        else:
                            GlobalEnvStorage.infoLogger.info('Wrong searchEngine or operationType')
# uncompyle6 version 3.2.2
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.6.3 (v3.6.3:2c5fed8, Oct  3 2017, 18:11:49) [MSC v.1900 64 bit (AMD64)]
# Embedded file name: C:\PycharmProjects\AutoOptimize\autooptimize\operateprocess\abstractProcess.py
from autooptimize.globalEnvStorage import GlobalEnvStorage

class AbstractProcess:

    def execute(self):
        GlobalEnvStorage.infoLogger.info('Please implement execute')
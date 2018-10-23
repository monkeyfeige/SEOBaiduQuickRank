# uncompyle6 version 3.2.2
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.6.3 (v3.6.3:2c5fed8, Oct  3 2017, 18:11:49) [MSC v.1900 64 bit (AMD64)]
# Embedded file name: C:\PycharmProjects\AutoOptimize\autooptimize\env.py
import traceback
from configparser import ConfigParser
import time, shutil
from autooptimize.globalEnvStorage import GlobalEnvStorage
from autooptimize.util.scheduler import backUpConf, closeSelfAndStart

class Env:

    def initGlobalEnvStorage(self):
        try:
            _Env__cf = ConfigParser()
            if GlobalEnvStorage.env == 'Development':
                _Env__cf.read('../config/dev/server.ini', encoding='utf-8-sig')
            else:
                _Env__cf.read('C:\\working' + '\\server.ini', encoding='utf-8-sig')
            GlobalEnvStorage.customerKeywordServerHost = 'http://' + _Env__cf.get('set', 'host')
            GlobalEnvStorage.customerKeywordServerUser = _Env__cf.get('set', 'user')
            GlobalEnvStorage.customerKeywordServerPassword = _Env__cf.get('set', 'pass')
            GlobalEnvStorage.isConncet = int(_Env__cf.get('Connect', 'isConncet'))
            GlobalEnvStorage.connectName = _Env__cf.get('Connect', 'name')
            GlobalEnvStorage.connectUserName = _Env__cf.get('Connect', 'username')
            GlobalEnvStorage.connectPassword = _Env__cf.get('Connect', 'password')
            _Env__cf.clear()
            if GlobalEnvStorage.env == 'Development':
                _Env__cf.read('../config/dev/env.conf', encoding='utf-8-sig')
            else:
                _Env__cf.read('C:\\working\\env.conf', encoding='utf-8-sig')
            GlobalEnvStorage.clientID = _Env__cf.get('Basic', 'clientID')
            GlobalEnvStorage.BaiduPCEntryUrl = _Env__cf.get('BaiduEntryUrl', 'PCEntryUrl')
            GlobalEnvStorage.BaiduPhoneEntryUrl = _Env__cf.get('BaiduEntryUrl', 'PhoneEntryUrl')
            GlobalEnvStorage.SogouPCEntryUrl = _Env__cf.get('SogouEntryUrl', 'PCEntryUrl')
            GlobalEnvStorage.SogouPhoneEntryUrl = _Env__cf.get('SogouEntryUrl', 'PhoneEntryUrl')
            GlobalEnvStorage._360PCEntryUrl = _Env__cf.get('360EntryUrl', 'PCEntryUrl')
            GlobalEnvStorage._360PhoneEntryUrl = _Env__cf.get('360EntryUrl', 'PhoneEntryUrl')
            GlobalEnvStorage.ShenmaPhoneEntryUrl = _Env__cf.get('ShenmaEntryUrl', 'PhoneEntryUrl')
            GlobalEnvStorage.last_profileID = _Env__cf.get('Basic', 'last_profileID')
            GlobalEnvStorage.fail_num = int(_Env__cf.get('Basic', 'fail_num'))
            GlobalEnvStorage.profileID = int(_Env__cf.get('Basic', 'last_profileID'))
            GlobalEnvStorage.profileIDCountList = eval(_Env__cf.get('profileIDCountList', 'list'))
            GlobalEnvStorage.cookiesProfileList = eval(_Env__cf.get('cookiesProfileList', 'list'))
            GlobalEnvStorage.chromeExeFilePath = _Env__cf.get('ChromePath', 'exe_file_path')
            GlobalEnvStorage.chromeUserDataDir = _Env__cf.get('ChromePath', 'user_data_dir')
            GlobalEnvStorage.PelsWidth = int(_Env__cf.get('Resolution', 'PelsWidth'))
            GlobalEnvStorage.PelsHeight = int(_Env__cf.get('Resolution', 'PelsHeight'))
            GlobalEnvStorage.BitsPerPel = int(_Env__cf.get('Resolution', 'BitsPerPel'))
            GlobalEnvStorage.inputMethod_paste = _Env__cf.get('inputMethod', 'paste')
            GlobalEnvStorage.inputMethod_click = _Env__cf.get('inputMethod', 'input')
            GlobalEnvStorage.search_enter = _Env__cf.get('SearchMethod', 'enter')
            GlobalEnvStorage.search_click = _Env__cf.get('SearchMethod', 'click')
            GlobalEnvStorage.clickTarget_image = _Env__cf.get('clickTarget', 'image')
            GlobalEnvStorage.clickTarget_title = _Env__cf.get('clickTarget', 'title')
            GlobalEnvStorage.MutiClick_one = int(_Env__cf.get('MutiClick', 'one'))
            GlobalEnvStorage.MutiClick_two = int(_Env__cf.get('MutiClick', 'two'))
            GlobalEnvStorage.MutiClick_three = int(_Env__cf.get('MutiClick', 'three'))
            GlobalEnvStorage.MutiClick_four = int(_Env__cf.get('MutiClick', 'four'))
            GlobalEnvStorage.NoResultClick_FirstPageThree = _Env__cf.get('NoResultClick', 'FirstPageThree')
            GlobalEnvStorage.NoResultClick_FirstPageTen = _Env__cf.get('NoResultClick', 'FirstPageTen')
            GlobalEnvStorage.NoResultClick_SecondPageThree = _Env__cf.get('NoResultClick', 'SecondPageThree')
            GlobalEnvStorage.NoResultClick_SecondPageTen = _Env__cf.get('NoResultClick', 'SecondPageTen')
            GlobalEnvStorage.NoFindFlip_nextPage = _Env__cf.get('NoFindFlip', 'nextPage')
            GlobalEnvStorage.NoFindFlip_clickPage = _Env__cf.get('NoFindFlip', 'clickPage')
            GlobalEnvStorage.FindFlip_nextPage = _Env__cf.get('FindFlip', 'nextPage')
            GlobalEnvStorage.FindFlip_clickTarget = _Env__cf.get('FindFlip', 'clickTarget')
            GlobalEnvStorage.xiaoxiala_percentage = _Env__cf.get('xiaoxiala', 'percentage')
            GlobalEnvStorage.PageMargin_PCTopMargin = int(_Env__cf.get('PageMargin', 'PCTopMargin'))
            GlobalEnvStorage.PageMargin_PCBottomMargin = int(_Env__cf.get('PageMargin', 'PCBottomMargin'))
            GlobalEnvStorage.PageMargin_PhoneTopMargin = int(_Env__cf.get('PageMargin', 'PhoneTopMargin'))
            GlobalEnvStorage.PageMargin_PhoneBottomMargin = int(_Env__cf.get('PageMargin', 'PhoneBottomMargin'))
            GlobalEnvStorage.TargetMargin_PCTopMargin = int(_Env__cf.get('TargetMargin', 'PCTopMargin'))
            GlobalEnvStorage.TargetMargin_PCBottomMargin = int(_Env__cf.get('TargetMargin', 'PCBottomMargin'))
            GlobalEnvStorage.TargetMargin_PhoneTopMargin = int(_Env__cf.get('TargetMargin', 'PhoneTopMargin'))
            GlobalEnvStorage.TargetMargin_PhoneBottomMargin = int(_Env__cf.get('TargetMargin', 'PhoneBottomMargin'))
            GlobalEnvStorage.ClearCookies_clearNum = int(_Env__cf.get('ClearCookies', 'clearNum'))
            GlobalEnvStorage.ClearCookies_clearPercentage = int(_Env__cf.get('ClearCookies', 'clearPercentage'))
            GlobalEnvStorage.baiduPC_selector = eval(_Env__cf.get('Cssselector', 'baiduPC_selector'))
            GlobalEnvStorage.baiduPhone_selector = eval(_Env__cf.get('Cssselector', 'baiduPhone_selector'))
            GlobalEnvStorage.sogouPC_selector = eval(_Env__cf.get('Cssselector', 'sogouPC_selector'))
            GlobalEnvStorage.sogouPhone_selector = eval(_Env__cf.get('Cssselector', 'sogouPhone_selector'))
            GlobalEnvStorage._360PC_selector = eval(_Env__cf.get('Cssselector', '_360PC_selector'))
            GlobalEnvStorage._360Phone_selector = eval(_Env__cf.get('Cssselector', '_360Phone_selector'))
            GlobalEnvStorage.shenmaPhone_selector = eval(_Env__cf.get('Cssselector', 'shenmaPhone_selector'))
            _Env__cf.clear()
            backUpConf()
        except:
            traceback.print_exc()
            shutil.copyfile('C:\\working\\env_backup.conf', 'C:\\working\\env.conf')
            time.sleep(10)
            closeSelfAndStart(startNow=True)
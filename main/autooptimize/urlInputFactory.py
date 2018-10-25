# uncompyle6 version 3.2.2
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.6.3 (v3.6.3:2c5fed8, Oct  3 2017, 18:11:49) [MSC v.1900 64 bit (AMD64)]
# Embedded file name: C:\PycharmProjects\AutoOptimize\autooptimize\urlInputFactory.py
import json, time
from random import randint
from random import uniform
from autooptimize.globalEnvStorage import GlobalEnvStorage
from autooptimize.keywordInputFactory import KeywordInputFactory
from autooptimize.model.entryUrl import EntryUrl

class UrlInputFactory:
    url = None

    def __init__(self, start=1, end=100):
        if GlobalEnvStorage.customerKeyword.terminalType == 'PC':
            if GlobalEnvStorage.customerKeyword.searchEngine == '百度':
                entryUrlPercentage = GlobalEnvStorage.BaiduPCEntryUrl
                GlobalEnvStorage.selector = GlobalEnvStorage.baiduPC_selector
            else:
                if GlobalEnvStorage.customerKeyword.searchEngine == '搜狗':
                    entryUrlPercentage = GlobalEnvStorage.SogouPCEntryUrl
                    GlobalEnvStorage.selector = GlobalEnvStorage.sogouPC_selector
                else:
                    if GlobalEnvStorage.customerKeyword.searchEngine == '360':
                        entryUrlPercentage = GlobalEnvStorage._360PCEntryUrl
                        GlobalEnvStorage.selector = GlobalEnvStorage._360PC_selector
                    entryUrls = json.loads(entryUrlPercentage, object_hook=EntryUrl)
                    randValue = randint(start, end)
                    for entryUrl in entryUrls:
                        if randValue >= entryUrl.durationStart and randValue <= entryUrl.durationEnd:
                            GlobalEnvStorage.entryUrl = entryUrl.url
                            GlobalEnvStorage.searchText = entryUrl.searchText
                            GlobalEnvStorage.searchButtom = entryUrl.searchButtom
                            GlobalEnvStorage.dropDownList = entryUrl.dropDownList
                            GlobalEnvStorage.skipPosition = entryUrl.skipPosition
                            break

        else:
            if GlobalEnvStorage.customerKeyword.searchEngine == '百度':
                entryUrl = json.loads(GlobalEnvStorage.BaiduPhoneEntryUrl, object_hook=EntryUrl)[0]
                GlobalEnvStorage.selector = GlobalEnvStorage.baiduPhone_selector
            else:
                if GlobalEnvStorage.customerKeyword.searchEngine == '搜狗':
                    entryUrl = json.loads(GlobalEnvStorage.SogouPhoneEntryUrl, object_hook=EntryUrl)[0]
                    GlobalEnvStorage.selector = GlobalEnvStorage.sogouPhone_selector
                else:
                    if GlobalEnvStorage.customerKeyword.searchEngine == '360':
                        entryUrl = json.loads(GlobalEnvStorage._360PhoneEntryUrl, object_hook=EntryUrl)[0]
                        GlobalEnvStorage.selector = GlobalEnvStorage._360Phone_selector
                    else:
                        if GlobalEnvStorage.customerKeyword.searchEngine == '神马':
                            entryUrl = json.loads(GlobalEnvStorage.ShenmaPhoneEntryUrl, object_hook=EntryUrl)[0]
                            GlobalEnvStorage.selector = GlobalEnvStorage.shenmaPhone_selector
                        GlobalEnvStorage.entryUrl = entryUrl.url
                        GlobalEnvStorage.searchText = entryUrl.searchText
                        GlobalEnvStorage.searchButtom = entryUrl.searchButtom
                        GlobalEnvStorage.dropDownList = entryUrl.dropDownList
                    GlobalEnvStorage.infoLogger.info('%s', GlobalEnvStorage.entryUrl)

    def input(self, url=None, newProfile=True):
        keywordInputFactory = KeywordInputFactory()
        GlobalEnvStorage.dmFactory.dm.MoveTo(250, 40)
        GlobalEnvStorage.dmFactory.dm.LeftClick()
        if GlobalEnvStorage.customerKeyword.terminalType == 'PC':
            keywordInputFactory.setClipboardData('about:blank')
            time.sleep(uniform(0.1, 0.3))
            keywordInputFactory.pasteFromClipboard()
            time.sleep(uniform(0.1, 0.3))
            keywordInputFactory.Enter()
        else:
            if GlobalEnvStorage.customerKeyword.terminalType == 'Phone' and newProfile:
                keywordInputFactory.setClipboardData('chrome://settings/content')
                time.sleep(uniform(0.1, 0.3))
                keywordInputFactory.pasteFromClipboard()
                time.sleep(uniform(0.1, 0.3))
                keywordInputFactory.Enter()
                try:
                    time.sleep(0.5)
                    GlobalEnvStorage.browser.driver.switch_to.frame('settings')
                    GlobalEnvStorage.browser.choose('location', 'block')
                except Exception as e:
                    GlobalEnvStorage.exceptionlogger.exception('%s', e)

            else:
                keywordInputFactory.setClipboardData('about:blank')
                time.sleep(uniform(0.1, 0.3))
                keywordInputFactory.pasteFromClipboard()
                time.sleep(uniform(0.1, 0.3))
                keywordInputFactory.Enter()
            GlobalEnvStorage.dmFactory.dm.MoveTo(randint(int(int(GlobalEnvStorage.PelsWidth) * 0.5), int(int(GlobalEnvStorage.PelsWidth) * 0.8)), randint(int(int(GlobalEnvStorage.PelsHeight) * 0.6), int(int(GlobalEnvStorage.PelsHeight) * 0.8)))
            if GlobalEnvStorage.customerKeyword.terminalType == 'PC':
                GlobalEnvStorage.browser.driver.set_page_load_timeout(20)
            else:
                GlobalEnvStorage.browser.driver.set_page_load_timeout(20)
            GlobalEnvStorage.browser.driver.set_script_timeout(20)
        try:
            if url:
                GlobalEnvStorage.browser.visit(url)
            else:
                GlobalEnvStorage.browser.visit(GlobalEnvStorage.entryUrl)
            try:
                if '.baidu.com' in GlobalEnvStorage.entryUrl and ('_cookies' in GlobalEnvStorage.customerKeyword.operationType or '_pm_map' in GlobalEnvStorage.customerKeyword.operationType):
                    if not GlobalEnvStorage.profileIDCountList[str(GlobalEnvStorage.profileID)]['baiduCookies']:
                        cookies = [
                         {'name': 'BDUSS',  'domain': '.baidu.com',  'path': '/',  'httpOnly': False,  'expiry': str(time.time() + randint(1000000, 10000000)), 
                          'secure': False, 
                          'value': GlobalEnvStorage.cookies[GlobalEnvStorage.profileID]}]
                        for cookie in cookies:
                            GlobalEnvStorage.browser.driver.add_cookie(cookie)

                        GlobalEnvStorage.profileIDCountList[str(GlobalEnvStorage.profileID)]['baiduCookies'] = True
            except Exception as e:
                GlobalEnvStorage.infoLogger.info('%s', e)

            time.sleep(GlobalEnvStorage.customerKeyword.waitTimeAfterOpenBaidu)
        except Exception as e:
            GlobalEnvStorage.infoLogger.info('%s', e)

    def inputTwo(self, url=None):
        keywordInputFactory = KeywordInputFactory()
        GlobalEnvStorage.dmFactory.dm.MoveTo(250, 40)
        GlobalEnvStorage.dmFactory.dm.LeftClick()
        if GlobalEnvStorage.customerKeyword.terminalType == 'PC':
            keywordInputFactory.setClipboardData('chrome://settings/startup')
            time.sleep(uniform(0.1, 0.3))
            keywordInputFactory.pasteFromClipboard()
            time.sleep(uniform(0.1, 0.3))
            keywordInputFactory.Enter()
        else:
            keywordInputFactory.setClipboardData('chrome://settings/content')
            time.sleep(uniform(0.1, 0.3))
            keywordInputFactory.pasteFromClipboard()
            time.sleep(uniform(0.1, 0.3))
            keywordInputFactory.Enter()
            try:
                time.sleep(0.5)
                GlobalEnvStorage.browser.driver.switch_to.frame('settings')
                GlobalEnvStorage.browser.choose('location', 'block')
            except Exception as e:
                GlobalEnvStorage.exceptionlogger.exception('%s', e)

            GlobalEnvStorage.dmFactory.dm.MoveTo(randint(int(int(GlobalEnvStorage.PelsWidth) * 0.5), int(int(GlobalEnvStorage.PelsWidth) * 0.8)), randint(int(int(GlobalEnvStorage.PelsHeight) * 0.6), int(int(GlobalEnvStorage.PelsHeight) * 0.8)))
            if GlobalEnvStorage.customerKeyword.terminalType == 'PC':
                GlobalEnvStorage.browser.driver.set_page_load_timeout(10)
            else:
                GlobalEnvStorage.browser.driver.set_page_load_timeout(20)
            GlobalEnvStorage.browser.driver.set_script_timeout(20)
        try:
            if url:
                GlobalEnvStorage.browser.visit(url)
            else:
                GlobalEnvStorage.browser.visit(GlobalEnvStorage.entryUrl)
            try:
                if GlobalEnvStorage.entryUrl == 'https://www.baidu.com' and ('_cookies' in GlobalEnvStorage.customerKeyword.operationType or '_pm_map' in GlobalEnvStorage.customerKeyword.operationType):
                    cookies = [
                     {'name': 'BDUSS',  'domain': '.baidu.com',  'path': '/',  'httpOnly': False,  'expiry': str(time.time() + randint(1000000, 10000000)), 
                      'secure': False, 
                      'value': GlobalEnvStorage.cookies[GlobalEnvStorage.profileID]}]
                    for cookie in cookies:
                        GlobalEnvStorage.browser.driver.add_cookie(cookie)

            except Exception as e:
                GlobalEnvStorage.infoLogger.info('%s', e)

        except Exception as e:
            GlobalEnvStorage.infoLogger.info('%s', e)
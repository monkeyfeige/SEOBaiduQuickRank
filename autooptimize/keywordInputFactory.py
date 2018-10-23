# uncompyle6 version 3.2.2
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.6.3 (v3.6.3:2c5fed8, Oct  3 2017, 18:11:49) [MSC v.1900 64 bit (AMD64)]
# Embedded file name: C:\PycharmProjects\AutoOptimize\autooptimize\keywordInputFactory.py
import ctypes, time
from random import randint, uniform
import win32.win32api as win32api, win32.win32clipboard as w, win32con
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.wait import WebDriverWait
from autooptimize.globalEnvStorage import GlobalEnvStorage

class KeywordInputFactory:

    def inputOneWord(self, word, MapVirtualKey):
        GlobalEnvStorage.infoLogger.info('%s', word)
        ky = word.encode('gbk')
        if len(ky) == 1:
            kyInt = ord(ky)
            kyStr = str(kyInt)
        else:
            kyInt = ky[0] // 16 * 4096 + ky[0] % 16 * 256 + ky[1] // 16 * 16 + ky[1] % 16
            kyStr = str(kyInt)
        win32api.keybd_event(18, MapVirtualKey(18, 0), 0, 0)
        for num in kyStr:
            win32api.keybd_event(96 + int(num), MapVirtualKey(96 + int(num), 0), 0, 0)
            win32api.keybd_event(96 + int(num), MapVirtualKey(96 + int(num), 0), win32con.KEYEVENTF_KEYUP, 0)

        win32api.keybd_event(18, MapVirtualKey(18, 0), win32con.KEYEVENTF_KEYUP, 0)
        time.sleep(uniform(GlobalEnvStorage.customerKeyword.inputDelayMinTime, GlobalEnvStorage.customerKeyword.inputDelayMaxTime))

    def inputWords(self, words):
        MapVirtualKey = ctypes.windll.user32.MapVirtualKeyA
        for word in words:
            self.inputOneWord(word, MapVirtualKey)
            if randint(1, 3) == 2 and GlobalEnvStorage.customerKeyword.sleepPer2Words:
                time.sleep(uniform(0.3, 0.6))
                continue

    def inputString(self, keyword):
        MapVirtualKey = ctypes.windll.user32.MapVirtualKeyA
        idx = 0
        for word in keyword:
            self.inputOneWord(word, MapVirtualKey)
            idx += 1
            if idx % 2 == 0:
                GlobalEnvStorage.infoLogger.info('开始下拉框的操作。')
                if GlobalEnvStorage.customerKeyword.sleepPer2Words:
                    time.sleep(uniform(0.3, 0.6))
                try:
                    flag = self.dropDownList(keyword)
                    if flag:
                        return
                    GlobalEnvStorage.infoLogger.info('下拉没找到,继续')
                except:
                    GlobalEnvStorage.infoLogger.info('下拉出现异常,没找到,继续')

                continue

        from autooptimize.searchFactory import SearchFactory
        SearchFactory().search()

    def inputKeyword(self, keyword):
        GlobalEnvStorage.infoLogger.info('GlobalEnvStorage.searchText:%s', GlobalEnvStorage.searchText)
        GlobalEnvStorage.infoLogger.info('GlobalEnvStorage.searchButtom:%s', GlobalEnvStorage.searchButtom)
        if GlobalEnvStorage.entryUrl == 'https://m.baidu.com' and GlobalEnvStorage.browser.driver.find_elements_by_css_selector('.callappbox') != []:
            GlobalEnvStorage.browserWrapper.locateAndClick(GlobalEnvStorage.browser.driver.find_elements_by_css_selector('.callappbox-wrap-chose-close')[0])
            time.sleep(uniform(0.7, 1.2))
        if GlobalEnvStorage.relocation:
            element = WebDriverWait(GlobalEnvStorage.browser.driver, 30).until(expected_conditions.presence_of_all_elements_located((By.CSS_SELECTOR, GlobalEnvStorage.searchText)))[0]
            GlobalEnvStorage.browserWrapper.locateAndClick(element)
            time.sleep(uniform(0.7, 1.2))
        if GlobalEnvStorage.customerKeyword.supportPaste == 1 and GlobalEnvStorage.customerKeyword.terminalType == 'PC':
            n = randint(1, 100)
            if n <= int(GlobalEnvStorage.inputMethod_paste):
                self.setClipboardData(keyword)
                time.sleep(uniform(0.1, 0.2))
                self.pasteFromClipboard()
                from autooptimize.searchFactory import SearchFactory
                SearchFactory().search()
            else:
                self.inputString(keyword)
        else:
            self.inputString(keyword)

    def pasteFromClipboard(self):
        MapVirtualKey = ctypes.windll.user32.MapVirtualKeyA
        win32api.keybd_event(win32con.VK_CONTROL, MapVirtualKey(win32con.VK_CONTROL, 0), 0, 0)
        win32api.keybd_event(86, MapVirtualKey(86, 0), 0, 0)
        win32api.keybd_event(86, MapVirtualKey(86, 0), win32con.KEYEVENTF_KEYUP, 0)
        win32api.keybd_event(win32con.VK_CONTROL, MapVirtualKey(win32con.VK_CONTROL, 0), win32con.KEYEVENTF_KEYUP, 0)
        time.sleep(uniform(0.1, 0.3))

    def setClipboardData(self, content):
        w.OpenClipboard()
        w.EmptyClipboard()
        w.SetClipboardData(win32con.CF_UNICODETEXT, content)
        w.CloseClipboard()
        time.sleep(uniform(0.1, 0.3))

    @staticmethod
    def Enter():
        MapVirtualKey = ctypes.windll.user32.MapVirtualKeyA
        win32api.keybd_event(win32con.VK_RETURN, MapVirtualKey(win32con.VK_RETURN, 0), 0, 0)
        win32api.keybd_event(win32con.VK_RETURN, MapVirtualKey(win32con.VK_RETURN, 0), win32con.KEYEVENTF_KEYUP, 0)

    @staticmethod
    def Ctrl_Tab():
        MapVirtualKey = ctypes.windll.user32.MapVirtualKeyA
        win32api.keybd_event(win32con.VK_CONTROL, MapVirtualKey(win32con.VK_CONTROL, 0), 0, 0)
        win32api.keybd_event(win32con.VK_TAB, MapVirtualKey(win32con.VK_TAB, 0), 0, 0)
        win32api.keybd_event(win32con.VK_TAB, MapVirtualKey(win32con.VK_TAB, 0), win32con.KEYEVENTF_KEYUP, 0)
        win32api.keybd_event(win32con.VK_CONTROL, MapVirtualKey(win32con.VK_CONTROL, 0), win32con.KEYEVENTF_KEYUP, 0)

    @staticmethod
    def Ctrl_PageUP():
        MapVirtualKey = ctypes.windll.user32.MapVirtualKeyA
        win32api.keybd_event(win32con.VK_CONTROL, MapVirtualKey(win32con.VK_CONTROL, 0), 0, 0)
        win32api.keybd_event(win32con.VK_PRIOR, MapVirtualKey(win32con.VK_TAB, 0), 0, 0)
        win32api.keybd_event(win32con.VK_PRIOR, MapVirtualKey(win32con.VK_TAB, 0), win32con.KEYEVENTF_KEYUP, 0)
        win32api.keybd_event(win32con.VK_CONTROL, MapVirtualKey(win32con.VK_CONTROL, 0), win32con.KEYEVENTF_KEYUP, 0)

    @staticmethod
    def Ctrl_Number(num):
        MapVirtualKey = ctypes.windll.user32.MapVirtualKeyA
        win32api.keybd_event(win32con.VK_CONTROL, MapVirtualKey(win32con.VK_CONTROL, 0), 0, 0)
        win32api.keybd_event(96 + int(num), MapVirtualKey(96 + int(num), 0), 0, 0)
        win32api.keybd_event(96 + int(num), MapVirtualKey(96 + int(num), 0), win32con.KEYEVENTF_KEYUP, 0)
        win32api.keybd_event(win32con.VK_CONTROL, MapVirtualKey(win32con.VK_CONTROL, 0), win32con.KEYEVENTF_KEYUP, 0)

    @staticmethod
    def Delete():
        MapVirtualKey = ctypes.windll.user32.MapVirtualKeyA
        win32api.keybd_event(win32con.VK_BACK, MapVirtualKey(win32con.VK_BACK, 0), 0, 0)
        win32api.keybd_event(win32con.VK_BACK, MapVirtualKey(win32con.VK_BACK, 0), win32con.KEYEVENTF_KEYUP, 0)

    @staticmethod
    def End():
        MapVirtualKey = ctypes.windll.user32.MapVirtualKeyA
        win32api.keybd_event(win32con.VK_END, MapVirtualKey(win32con.VK_END, 0), 0, 0)
        win32api.keybd_event(win32con.VK_END, MapVirtualKey(win32con.VK_END, 0), win32con.KEYEVENTF_KEYUP, 0)

    @staticmethod
    def Down():
        MapVirtualKey = ctypes.windll.user32.MapVirtualKeyA
        win32api.keybd_event(win32con.VK_DOWN, MapVirtualKey(win32con.VK_DOWN, 0), 0, 0)
        win32api.keybd_event(win32con.VK_DOWN, MapVirtualKey(win32con.VK_DOWN, 0), win32con.KEYEVENTF_KEYUP, 0)

    def dropDownList(self, words):
        if GlobalEnvStorage.customerKeyword.terminalType == 'PC':
            parentsDiv = GlobalEnvStorage.dropDownList
            keywords = GlobalEnvStorage.browser.driver.find_elements_by_css_selector(parentsDiv)
            for i in range(len(keywords)):
                if words == keywords[i].text:
                    percentage = randint(1, 100)
                    if percentage <= int(GlobalEnvStorage.search_click):
                        GlobalEnvStorage.browserWrapper.locateAndClick(keywords[i])
                        GlobalEnvStorage.infoLogger.info('下拉找到，鼠标点解')
                    else:
                        nowPosition = -1
                        while i > nowPosition:
                            self.Down()
                            nowPosition = nowPosition + 1
                            time.sleep(uniform(0.1, 0.3))

                        time.sleep(uniform(0.1, 0.3))
                        self.Enter()
                        GlobalEnvStorage.infoLogger.info('下拉找到，enter键')
                    return True
                return False

        else:
            list = GlobalEnvStorage.dropDownList
            keywords = GlobalEnvStorage.browser.driver.find_elements_by_css_selector(list)
            for i in range(len(keywords)):
                if words == keywords[i].text:
                    GlobalEnvStorage.browserWrapper.locateAndClick(keywords[i])
                    return True
                return False

    def intoBaidu(self, skipPosition):
        time.sleep(2)
        GlobalEnvStorage.infoLogger.info('进入百度搜索页面')
        from autooptimize.operatetarget.baiduPCOperateTarget import BaiduPCOperateTarget
        baiduPCOperateTarget = BaiduPCOperateTarget()
        element = WebDriverWait(GlobalEnvStorage.browser.driver, 30).until(expected_conditions.presence_of_all_elements_located((By.PARTIAL_LINK_TEXT, '去网页搜索')))[0]
        baiduPCOperateTarget.scrolledIntoView(element)
        GlobalEnvStorage.browserWrapper.locateAndClick(element)

    def disturbInput(self, wordType):
        from autooptimize.util.util import fetchSuggestionsValue
        from autooptimize.util.util import fetchRelativeAndRecommendationValue
        disturbword = None
        if wordType == 0:
            if '_3grade' in GlobalEnvStorage.customerKeyword.operationType:
                n = randint(1, 100)
                if n <= 100:
                    grade = 1
                elif n <= 80:
                    grade = 2
                else:
                    grade = 3
            else:
                grade = 1
            suggestionWord = GlobalEnvStorage.customerKeyword.keyword
            for time in range(grade):
                suggestionWord = fetchSuggestionsValue(suggestionWord, GlobalEnvStorage.customerKeyword.terminalType)
                if suggestionWord != None and suggestionWord != '':
                    disturbword = suggestionWord
                else:
                    break

            if disturbword is None:
                GlobalEnvStorage.infoLogger.info('下拉词不存在')
                return False
            GlobalEnvStorage.infoLogger.info('下拉词*' + disturbword + '*')
            self.inputDisturbString(disturbword)
        else:
            if '_3grade' in GlobalEnvStorage.customerKeyword.operationType:
                n = randint(1, 100)
                if n <= 50:
                    grade = 1
                elif n <= 80:
                    grade = 2
                else:
                    grade = 3
            else:
                grade = 1
            recommendationWord = GlobalEnvStorage.customerKeyword.keyword
            for time in range(grade):
                recommendationWord = fetchRelativeAndRecommendationValue(recommendationWord, GlobalEnvStorage.customerKeyword.terminalType)
                if recommendationWord != None and recommendationWord != '':
                    disturbword = recommendationWord
                else:
                    break

            if disturbword is None:
                GlobalEnvStorage.infoLogger.info('相关搜索词不存在')
                return False
            GlobalEnvStorage.infoLogger.info('相关搜索词*' + disturbword + '*')
            self.inputDisturbString(disturbword)

    def inputDisturbString(self, keyword):
        GlobalEnvStorage.infoLogger.info('GlobalEnvStorage.searchText:%s', GlobalEnvStorage.searchText)
        GlobalEnvStorage.infoLogger.info('GlobalEnvStorage.searchButtom:%s', GlobalEnvStorage.searchButtom)
        if GlobalEnvStorage.entryUrl == 'https://m.baidu.com' and GlobalEnvStorage.browser.driver.find_elements_by_css_selector('.callappbox') != []:
            GlobalEnvStorage.browserWrapper.locateAndClick(GlobalEnvStorage.browser.driver.find_elements_by_css_selector('.callappbox-wrap-chose-close')[0])
            time.sleep(uniform(0.7, 1.2))
        if GlobalEnvStorage.relocation:
            search = GlobalEnvStorage.searchText
            element = WebDriverWait(GlobalEnvStorage.browser.driver, 30).until(expected_conditions.presence_of_all_elements_located((By.CSS_SELECTOR, search)))[0]
            GlobalEnvStorage.browserWrapper.locateAndClick(element)
            time.sleep(uniform(0.7, 1.2))
        MapVirtualKey = ctypes.windll.user32.MapVirtualKeyA
        from autooptimize.searchFactory import SearchFactory
        if GlobalEnvStorage.customerKeyword.supportPaste == 1 and GlobalEnvStorage.customerKeyword.terminalType == 'PC':
            n = randint(1, 100)
            if n <= int(GlobalEnvStorage.inputMethod_paste):
                self.setClipboardData(keyword)
                self.pasteFromClipboard()
            else:
                for letter in keyword:
                    self.inputOneWord(letter, MapVirtualKey)
                    if randint(1, 2) == 2 and GlobalEnvStorage.customerKeyword.sleepPer2Words:
                        time.sleep(uniform(0.3, 0.6))
                        continue

        else:
            for letter in keyword:
                self.inputOneWord(letter, MapVirtualKey)
                if randint(1, 2) == 2 and GlobalEnvStorage.customerKeyword.sleepPer2Words:
                    time.sleep(uniform(0.3, 0.6))
                    continue

        SearchFactory().search()

    def inputMapAddr(self):
        GlobalEnvStorage.searchText = '#sole-input'
        GlobalEnvStorage.searchButtom = '#search-button'
        GlobalEnvStorage.dropDownList = '.ui3-suggest-item'
        self.inputKeyword(GlobalEnvStorage.customerKeyword.keyword)

    def UrlBack(self, url):
        GlobalEnvStorage.dmFactory.dm.MoveTo(250, 40)
        GlobalEnvStorage.dmFactory.dm.LeftClick()
        self.setClipboardData(url)
        time.sleep(uniform(0.1, 0.3))
        self.pasteFromClipboard()
        time.sleep(uniform(0.1, 0.3))
        self.Enter()
        time.sleep(2)
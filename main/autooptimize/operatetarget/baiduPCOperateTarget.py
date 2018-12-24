# uncompyle6 version 3.2.2
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.6.3 (v3.6.3:2c5fed8, Oct  3 2017, 18:11:49) [MSC v.1900 64 bit (AMD64)]
# Embedded file name: C:\PycharmProjects\AutoOptimize\autooptimize\operatetarget\baiduPCOperateTarget.py
import time
from random import randint, uniform
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.wait import WebDriverWait
from autooptimize.globalEnvStorage import GlobalEnvStorage
from autooptimize.keywordInputFactory import KeywordInputFactory
from autooptimize.model.rowSummaryInfo import RowSummaryInfo
from autooptimize.operatetarget.PCOperateTarget import PCOperatetarget
from autooptimize.util.util import zhangneiUrl

class BaiduPCOperateTarget(PCOperatetarget):

    def initPageSize(self):
        if GlobalEnvStorage.customerKeyword.pageSize != GlobalEnvStorage.profileIDCountList[str(GlobalEnvStorage.profileID)]['pageSize']:
            if GlobalEnvStorage.entryUrl == 'https://www.baidu.com':
                pf = WebDriverWait(GlobalEnvStorage.browser.driver, 30).until(expected_conditions.presence_of_all_elements_located((By.CSS_SELECTOR, '.pf')))[-1]
            else:
                pf = WebDriverWait(GlobalEnvStorage.browser.driver, 30).until(expected_conditions.presence_of_all_elements_located((By.CSS_SELECTOR, '.pf')))[0]
            GlobalEnvStorage.browserWrapper.locateAndClick(pf)
            setpref = GlobalEnvStorage.browser.evaluate_script('$(".bdpfmenu >a.setpref")')[0]
            GlobalEnvStorage.browserWrapper.locateAndClick(setpref)
            time.sleep(2)
            nr = GlobalEnvStorage.browser.evaluate_script('$("#nr")')[0]
            GlobalEnvStorage.browserWrapper.locateAndClick(nr)
            options = nr.find_elements_by_tag_name('option')
            info = GlobalEnvStorage.browserWrapper.getElementLocationInfo(nr)
            for idx in range(len(options)):
                if str(GlobalEnvStorage.customerKeyword.pageSize) in options[idx].text:
                    GlobalEnvStorage.dmFactory.simulateTrajectory(info['x'] + randint(int(info['width'] * 0.2), int(info['width'] * 0.8)), info['y'] + GlobalEnvStorage.toolBarHeight + randint(int(info['height'] * 0.2), int(info['height'] * 0.5)) + (idx + 1) * info['height'])
                    break

            save = GlobalEnvStorage.browser.evaluate_script('$(".prefpanelgo")')[0]
            GlobalEnvStorage.browserWrapper.locateAndClick(save)
            try:
                WebDriverWait(GlobalEnvStorage.browser.driver, 30).until(expected_conditions.alert_is_present())
                GlobalEnvStorage.browser.driver.switch_to_alert().accept()
            except:
                pass

            GlobalEnvStorage.profileIDCountList[str(GlobalEnvStorage.profileID)]['pageSize'] = GlobalEnvStorage.customerKeyword.pageSize
            GlobalEnvStorage.infoLogger.info('设置一页多少条成功')

    def getRowSummaryInfo(self, rowObject):
        try:
            title = rowObject.find_elements(By.CSS_SELECTOR, 'h3 a')[0].text
            if title.endswith('....'):
                title = title[0:-4]
            if title.endswith('...'):
                title = title[0:-3]
            title = title.strip()
            url = ''
            if GlobalEnvStorage.customerKeyword.title != None and GlobalEnvStorage.customerKeyword.title != '':
                urlObjs = rowObject.find_elements_by_css_selector('.c-showurl .c-showurl')
                if len(urlObjs) == 0:
                    urlObjs = rowObject.find_elements_by_css_selector('.c-showurl')
                if len(urlObjs) > 0:
                    url = urlObjs[0].text
                url = url.strip()
                if url.endswith('...'):
                    url = url[0:-3]
                url = url.strip()
                if url.endswith('/'):
                    url = url[0:-1]
                url = url.strip()
                rowSummaryInfo = RowSummaryInfo()
                rowSummaryInfo.title = title
                rowSummaryInfo.url = url
                return rowSummaryInfo
        except:
            return

    def clickxiaoxiala(self, element):
        n = randint(1, 100)
        if n <= int(GlobalEnvStorage.xiaoxiala_percentage):
            try:
                xiaoxiala = element.find_element(By.CSS_SELECTOR, '.c-icon.c-icon-triangle-down-g')
                self.scrolledIntoView(xiaoxiala, topMargin=GlobalEnvStorage.TargetMargin_PCTopMargin, bottomMargin=GlobalEnvStorage.TargetMargin_PCBottomMargin)
                GlobalEnvStorage.browserWrapper.locateAndClick(xiaoxiala, click=False)
                time.sleep(uniform(0.1, 2))
                cursor_pos = GlobalEnvStorage.dmFactory.dm.GetCursorPos()
                cursor_posX = cursor_pos[1]
                cursor_posY = cursor_pos[2]
                GlobalEnvStorage.dmFactory.simulateTrajectory(randint(int(cursor_posX - 300), int(cursor_posX + 300)), randint(int(cursor_posY - 300), int(cursor_posY + 300)), click=False)
                time.sleep(uniform(0.2, 0.5))
                GlobalEnvStorage.browserWrapper.locateAndClick(xiaoxiala, click=False)
                time.sleep(uniform(0.2, 0.5))
            except:
                GlobalEnvStorage.infoLogger.info('没有找到')

    def zhanneiSearch(self):
        if GlobalEnvStorage.customerKeyword.url is None or GlobalEnvStorage.customerKeyword.url == '':
            return
        zhanneiPercent = randint(1, 100)
        if GlobalEnvStorage.customerKeyword.terminalType == 'PC' and zhanneiPercent <= GlobalEnvStorage.customerKeyword.zhanneiPercent:
            url = zhangneiUrl(GlobalEnvStorage.customerKeyword.url)
            keywordInputFactory = KeywordInputFactory()
            n = randint(1, 100)
            if n <= 50:
                pf = WebDriverWait(GlobalEnvStorage.browser.driver, 20).until(expected_conditions.presence_of_all_elements_located((By.CSS_SELECTOR, '.pf')))[0]
                GlobalEnvStorage.browserWrapper.locateAndClick(pf)
                advancedSearch = WebDriverWait(GlobalEnvStorage.browser.driver, 10).until(expected_conditions.presence_of_all_elements_located((
                 By.CSS_SELECTOR, '.bdpfmenu >a')))[1]
                GlobalEnvStorage.browserWrapper.locateAndClick(advancedSearch)
                time.sleep(uniform(1, 2))

                gpc = GlobalEnvStorage.browser.evaluate_script('$("#adv-setting-4 >select[name=gpc]")')[0]
                GlobalEnvStorage.browserWrapper.locateAndClick(gpc)
                options = gpc.find_elements_by_tag_name('option')
                info = GlobalEnvStorage.browserWrapper.getElementLocationInfo(gpc)
                for idx in range(len(options)):
                    if str(GlobalEnvStorage.customerKeyword.limitTime) in options[idx].text:
                        GlobalEnvStorage.infoLogger.info('idx:%d, x:%s, y:%s, bar:%s', idx, info['x'], info['y'], GlobalEnvStorage.toolBarHeight)
                        GlobalEnvStorage.dmFactory.simulateTrajectory(info['x'] + randint(int(info['width'] * 0.2), int(info['width'] * 0.8)), info['y'] + GlobalEnvStorage.toolBarHeight + randint(int(info['height'] * 0.2), int(info['height'] * 0.5)) + (idx + 1) * info['height'])
                        break

                adv_keyword = WebDriverWait(GlobalEnvStorage.browser.driver, 10).until(expected_conditions.presence_of_all_elements_located((
                 By.CSS_SELECTOR, '#adv_keyword')))[0]
                if adv_keyword.get_attribute('value') == '':
                    GlobalEnvStorage.browserWrapper.locateAndClick(adv_keyword)
                    keywordInputFactory = KeywordInputFactory()
                    if GlobalEnvStorage.customerKeyword.supportPaste == 1:
                        n = randint(1, 100)
                        if n <= int(GlobalEnvStorage.inputMethod_paste):
                            keywordInputFactory.setClipboardData(GlobalEnvStorage.customerKeyword.keyword)
                            keywordInputFactory.pasteFromClipboard()
                        else:
                            keywordInputFactory.inputWords(GlobalEnvStorage.customerKeyword.keyword)
                    else:
                        keywordInputFactory.inputWords(GlobalEnvStorage.customerKeyword.keyword)
                urlElement = GlobalEnvStorage.browser.evaluate_script('$("#adv-setting-7 >input.c-input")')[0]
                GlobalEnvStorage.browserWrapper.locateAndClick(urlElement)
                if GlobalEnvStorage.customerKeyword.supportPaste == 1:
                    n = randint(1, 100)
                    if n <= int(GlobalEnvStorage.inputMethod_paste):
                        keywordInputFactory.setClipboardData(url)
                        keywordInputFactory.pasteFromClipboard()
                    else:
                        keywordInputFactory.inputWords(url)
                else:
                    keywordInputFactory.inputWords(url)
                keywordInputFactory.Enter()
                while 1:
                    if len(GlobalEnvStorage.browser.windows) == 1:
                        GlobalEnvStorage.infoLogger.info('wait')
                        time.sleep(1)

                GlobalEnvStorage.browser.windows.current = GlobalEnvStorage.browser.windows[-1]
            else:
                search_tool = WebDriverWait(GlobalEnvStorage.browser.driver, 20).until(expected_conditions.presence_of_all_elements_located((
                 By.CSS_SELECTOR, '.search_tool')))[0]
                GlobalEnvStorage.browserWrapper.locateAndClick(search_tool)
                time.sleep(uniform(1, 1.5))
                search_tool_si = GlobalEnvStorage.browser.evaluate_script('$(".search_tool_si")')[0]
                GlobalEnvStorage.browserWrapper.locateAndClick(search_tool_si)
                time.sleep(uniform(0.2, 0.5))
                si = GlobalEnvStorage.browser.evaluate_script('$("input[name=si]")')[0]
                GlobalEnvStorage.browserWrapper.locateAndClick(si)
                time.sleep(uniform(0.2, 0.5))
                if GlobalEnvStorage.customerKeyword.supportPaste == 1:
                    n = randint(1, 100)
                    if n <= int(GlobalEnvStorage.inputMethod_paste):
                        keywordInputFactory.setClipboardData(url)
                        keywordInputFactory.pasteFromClipboard()
                    else:
                        keywordInputFactory.inputWords(url)
                else:
                    keywordInputFactory.inputWords(url)
                submit = GlobalEnvStorage.browser.evaluate_script('$(".c-tip-timerfilter-si-submit")')[0]
                GlobalEnvStorage.browserWrapper.locateAndClick(submit)
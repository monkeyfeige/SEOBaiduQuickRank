# uncompyle6 version 3.2.2
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.6.3 (v3.6.3:2c5fed8, Oct  3 2017, 18:11:49) [MSC v.1900 64 bit (AMD64)]
# Embedded file name: C:\PycharmProjects\AutoOptimize\autooptimize\operatetarget\PCOperateTarget.py
import time, traceback
from random import randint, uniform
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.wait import WebDriverWait
from autooptimize.browser.browserFactory import BrowserFactory
from autooptimize.globalEnvStorage import GlobalEnvStorage
from autooptimize.keywordInputFactory import KeywordInputFactory
from autooptimize.model.rowSummaryInfo import RowSummaryInfo
from autooptimize.operatetarget.abstractOperateTarget import AbstractOperateTarget
from autooptimize.urlInputFactory import UrlInputFactory
from autooptimize.util.util import profileIDKeywordCount

class PCOperatetarget(AbstractOperateTarget):

    def getRowObjects(self, errorTime=0):
        if GlobalEnvStorage.customerKeyword.searchEngine == '百度' and GlobalEnvStorage.browser.driver.find_elements_by_css_selector('div.content_none') != []:
            time.sleep(uniform(2, 4))
            return
        if GlobalEnvStorage.customerKeyword.searchEngine == '搜狗' and GlobalEnvStorage.browser.driver.find_elements_by_css_selector('div#noresult_part1_container') != []:
            time.sleep(uniform(2, 4))
            return
        if GlobalEnvStorage.customerKeyword.searchEngine == '360' and GlobalEnvStorage.browser.driver.find_elements_by_css_selector('div#no-result') != []:
            time.sleep(uniform(2, 4))
            return
        try:
            RowObjects = WebDriverWait(GlobalEnvStorage.browser.driver, 30).until(expected_conditions.presence_of_all_elements_located((
             By.CSS_SELECTOR, GlobalEnvStorage.selector['rowobjects'])), message='element获取超时')
            for RowObject in RowObjects:
                if RowObject.text == '':
                    RowObjects.remove(RowObject)
                    continue

            return RowObjects
        except TimeoutException as e:
            if 'Message: timeout: Timed out receiving message from renderer' in str(e):
                errorTime += 1
                if errorTime <= 2:
                    GlobalEnvStorage.exceptionlogger.exception('第%s次重新加载', errorTime)
                    GlobalEnvStorage.browser.reload()
                    self.getRowObjects(errorTime)
                else:
                    raise Exception('超过重新加载的次数')

    def nextPage(self, pageNo=0):
        GlobalEnvStorage.infoLogger.info('下一页')
        doNext = False
        try:
            if self.hasNextPage():
                element = GlobalEnvStorage.browser.driver.find_elements_by_css_selector(GlobalEnvStorage.selector['page'])[0]
                self.scrolledIntoView(element, topMargin=GlobalEnvStorage.PageMargin_PCTopMargin, bottomMargin=GlobalEnvStorage.PageMargin_PCBottomMargin)
                if pageNo == 0:
                    nextPageElement = element.find_element(By.LINK_TEXT, GlobalEnvStorage.selector['page_text'])
                    GlobalEnvStorage.browserWrapper.locateAndClick(nextPageElement)
                else:
                    nextPageElement = element.find_element(By.LINK_TEXT, str(pageNo))
                    GlobalEnvStorage.browserWrapper.locateAndClick(nextPageElement)
            else:
                GlobalEnvStorage.infoLogger.info('电脑端没有下一页了,程序将继续')
        except Exception as e:
            GlobalEnvStorage.infoLogger.info('电脑端没有下一页了,程序将退出%s', e)
        finally:
            return doNext

    def NoResultClick(self, pageNo, targetRowObjects, needBack=True, start=1, end=100):
        if GlobalEnvStorage.customerKeyword.randomlyClickNoResult:
            n = randint(start, end)
            element = None
            if pageNo == 1:
                if n <= int(GlobalEnvStorage.NoResultClick_FirstPageThree):
                    GlobalEnvStorage.infoLogger.info('只是随机点击')
                    targetRowObject = targetRowObjects[randint(0, 2)]
                    element = self.isNotNagetive(targetRowObject)
                elif n <= int(GlobalEnvStorage.NoResultClick_FirstPageTen):
                    GlobalEnvStorage.infoLogger.info('只是随机点击')
                    targetRowObject = targetRowObjects[randint(0, len(targetRowObjects) - 1)]
                    element = self.isNotNagetive(targetRowObject)
                else:
                    return
            if pageNo == 2:
                if n <= int(GlobalEnvStorage.NoResultClick_SecondPageThree):
                    GlobalEnvStorage.infoLogger.info('只是随机点击')
                    targetRowObject = targetRowObjects[randint(0, 2)]
                    element = self.isNotNagetive(targetRowObject)
                elif n <= int(GlobalEnvStorage.NoResultClick_SecondPageTen):
                    GlobalEnvStorage.infoLogger.info('只是随机点击')
                    targetRowObject = targetRowObjects[randint(0, len(targetRowObjects) - 1)]
                    element = self.isNotNagetive(targetRowObject)
                else:
                    return
            if element:
                searchEngineWindowTitle = GlobalEnvStorage.browser.windows.current.title
                self.moveToTargetElementAndClick(element)
                time.sleep(uniform(GlobalEnvStorage.customerKeyword.pageRemainMinTime / 2, GlobalEnvStorage.customerKeyword.pageRemainMaxTime / 2))
                if needBack:
                    for windowIdx in range(len(GlobalEnvStorage.browser.windows)):
                        if GlobalEnvStorage.browser.windows[windowIdx].title == searchEngineWindowTitle:
                            KeywordInputFactory.Ctrl_Number(windowIdx + 1)
                            break

    def insideClick(self):
        GlobalEnvStorage.infoLogger.info('内页点击%s', GlobalEnvStorage.customerKeyword.waitTimeAfterClick)
        time.sleep(GlobalEnvStorage.customerKeyword.waitTimeAfterClick)
        entryPageCount = randint(GlobalEnvStorage.customerKeyword.entryPageMinCount, GlobalEnvStorage.customerKeyword.entryPageMaxCount)
        hrefList = WebDriverWait(GlobalEnvStorage.browser.driver, 30).until(expected_conditions.presence_of_all_elements_located((By.CSS_SELECTOR, 'a')))
        current_window_title = GlobalEnvStorage.browser.windows.current.title
        for idx in range(10):
            BrowserFactory.closeLast(current_window_title)
            GlobalEnvStorage.browserWrapper.locateAndClick(hrefList[randint(0, len(hrefList) - 1)])
            time.sleep(10)
            for idx in range(len(GlobalEnvStorage.browser.windows)):
                if GlobalEnvStorage.browser.windows[idx].title == current_window_title:
                    GlobalEnvStorage.browser.windows.current = GlobalEnvStorage.browser.windows[idx]
                    KeywordInputFactory.Ctrl_Number(idx + 1)
                    break

    def moveToTargetElementAndClick(self, element):
        self.scrolledIntoView(element, topMargin=GlobalEnvStorage.TargetMargin_PCTopMargin, bottomMargin=GlobalEnvStorage.TargetMargin_PCBottomMargin)
        GlobalEnvStorage.browserWrapper.locateAndClick(element, minTime=GlobalEnvStorage.customerKeyword.titleRemainMinTime, maxTime=GlobalEnvStorage.customerKeyword.titleRemainMaxTime)

    def jingjiaClick(self):
        percentage = randint(1, 100)
        if percentage <= GlobalEnvStorage.customerKeyword.baiduSemPercent:
            GlobalEnvStorage.infoLogger.info('广告点击')
            try:
                current_window_title = GlobalEnvStorage.browser.windows.current.title
                jingjia = GlobalEnvStorage.browser.driver.find_elements_by_css_selector(GlobalEnvStorage.selector['jingjia'])
                n = randint(0, len(jingjia) - 1)
                self.moveToTargetElementAndClick(jingjia[n])
                time.sleep(uniform(GlobalEnvStorage.customerKeyword.pageRemainMinTime / 2, GlobalEnvStorage.customerKeyword.pageRemainMaxTime / 2))
                BrowserFactory.closeLast(current_window_title)
                for idx in range(len(GlobalEnvStorage.browser.windows)):
                    if GlobalEnvStorage.browser.windows[idx].title == current_window_title:
                        GlobalEnvStorage.browser.windows.current = GlobalEnvStorage.browser.windows[idx]
                        KeywordInputFactory.Ctrl_Number(idx + 1)
                        break

            except:
                GlobalEnvStorage.infoLogger.info('没有广告')

    def multiClick(self, targetRowObject):
        GlobalEnvStorage.infoLogger.info('找到_______')
        clickNumPercentage = randint(1, 100)
        if clickNumPercentage <= GlobalEnvStorage.MutiClick_one:
            clickNum = 1
        else:
            if clickNumPercentage <= GlobalEnvStorage.MutiClick_two:
                clickNum = 2
            else:
                if clickNumPercentage <= GlobalEnvStorage.MutiClick_three:
                    clickNum = 3
                else:
                    clickNum = 4
                GlobalEnvStorage.infoLogger.info('clickNum %s', clickNum)
                searchEngineWindowTitle = GlobalEnvStorage.browser.windows.current.title
                for clickNumIdx in range(clickNum):
                    BrowserFactory.closeLast(searchEngineWindowTitle)
                    finalWindowIdx = 0
                    element = self.decideClickElement(targetRowObject)
                    self.moveToTargetElementAndClick(element)
                    time.sleep(uniform(GlobalEnvStorage.customerKeyword.pageRemainMinTime, GlobalEnvStorage.customerKeyword.pageRemainMaxTime))
                    if GlobalEnvStorage.hasNextWord:
                        for windowIdx in range(len(GlobalEnvStorage.browser.windows)):
                            if GlobalEnvStorage.browser.windows[windowIdx].title == searchEngineWindowTitle:
                                KeywordInputFactory.Ctrl_Number(windowIdx + 1)
                                finalWindowIdx = windowIdx
                                if clickNumIdx == clickNum - 1:
                                    self.clearInput()
                                break

                    elif clickNumIdx == clickNum - 1:
                        if clickNum == 1:
                            KeywordInputFactory.Ctrl_Number(finalWindowIdx + 2)
                        else:
                            KeywordInputFactory.Ctrl_Number(finalWindowIdx + clickNum)
                        GlobalEnvStorage.browser.windows.current = GlobalEnvStorage.browser.windows[finalWindowIdx]
                    else:
                        for windowIdx in range(len(GlobalEnvStorage.browser.windows)):
                            if GlobalEnvStorage.browser.windows[windowIdx].title == searchEngineWindowTitle:
                                KeywordInputFactory.Ctrl_Number(windowIdx + 1)
                                finalWindowIdx = windowIdx
                                break

    def decideClickElement(self, targetRowObject):
        element = None
        try:
            element = targetRowObject.find_element(By.CSS_SELECTOR, GlobalEnvStorage.selector['image'])
        except:
            GlobalEnvStorage.infoLogger.info('不存在图片')

        percentage = randint(1, 100)
        if element == None or percentage > int(GlobalEnvStorage.clickTarget_image):
            element = targetRowObject.find_elements(By.CSS_SELECTOR, GlobalEnvStorage.selector['title'])[0]
        return element

    def scrolledIntoView(self, element, topMargin=50, bottomMargin=50, maxCount=10):
        count = 0
        while True:
            top = element.location['y']
            scrollTop = GlobalEnvStorage.browser.evaluate_script('document.body.scrollTop')
            if scrollTop > top - GlobalEnvStorage.innerHeight + bottomMargin and scrollTop < top - topMargin or count >= maxCount:
                break
            else:
                if scrollTop < top - GlobalEnvStorage.innerHeight + bottomMargin:
                    GlobalEnvStorage.infoLogger.info('moving down')
                    GlobalEnvStorage.dmFactory.wheel(randint(3, 5), type='DOWN')
                    if randint(1, 100) <= 70:
                        GlobalEnvStorage.dmFactory.simulateTrajectoryTwo(randint(int(int(GlobalEnvStorage.PelsWidth) * 0.2), int(int(GlobalEnvStorage.PelsWidth) * 0.8)), randint(int(int(GlobalEnvStorage.PelsHeight) * 0.2), int(int(GlobalEnvStorage.PelsHeight) * 0.8)))
                else:
                    if randint(1, 100) <= 70:
                        GlobalEnvStorage.infoLogger.info('moving up')
                        GlobalEnvStorage.dmFactory.wheel(randint(1, 2), type='UP')
                        GlobalEnvStorage.dmFactory.simulateTrajectoryTwo(randint(int(int(GlobalEnvStorage.PelsWidth) * 0.2), int(int(GlobalEnvStorage.PelsWidth) * 0.8)), randint(int(int(GlobalEnvStorage.PelsHeight) * 0.2), int(int(GlobalEnvStorage.PelsHeight) * 0.8)))
            count += 1

    def clickkuaizhao(self, element):
        n = randint(1, 100)
        if n <= GlobalEnvStorage.customerKeyword.kuaizhaoPercent:
            try:
                kuaizhao = element.find_element(By.CSS_SELECTOR, GlobalEnvStorage.selector['kuaizhao'])
                GlobalEnvStorage.browserWrapper.locateAndClick(kuaizhao)
                time.sleep(uniform(1, 2))
                searchEngineWindowTitle = GlobalEnvStorage.browser.windows.current.title
                for windowIdx in range(len(GlobalEnvStorage.browser.windows)):
                    if GlobalEnvStorage.browser.windows[windowIdx].title == searchEngineWindowTitle:
                        KeywordInputFactory.Ctrl_Number(windowIdx + 1)
                        break

            except:
                GlobalEnvStorage.infoLogger.info('没有找到')

    def disturbOperate(self):
        if GlobalEnvStorage.entryUrl != 'https://www.baidu.com' and GlobalEnvStorage.entryUrl != 'https://www.sogou.com' and GlobalEnvStorage.entryUrl != 'https://www.so.com' and GlobalEnvStorage.entryUrl != 'http://www.soku.com':
            GlobalEnvStorage.newTarget = True
        if GlobalEnvStorage.newTarget:
            waitTime = 0
            while len(GlobalEnvStorage.browser.windows) == 1:
                GlobalEnvStorage.infoLogger.info('wait')
                time.sleep(0.5)
                if waitTime > 10:
                    element = WebDriverWait(GlobalEnvStorage.browser.driver, 20).until(expected_conditions.presence_of_all_elements_located((
                     By.CSS_SELECTOR, GlobalEnvStorage.searchButtom)))[0]
                    GlobalEnvStorage.browserWrapper.locateAndClick(element)
                else:
                    waitTime += 1

            GlobalEnvStorage.browser.windows.current = GlobalEnvStorage.browser.windows[1]
        else:
            url = GlobalEnvStorage.browser.windows.current.url
            if url == 'https://www.baidu.com/' or url == 'https://www.sogou.com/' or url == 'https://www.so.com/' or url == 'http://www.soku.com/':
                element = WebDriverWait(GlobalEnvStorage.browser.driver, 20).until(expected_conditions.presence_of_all_elements_located((
                 By.CSS_SELECTOR, GlobalEnvStorage.searchButtom)))[0]
                GlobalEnvStorage.browserWrapper.locateAndClick(element)
            time.sleep(2)
            if GlobalEnvStorage.customerKeyword.searchEngine == '百度' and GlobalEnvStorage.customerKeyword.terminalType == 'PC' and GlobalEnvStorage.entryUrl != 'https://www.baidu.com':
                self.initPageSize()
                time.sleep(2)
            searchEngineWindowTitle = GlobalEnvStorage.browser.windows.current.title
            try:
                if randint(1, 50) <= 50:
                    randomTarget = self.getRowObjects()
                    for idx in range(len(randomTarget)):
                        targetRowObject = randomTarget[randint(0, len(randomTarget)) - 1]
                        element = self.isNotNagetive(targetRowObject)
                        if element != None:
                            self.moveToTargetElementAndClick(element)
                            time.sleep(uniform(GlobalEnvStorage.customerKeyword.pageRemainMinTime / 2, GlobalEnvStorage.customerKeyword.pageRemainMaxTime / 2))
                            if GlobalEnvStorage.hasNextWord:
                                for windowIdx in range(len(GlobalEnvStorage.browser.windows)):
                                    if GlobalEnvStorage.browser.windows[windowIdx].title == searchEngineWindowTitle:
                                        GlobalEnvStorage.infoLogger.info('是第%s个window', windowIdx + 1)
                                        KeywordInputFactory.Ctrl_Number(windowIdx + 1)
                                        break

                            break

                else:
                    for idx in range(randint(3, 5)):
                        GlobalEnvStorage.dmFactory.wheel(randint(2, 3))
                        if randint(1, 100) <= 70:
                            GlobalEnvStorage.dmFactory.simulateTrajectoryTwo(x=uniform(100, 400), y=uniform(100, 600))
                            continue

            except Exception as e:
                GlobalEnvStorage.infoLogger.info('%s', e)
            finally:
                if GlobalEnvStorage.hasNextWord:
                    self.clearInput()

    def hasNextPage(self):
        return GlobalEnvStorage.browser.is_element_present_by_text(GlobalEnvStorage.selector['page_text'])

    def xialaclick(self, needBack=False, isKeyword=False):
        if GlobalEnvStorage.entryUrl != 'https://www.baidu.com' and GlobalEnvStorage.entryUrl != 'https://www.sogou.com' and GlobalEnvStorage.entryUrl != 'https://www.so.com' and GlobalEnvStorage.entryUrl != 'http://www.soku.com':
            GlobalEnvStorage.newTarget = True
        if GlobalEnvStorage.newTarget:
            waitTime = 0
            while len(GlobalEnvStorage.browser.windows) == 1:
                GlobalEnvStorage.infoLogger.info('wait')
                time.sleep(0.5)
                if waitTime > 10:
                    element = WebDriverWait(GlobalEnvStorage.browser.driver, 20).until(expected_conditions.presence_of_all_elements_located((
                     By.CSS_SELECTOR, GlobalEnvStorage.searchButtom)))[0]
                    GlobalEnvStorage.browserWrapper.locateAndClick(element)
                else:
                    waitTime += 1

            GlobalEnvStorage.browser.windows.current = GlobalEnvStorage.browser.windows[1]
        else:
            url = GlobalEnvStorage.browser.windows.current.url
            if url == 'https://www.baidu.com/' or url == 'https://www.sogou.com/' or url == 'https://www.so.com/' or url == 'http://www.soku.com/':
                element = WebDriverWait(GlobalEnvStorage.browser.driver, 20).until(expected_conditions.presence_of_all_elements_located((
                 By.CSS_SELECTOR, GlobalEnvStorage.searchButtom)))[0]
                GlobalEnvStorage.browserWrapper.locateAndClick(element)
            time.sleep(2)
            n = randint(1, 100)
        if 60 < n <= 90:
            self.nextPage()
        else:
            if n > 90:
                if self.nextPage():
                    time.sleep(2)
                self.nextPage()
            time.sleep(2)
            searchEngineWindowTitle = GlobalEnvStorage.browser.windows.current.title
            RowObjects = self.getRowObjects()
            element = None
            for i in range(len(RowObjects) - 1):
                rowObject = RowObjects[randint(0, len(RowObjects) - 1)]
                element = self.isNotNagetive(rowObject)
                if element:
                    break
                else:
                    RowObjects.remove(rowObject)

            if element:
                element = self.decideClickElement(RowObjects[randint(0, len(RowObjects) - 1)])
                self.moveToTargetElementAndClick(element)
                time.sleep(uniform(GlobalEnvStorage.customerKeyword.pageRemainMinTime, GlobalEnvStorage.customerKeyword.pageRemainMaxTime))
                if '_tj' in GlobalEnvStorage.customerKeyword.operationType and isKeyword:
                    try:
                        for windowIdx in range(len(GlobalEnvStorage.browser.windows)):
                            if GlobalEnvStorage.browser.windows[windowIdx].title == searchEngineWindowTitle:
                                KeywordInputFactory.Ctrl_Number(windowIdx + 1)
                                break

                        self.tjOperate()
                    except:
                        traceback.print_exc()
                        GlobalEnvStorage.infoLogger.info('页面超时继续执行')

                if needBack:
                    for windowIdx in range(len(GlobalEnvStorage.browser.windows)):
                        if GlobalEnvStorage.browser.windows[windowIdx].title == searchEngineWindowTitle:
                            KeywordInputFactory.Ctrl_Number(windowIdx + 1)
                            break

            else:
                if '_tj' in GlobalEnvStorage.customerKeyword.operationType and isKeyword:
                    try:
                        for windowIdx in range(len(GlobalEnvStorage.browser.windows)):
                            if GlobalEnvStorage.browser.windows[windowIdx].title == searchEngineWindowTitle:
                                KeywordInputFactory.Ctrl_Number(windowIdx + 1)
                                break

                        self.tjOperate()
                    except:
                        traceback.print_exc()
                        GlobalEnvStorage.infoLogger.info('页面超时继续执行')

        return searchEngineWindowTitle

    def clearInput(self):
        GlobalEnvStorage.relocation = False
        GlobalEnvStorage.infoLogger.info('开始删除字')
        GlobalEnvStorage.searchText = GlobalEnvStorage.selector['searchText']
        GlobalEnvStorage.searchButtom = GlobalEnvStorage.selector['searchButtom']
        previousPageInput = WebDriverWait(GlobalEnvStorage.browser.driver, 10).until(expected_conditions.presence_of_all_elements_located((By.CSS_SELECTOR, GlobalEnvStorage.searchText)))[0]
        length = len(previousPageInput.get_attribute('value'))
        self.scrolledIntoView(previousPageInput, topMargin=0, bottomMargin=GlobalEnvStorage.TargetMargin_PCBottomMargin)
        GlobalEnvStorage.browserWrapper.locateAndClick(previousPageInput)
        KeywordInputFactory.End()
        time.sleep(uniform(0.1, 0.2))
        i = length
        while 1:
            if i > 0:
                KeywordInputFactory.Delete()
                time.sleep(uniform(0.01, 0.1))
                i = i - 1

    def xialaOperate(self):
        profileIDKeywordCount()
        urlInputFactory = UrlInputFactory()
        urlInputFactory.input()
        self.initPageSize()
        keywordInputFactory = KeywordInputFactory()
        browserFactory = BrowserFactory()
        k1 = GlobalEnvStorage.customerKeyword.keyword
        if '_tj' in GlobalEnvStorage.customerKeyword.operationType and GlobalEnvStorage.customerKeyword.recommendedKeywords:
            k2 = GlobalEnvStorage.customerKeyword.recommendedKeywords[randint(0, len(GlobalEnvStorage.customerKeyword.recommendedKeywords) - 1)]
        else:
            k2 = GlobalEnvStorage.customerKeyword.title
        n = randint(1, 100)
        if n <= 20:
            keywordInputFactory.inputKeyword(k1)
            self.xialaclick(isKeyword=True)
            GlobalEnvStorage.browser.quit()
            browserFactory.initBrowser()
            urlInputFactory.input()
            keywordInputFactory.inputKeyword(k2)
            self.xialaclick()
        else:
            if n <= 30:
                keywordInputFactory.inputKeyword(k2)
                self.xialaclick()
                GlobalEnvStorage.browser.quit()
                browserFactory.initBrowser()
                urlInputFactory.input()
                keywordInputFactory.inputKeyword(k1)
                self.xialaclick(isKeyword=True)
            else:
                if n <= 60:
                    keywordInputFactory.inputKeyword(k1)
                    self.xialaclick(needBack=True, isKeyword=True)
                    self.clearInput()
                    keywordInputFactory.inputKeyword(k2)
                    self.xialaclick()
                else:
                    if n <= 70:
                        keywordInputFactory.inputKeyword(k2)
                        self.xialaclick(needBack=True)
                        self.clearInput()
                        keywordInputFactory.inputKeyword(k1)
                        self.xialaclick(isKeyword=True)
                    else:
                        if n <= 80:
                            keywordInputFactory.inputKeyword(k2)
                            self.xialaclick()
                        else:
                            if n <= 85:
                                keywordInputFactory.inputKeyword(k1)
                                self.xialaclick(isKeyword=True)
                            else:
                                keywordInputFactory.inputKeyword(k1)
                                if GlobalEnvStorage.entryUrl != 'https://www.baidu.com' and GlobalEnvStorage.entryUrl != 'https://www.sogou.com' and GlobalEnvStorage.entryUrl != 'https://www.so.com':
                                    GlobalEnvStorage.newTarget = True
                                if GlobalEnvStorage.newTarget:
                                    while 1:
                                        if len(GlobalEnvStorage.browser.windows) == 1:
                                            GlobalEnvStorage.infoLogger.info('wait')
                                            time.sleep(0.5)

                                    GlobalEnvStorage.browser.windows.current = GlobalEnvStorage.browser.windows[1]
                                time.sleep(uniform(2, 3))
                                self.clearInput()
                                keywordInputFactory.inputKeyword(k2)
                                self.xialaclick()
                            GlobalEnvStorage.optimizeCount = 1
                            GlobalEnvStorage.optimizeStatus = 'succ'

    def decideFile(self, pageNo):
        n = randint(1, 100)
        if n <= int(GlobalEnvStorage.NoFindFlip_nextPage):
            GlobalEnvStorage.infoLogger.info('pageNo:%s', pageNo)
            self.nextPage()
        else:
            self.nextPage(pageNo)

    def tjOperate(self):
        time.sleep(2)
        self.tjClick('#rs a')

    def tjClick(self, selector):
        list = []
        excludeKeywords = GlobalEnvStorage.customerKeyword.excludeKeywords
        negativeKeywords = GlobalEnvStorage.customerKeyword.negativeKeywords
        items = WebDriverWait(GlobalEnvStorage.browser.driver, 40).until(expected_conditions.presence_of_all_elements_located((By.CSS_SELECTOR, selector)))
        if len(items) > 0:
            for item in items:
                isNegativeElement = False
                if excludeKeywords is None or item.text.strip() not in excludeKeywords and negativeKeywords:
                    for negativeKeyword in negativeKeywords:
                        if negativeKeyword in item.text.strip():
                            isNegativeElement = True
                            break

                    if isNegativeElement:
                        continue
                    else:
                        list.append(item)
                        continue

        if len(list) > 0:
            GlobalEnvStorage.infoLogger.info('随机点击一次')
            self.moveToTargetElementAndClick(list[randint(0, len(list) - 1)])
            time.sleep(2)
            rowObjects = self.getRowObjects()
            element = None
            for i in range(len(rowObjects) - 1):
                rowObject = rowObjects[randint(0, len(rowObjects) - 1)]
                element = self.isNotNagetive(rowObjects)
                if element:
                    break
                else:
                    rowObjects.remove(rowObject)

            if element:
                self.moveToTargetElementAndClick(element)
                time.sleep(uniform(2, 4))
            GlobalEnvStorage.optimizeCount = 1
            GlobalEnvStorage.optimizeStatus = 'succ'

    def isNotNagetive(self, targetRowObject):
        element = None
        try:
            rowSummaryInfo = self.getRowSummaryInfo(targetRowObject)
            if rowSummaryInfo is None:
                element = targetRowObject
            else:
                title = rowSummaryInfo.title
            if title not in GlobalEnvStorage.specifiedKeywordNegativeLists:
                GlobalEnvStorage.infoLogger.info('%s,不是负面', title)
                element = self.decideClickElement(targetRowObject)
            else:
                GlobalEnvStorage.infoLogger.info('%s,是负面', title)
        except Exception as e:
            GlobalEnvStorage.infoLogger.info('随机点的目标没有标题或者url %s', e)
            element = self.decideClickElement(targetRowObject)
        finally:
            return element

    def mapNextPage(self):
        parentElement = GlobalEnvStorage.browser.driver.find_elements_by_css_selector('li.card')[0]
        GlobalEnvStorage.browserWrapper.locateAndMove(parentElement)
        element = GlobalEnvStorage.browser.driver.find_elements_by_css_selector(GlobalEnvStorage.selector['page'])[0]
        GlobalEnvStorage.dmFactory.wheel(3, type='DOWN')
        nextPageElement = element.find_element(By.LINK_TEXT, '下一页>')
        GlobalEnvStorage.browserWrapper.locateAndClick(nextPageElement)

    def getBaiduMapRowSummaryInfo(self, rowObject, pageNo):
        try:
            title = rowObject.find_elements(By.CSS_SELECTOR, 'div.row a')[0].text
            title = title.replace("'", '')
            order = rowObject.get_attribute('data-index')
            order = int(order) + 10 * (pageNo - 1)
            rowSummaryInfo = RowSummaryInfo()
            rowSummaryInfo.title = title
            rowSummaryInfo.order = order
            return rowSummaryInfo
        except:
            return

    def getYoukuRowSummaryInfo(self, rowObject):
        try:
            title = rowObject.find_elements(By.CSS_SELECTOR, 'div.v-meta-title a')[0].text
            if title == '播单':
                title = rowObject.find_elements(By.CSS_SELECTOR, 'div.v-meta-title a')[1].text
            title = title.lstrip()
            title = title.rstrip()
            title = title.replace("'", '')
            print(title)
            rowSummaryInfo = RowSummaryInfo()
            rowSummaryInfo.title = title
            return rowSummaryInfo
        except:
            return

    def clickSave(self):
        try:
            WebDriverWait(GlobalEnvStorage.browser.driver, 5).until(expected_conditions.presence_of_all_elements_located((
             By.CSS_SELECTOR, '.buttons-fav-icon.has-faved')))
            GlobalEnvStorage.infoLogger.info('已经被收藏')
        except Exception as e:
            saveButton = WebDriverWait(GlobalEnvStorage.browser.driver, 5).until(expected_conditions.presence_of_all_elements_located((
             By.CSS_SELECTOR, '.generalInfo-function-buttons-fav')))[0]
            GlobalEnvStorage.browserWrapper.locateAndClick(saveButton)
            GlobalEnvStorage.optimizeCount = 1
            GlobalEnvStorage.optimizeStatus = 'succ'
            GlobalEnvStorage.exceptionlogger.error('%s', GlobalEnvStorage.customerKeyword.keyword)
            GlobalEnvStorage.cookiesProfileList[str(GlobalEnvStorage.profileID)].append(GlobalEnvStorage.customerKeyword.keyword)

    def timesClick(self, targetRowObject, clickNum=4):
        GlobalEnvStorage.infoLogger.info('找到_______')
        GlobalEnvStorage.infoLogger.info('clickNum %s', clickNum)
        searchEngineWindowTitle = GlobalEnvStorage.browser.windows.current.title
        if clickNum == 0:
            return
        for clickNumIdx in range(clickNum):
            BrowserFactory.closeLast(searchEngineWindowTitle)
            finalWindowIdx = 0
            element = self.decideClickElement(targetRowObject)
            self.moveToTargetElementAndClick(element)
            time.sleep(uniform(GlobalEnvStorage.customerKeyword.pageRemainMinTime, GlobalEnvStorage.customerKeyword.pageRemainMaxTime))
            if GlobalEnvStorage.hasNextWord:
                for windowIdx in range(len(GlobalEnvStorage.browser.windows)):
                    if GlobalEnvStorage.browser.windows[windowIdx].title == searchEngineWindowTitle:
                        KeywordInputFactory.Ctrl_Number(windowIdx + 1)
                        finalWindowIdx = windowIdx
                        if clickNumIdx == clickNum - 1:
                            self.clearInput()
                        break

            elif clickNumIdx == clickNum - 1:
                if clickNum == 1:
                    KeywordInputFactory.Ctrl_Number(finalWindowIdx + 2)
                else:
                    KeywordInputFactory.Ctrl_Number(finalWindowIdx + clickNum)
                GlobalEnvStorage.browser.windows.current = GlobalEnvStorage.browser.windows[finalWindowIdx]
            else:
                for windowIdx in range(len(GlobalEnvStorage.browser.windows)):
                    if GlobalEnvStorage.browser.windows[windowIdx].title == searchEngineWindowTitle:
                        KeywordInputFactory.Ctrl_Number(windowIdx + 1)
                        finalWindowIdx = windowIdx
                        break
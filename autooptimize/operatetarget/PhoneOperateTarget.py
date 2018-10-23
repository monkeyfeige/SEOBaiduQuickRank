# uncompyle6 version 3.2.2
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.6.3 (v3.6.3:2c5fed8, Oct  3 2017, 18:11:49) [MSC v.1900 64 bit (AMD64)]
# Embedded file name: C:\PycharmProjects\AutoOptimize\autooptimize\operatetarget\PhoneOperateTarget.py
import time, traceback
from random import randint, uniform
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.wait import WebDriverWait
from autooptimize.browser.browserFactory import BrowserFactory
from autooptimize.globalEnvStorage import GlobalEnvStorage
from autooptimize.keywordInputFactory import KeywordInputFactory
from autooptimize.operatetarget.abstractOperateTarget import AbstractOperateTarget
from autooptimize.urlInputFactory import UrlInputFactory
from autooptimize.util.util import profileIDKeywordCount

class PhoneOperateTarget(AbstractOperateTarget):

    def disturbOperate(self):
        url = GlobalEnvStorage.browser.windows.current.url
        if url == 'https://m.baidu.com/' or url == 'https://m.sogou.com/' or url == 'http://m.sm.cn/':
            element = WebDriverWait(GlobalEnvStorage.browser.driver, 20).until(expected_conditions.presence_of_all_elements_located((
             By.CSS_SELECTOR, GlobalEnvStorage.searchButtom)))[0]
            GlobalEnvStorage.browserWrapper.locateAndClick(element)
        time.sleep(2)
        searchEngineUrl = GlobalEnvStorage.browser.windows.current.url
        print(searchEngineUrl)
        try:
            randomTarget = self.getRowObjects()
            for idx in range(len(randomTarget)):
                targetRowObject = randomTarget[randint(0, len(randomTarget)) - 1]
                element = self.isNotNegative(targetRowObject)
                if element != None:
                    self.closeApp()
                    self.moveToTargetElementAndClick(targetRowObject)
                    time.sleep(uniform(GlobalEnvStorage.customerKeyword.pageRemainMinTime, GlobalEnvStorage.customerKeyword.pageRemainMaxTime))
                    try:
                        if GlobalEnvStorage.hasNextWord:
                            KeywordInputFactory().UrlBack(url=searchEngineUrl)
                    except:
                        GlobalEnvStorage.infoLogger.info('页面超时继续执行')

                    break
                else:
                    print('--------------')

        except Exception as e:
            GlobalEnvStorage.infoLogger.info('%s', e)
        finally:
            if GlobalEnvStorage.hasNextWord:
                self.clearInput()

    def nextPage(self):
        GlobalEnvStorage.infoLogger.info('下一页')
        doNext = False
        try:
            if self.hasNextPage():
                nextPageElement = self.getNextPageObject()
                self.scrolledIntoView(nextPageElement, GlobalEnvStorage.PageMargin_PhoneTopMargin, GlobalEnvStorage.PageMargin_PCBottomMargin)
                GlobalEnvStorage.browserWrapper.locateAndClick(self.getNextPageObject())
                doNext = True
            else:
                GlobalEnvStorage.infoLogger.info('%s', '手机已经没有下一页,程序将继续')
        except:
            GlobalEnvStorage.infoLogger.info('%s', '手机已经没有下一页,程序将退出')
        finally:
            return doNext

    def moveToTargetElementAndClick(self, targetRowObject):
        GlobalEnvStorage.infoLogger.info('找到_______')
        self.scrolledIntoView(targetRowObject, GlobalEnvStorage.TargetMargin_PhoneTopMargin, GlobalEnvStorage.TargetMargin_PhoneBottomMargin)
        GlobalEnvStorage.browserWrapper.locateAndClick(targetRowObject, minTime=GlobalEnvStorage.customerKeyword.titleRemainMinTime, maxTime=GlobalEnvStorage.customerKeyword.titleRemainMaxTime)

    def scrolledIntoView(self, element, topMargin=50, bottomMargin=50, maxCount=15):
        count = 0
        while True:
            top = element.location['y']
            scrollTop = GlobalEnvStorage.browser.evaluate_script('document.body.scrollTop')
            if scrollTop > top - GlobalEnvStorage.innerHeight + bottomMargin + element.size['height'] / 2 and scrollTop < top - topMargin or count >= maxCount:
                break
            else:
                if scrollTop < top - GlobalEnvStorage.innerHeight + bottomMargin + element.size['height'] / 2:
                    GlobalEnvStorage.infoLogger.info('moving down')
                    GlobalEnvStorage.dmFactory.moveScrollBar(type='UP')
                else:
                    GlobalEnvStorage.infoLogger.info('moving up')
                    if scrollTop > top - topMargin + GlobalEnvStorage.innerHeight:
                        GlobalEnvStorage.dmFactory.moveScrollBar(type='DOWN')
                    else:
                        GlobalEnvStorage.dmFactory.moveScrollBar(type='S_DOWN')
            count += 1

    def NoResultClick(self, pageNo, targetRowObjects, needBack=True, start=1, end=100):
        element = None
        if GlobalEnvStorage.customerKeyword.randomlyClickNoResult:
            n = randint(start, end)
        if pageNo == 1:
            if n <= int(GlobalEnvStorage.NoResultClick_FirstPageThree):
                GlobalEnvStorage.infoLogger.info('只是随机点击')
                targetRowObject = targetRowObjects[randint(0, 2)]
                element = self.isNotNegative(targetRowObject)
            elif n <= int(GlobalEnvStorage.NoResultClick_FirstPageTen):
                GlobalEnvStorage.infoLogger.info('只是随机点击')
                targetRowObject = targetRowObjects[randint(0, len(targetRowObjects) - 1)]
                element = self.isNotNegative(targetRowObject)
            else:
                return
        if pageNo == 2 and GlobalEnvStorage.customerKeyword.searchEngine != '神马':
            if n <= int(GlobalEnvStorage.NoResultClick_SecondPageThree):
                GlobalEnvStorage.infoLogger.info('只是随机点击')
                targetRowObject = targetRowObjects[randint(0, 2)]
                element = self.isNotNegative(targetRowObject)
            elif n <= int(GlobalEnvStorage.NoResultClick_SecondPageTen):
                GlobalEnvStorage.infoLogger.info('只是随机点击')
                targetRowObject = targetRowObjects[randint(0, len(targetRowObjects) - 1)]
                element = self.isNotNegative(targetRowObject)
            else:
                return
        if pageNo == 0:
            targetRowObject = targetRowObjects[randint(0, len(targetRowObjects) - 1)]
            element = self.isNotNegative(targetRowObject)
        if element:
            searchEngineurl = GlobalEnvStorage.browser.windows.current.url
            self.moveToTargetElementAndClick(element)
            time.sleep(uniform(GlobalEnvStorage.customerKeyword.pageRemainMinTime, GlobalEnvStorage.customerKeyword.pageRemainMaxTime))
            try:
                if needBack:
                    KeywordInputFactory().UrlBack(url=searchEngineurl)
            except:
                GlobalEnvStorage.infoLogger.info('页面超时继续执行')

    def multiClick(self, targetRowObject):
        n = randint(1, 100)
        if n <= GlobalEnvStorage.MutiClick_one:
            clickNum = 1
        else:
            if n <= GlobalEnvStorage.MutiClick_two:
                clickNum = 2
            else:
                if n <= GlobalEnvStorage.MutiClick_three:
                    clickNum = 3
                else:
                    clickNum = 4
                if GlobalEnvStorage.customerKeyword.searchEngine == '神马':
                    clickNum = 1
                GlobalEnvStorage.infoLogger.info('clickNum %s', clickNum)
                searchEngineurl = GlobalEnvStorage.browser.windows.current.url
                for idx in range(clickNum):
                    self.moveToTargetElementAndClick(targetRowObject)
                    time.sleep(uniform(GlobalEnvStorage.customerKeyword.pageRemainMinTime, GlobalEnvStorage.customerKeyword.pageRemainMaxTime))
                    if idx == clickNum - 1:
                        if GlobalEnvStorage.hasNextWord:
                            KeywordInputFactory().UrlBack(url=searchEngineurl)
                    else:
                        try:
                            KeywordInputFactory().UrlBack(url=searchEngineurl)
                        except:
                            GlobalEnvStorage.infoLogger.info('页面超时继续执行')

                        rowObjects = self.getRowObjects()
                        GlobalEnvStorage.infoLogger.info('%s', len(rowObjects))
                        if rowObjects != None:
                            targetRowObject = self.comparison(rowObjects)
                            continue

    def isNotNegative(self, targetRowObject):
        element = None
        try:
            rowSummaryInfo = self.getRowSummaryInfo(targetRowObject)
            if rowSummaryInfo is None:
                element = targetRowObject
            else:
                title = rowSummaryInfo.title
            if title not in GlobalEnvStorage.specifiedKeywordNegativeLists:
                GlobalEnvStorage.infoLogger.info('%s,不是负面', title)
                element = targetRowObject
            else:
                GlobalEnvStorage.infoLogger.info('%s,是负面', title)
        except Exception as e:
            GlobalEnvStorage.infoLogger.info('随机点的目标没有标题或者url %s', e)
            element = targetRowObject
        finally:
            return element

    def decideFile(self, pageNo):
        GlobalEnvStorage.infoLogger.info('pageNo:%s', pageNo)
        self.nextPage()

    def xialaclick(self, needBack=False, isKeyword=False):
        url = GlobalEnvStorage.browser.windows.current.url
        if url == 'https://m.baidu.com/' or url == 'https://m.sogou.com/' or url == 'http://m.sm.cn/':
            element = WebDriverWait(GlobalEnvStorage.browser.driver, 20).until(expected_conditions.presence_of_all_elements_located((
             By.CSS_SELECTOR, GlobalEnvStorage.searchButtom)))[0]
            GlobalEnvStorage.browserWrapper.locateAndClick(element)
        time.sleep(2)
        self.closeApp()
        n = randint(1, 100)
        if 60 < n <= 90:
            self.nextPage()
        else:
            if n > 90:
                if self.nextPage():
                    time.sleep(2)
                self.nextPage()
            time.sleep(2)
            searchEngineurl = GlobalEnvStorage.browser.windows.current.url
            rowObjects = self.getRowObjects()
            element = None
            for i in range(len(rowObjects) - 1):
                rowObject = rowObjects[randint(0, len(rowObjects) - 1)]
                element = self.isNotNegative(rowObject)
                if element:
                    break
                else:
                    rowObjects.remove(rowObject)

            if element:
                self.moveToTargetElementAndClick(element)
                time.sleep(uniform(GlobalEnvStorage.customerKeyword.pageRemainMinTime, GlobalEnvStorage.customerKeyword.pageRemainMaxTime))
                if isKeyword and '_tj' in GlobalEnvStorage.customerKeyword.operationType:
                    try:
                        if randint(1, 100) <= 100:
                            KeywordInputFactory().UrlBack(url=searchEngineurl)
                            self.tjOperate()
                    except:
                        traceback.print_exc()
                        GlobalEnvStorage.infoLogger.info('页面超时继续执行')

                if needBack:
                    try:
                        KeywordInputFactory().UrlBack(url=searchEngineurl)
                    except:
                        GlobalEnvStorage.infoLogger.info('页面超时继续执行')

            else:
                if isKeyword and '_tj' in GlobalEnvStorage.customerKeyword.operationType:
                    try:
                        KeywordInputFactory().UrlBack(url=searchEngineurl)
                        self.tjOperate()
                    except:
                        traceback.print_exc()
                        GlobalEnvStorage.infoLogger.info('页面超时继续执行')

    def clearInput(self):
        GlobalEnvStorage.relocation = False
        GlobalEnvStorage.searchText = GlobalEnvStorage.selector['searchText']
        GlobalEnvStorage.searchButtom = GlobalEnvStorage.selector['searchButtom']
        previousPageInput = WebDriverWait(GlobalEnvStorage.browser.driver, 30).until(expected_conditions.presence_of_all_elements_located((By.CSS_SELECTOR, GlobalEnvStorage.searchText)))[0]
        self.scrolledIntoView(previousPageInput, topMargin=0, bottomMargin=GlobalEnvStorage.TargetMargin_PhoneBottomMargin)
        GlobalEnvStorage.browserWrapper.locateAndClick(previousPageInput)
        time.sleep(uniform(0.5, 0.7))
        if GlobalEnvStorage.browser.driver.find_elements_by_css_selector(GlobalEnvStorage.searchText)[0].get_attribute('value') != '':
            cross = WebDriverWait(GlobalEnvStorage.browser.driver, 30).until(expected_conditions.presence_of_all_elements_located((
             By.CSS_SELECTOR, GlobalEnvStorage.selector['reset'])))[0]
            GlobalEnvStorage.browserWrapper.locateAndClick(cross)

    def xialaOperate(self, start=1, end=100):
        newProfile = profileIDKeywordCount()
        urlInputFactory = UrlInputFactory()
        urlInputFactory.input(newProfile=newProfile)
        keywordInputFactory = KeywordInputFactory()
        browserFactory = BrowserFactory()
        k1 = GlobalEnvStorage.customerKeyword.keyword
        if '_tj' in GlobalEnvStorage.customerKeyword.operationType:
            k2 = GlobalEnvStorage.customerKeyword.recommendedKeywords[randint(0, len(GlobalEnvStorage.customerKeyword.recommendedKeywords) - 1)]
        else:
            k2 = GlobalEnvStorage.customerKeyword.title
        n = randint(start, end)
        if n <= 20:
            keywordInputFactory.inputKeyword(k1)
            self.xialaclick(isKeyword=True)
            GlobalEnvStorage.browser.quit()
            browserFactory.initBrowser()
            urlInputFactory.input(newProfile=newProfile)
            keywordInputFactory.inputKeyword(k2)
            self.xialaclick()
        else:
            if n <= 30:
                keywordInputFactory.inputKeyword(k2)
                self.xialaclick()
                GlobalEnvStorage.browser.quit()
                browserFactory.initBrowser()
                urlInputFactory.input(newProfile=newProfile)
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
                                time.sleep(uniform(2, 3))
                                self.clearInput()
                                keywordInputFactory.inputKeyword(k2)
                                self.xialaclick()
                            GlobalEnvStorage.optimizeCount = 1
                            GlobalEnvStorage.optimizeStatus = 'succ'

    def tjOperate(self):
        time.sleep(2)
        return self.tjClick('#relativewords div.rw-list .rw-item')

    def tjClick(self, selector):
        list = []
        excludeKeywords = GlobalEnvStorage.customerKeyword.excludeKeywords
        negativeKeywords = GlobalEnvStorage.customerKeyword.negativeKeywords
        items = WebDriverWait(GlobalEnvStorage.browser.driver, 40).until(expected_conditions.presence_of_all_elements_located((By.CSS_SELECTOR, selector)))
        if len(items) > 0:
            for item in items:
                isNegativeElement = False
                if (excludeKeywords is None or item.text.strip() not in excludeKeywords) and negativeKeywords:
                    for negativeKeyword in negativeKeywords:
                        if negativeKeyword in item.text.strip():
                            isNegativeElement = True
                            break

                    if isNegativeElement:
                        continue
                    else:
                        list.append(item)
                        continue

            searchEngineurl = GlobalEnvStorage.browser.windows.current.url
            if len(list) > 0:
                GlobalEnvStorage.infoLogger.info('随机点击一次')
                self.closeApp()
                self.moveToTargetElementAndClick(list[randint(0, len(list) - 1)])
                time.sleep(2)
                searchEngineurl = GlobalEnvStorage.browser.windows.current.url
                rowObjects = self.getRowObjects()
                element = None
                for i in range(len(rowObjects) - 1):
                    rowObject = rowObjects[randint(0, len(rowObjects) - 1)]
                    element = self.isNotNegative(rowObject)
                    if element:
                        break
                    else:
                        rowObjects.remove(rowObject)

                if element:
                    self.moveToTargetElementAndClick(element)
                    time.sleep(uniform(2, 4))
                GlobalEnvStorage.optimizeCount = 1
                GlobalEnvStorage.optimizeStatus = 'succ'
                return searchEngineurl
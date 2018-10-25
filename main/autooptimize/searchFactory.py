# uncompyle6 version 3.2.2
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.6.3 (v3.6.3:2c5fed8, Oct  3 2017, 18:11:49) [MSC v.1900 64 bit (AMD64)]
# Embedded file name: C:\PycharmProjects\AutoOptimize\autooptimize\searchFactory.py
from random import randint, uniform
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.wait import WebDriverWait
from autooptimize.globalEnvStorage import GlobalEnvStorage
from autooptimize.keywordInputFactory import KeywordInputFactory

class SearchFactory:

    def search(self, searchButtom=None):
        if searchButtom:
            searchButtom = searchButtom
        else:
            searchButtom = GlobalEnvStorage.searchButtom
        if GlobalEnvStorage.customerKeyword.terminalType == 'PC':
            n = randint(1, 100)
            if n <= int(GlobalEnvStorage.search_click):
                element = WebDriverWait(GlobalEnvStorage.browser.driver, 30).until(expected_conditions.presence_of_all_elements_located((By.CSS_SELECTOR, searchButtom)))[0]
                time.sleep(uniform(0.5, 1.5))
                info = GlobalEnvStorage.browserWrapper.locateAndClick(element)
            else:
                keywordInputFactory = KeywordInputFactory()
                keywordInputFactory.Enter()
        else:
            element = WebDriverWait(GlobalEnvStorage.browser.driver, 30).until(expected_conditions.presence_of_all_elements_located((By.CSS_SELECTOR, searchButtom)))[0]
            GlobalEnvStorage.browserWrapper.locateAndClick(element)
# -*- coding: utf-8 -*-
import os
import shutil
import threading
import time
import traceback
from configparser import ConfigParser
from datetime import datetime
from random import randint
from win32api import GetTickCount

from selenium.common.exceptions import WebDriverException

from autooptimize.dmFactory import DMFactory
from autooptimize.env import Env
from autooptimize.globalEnvStorage import GlobalEnvStorage
from autooptimize.operateprocess.processFactory import ProcessFactory
from autooptimize.serviceProxy import ServiceProxy
from autooptimize.util.scheduler import clearWindowsLogTask, closeSelfAndStart, schedulerJob, clearSystem
from autooptimize.util.util import changeCustomerKeyword, initResolution, reConnect, autoStart, \
    clearFile, hidewindows, hotKeys, startClear, writeHostFile, browserQuit, isOnline, clearLastMain, initCookies, \
    zhangneiUrl
from autooptimize.util.util import getCity, get_free_space_mb, getLogger
from autooptimize.util.webRedirect import webServerRun

"""
【clearSystem.bat】       清空系统日志
【logging.conf】          日志looger的配置
【server.ini】            宽带拨号和服务器的配置
【env.conf】              程序运行环境和参数配置
"""

if __name__ == '__main__':
    if GlobalEnvStorage.env != "Development":
        startClear(fisrtRun=True)

    # 每次重新打开都是，日志都是默认打开的。
    GlobalEnvStorage.exceptionlogger = getLogger('error')  # rootlogger，用于打印异常信息到log文件中。
    GlobalEnvStorage.infoLogger = getLogger('info')  # infologger，用于打印正常运行时信息到console中。

    Env().initGlobalEnvStorage()

    if GlobalEnvStorage.env != "Development":
        initResolution()  # 设置屏幕分辨率
        autoStart("main", r"C:\working\main.exe")
        GlobalEnvStorage.clientID = os.environ['COMPUTERNAME'].lower()
        # 每次重新启动，系统都是关闭的。
        # 显示程序主窗口和任务管理器窗口
        hidewindows()
        # 注册热键，用于控制程序窗口的显示(F6)和日志的开关(F7)
        t = threading.Thread(target=hotKeys)
        t.start()
        # 清空windows中Application、System、Security的日志
        clearWindowsLogTask()

        clearSystem()
    else:
        GlobalEnvStorage.clientID

    # 后台定时任务，包括清除日志、备份conf、自杀重启等
    schedulerJob()

    # 大漠插件，类似按键精灵
    DMFactory()

    # 接口代理
    serviceProxy = ServiceProxy()

    clearLastMain()

    keywordCount = 0
    WebDriverExceptionNum = 0
    if GetTickCount() / 1000 <= 5 * 60:
        GlobalEnvStorage.fail_num = 0

    while GlobalEnvStorage.fail_num <= 10:
        GlobalEnvStorage.newTarget = False
        GlobalEnvStorage.hasNextWord = False
        GlobalEnvStorage.relocation = True
        customerKeyword = None
        text = """
        {
          "keyword" : "优化推广",
          "uuid" : 2118603,
          "url" : "www.scdzic.com",
          "group" : "sogou_pm_paiming",
          "entryType" : "qz",
          "operationType" : "pc_zhannei_sogou",
          "relatedKeyword" : "",
          "currentPosition" : 10,
          "originalUrl" : "www.scdzic.com/",
          "title" : "",
          "baiduAdUrl" : "",
          "page" : 5,
          "pageSize" : 0,
          "kuaizhaoPercent" : 0,
          "baiduSemPercent" : 0,
          "dragPercent" : 0,
          "multiBrowser" : 1,
          "clearCookie" : 0,
          "zhanneiPercent" : 0,
          "zhanwaiPercent" : 4,
          "openStatistics" : 1,
          "disableStatistics" : 0,
          "entryPageMinCount" : 0,
          "entryPageMaxCount" : 0,
          "disableVisitWebsite" : 0,
          "pageRemainMinTime" : 3000,
          "pageRemainMaxTime" : 5000,
          "inputDelayMinTime" : 50,
          "inputDelayMaxTime" : 80,
          "slideDelayMinTime" : 700,
          "slideDelayMaxTime" : 1500,
          "titleRemainMinTime" : 1000,
          "titleRemainMaxTime" : 3000,
          "optimizeKeywordCountPerIP" : 1,
          "oneIPOneUser" : 0,
          "randomlyClickNoResult" : 0,
          "justVisitSelfPage" : 1,
          "sleepPer2Words" : 1,
          "supportPaste" : 1,
          "moveRandomly" : 1,
          "parentSearchEntry" : 0,
          "clearLocalStorage" : 1,
          "lessClickAtNight" : 0,
          "sameCityUser" : 0,
          "locateTitlePosition" : 0,
          "baiduAllianceEntry" : 0,
          "justClickSpecifiedTitle" : 0,
          "randomlyClickMoreLink" : 0,
          "moveUp20" : 0,
          "waitTimeAfterOpenBaidu" : 1000,
          "waitTimeBeforeClick" : 1000,
          "waitTimeAfterClick" : 5000,
          "maxUserCount" : 300,
          "currentTime" : "2018-04-07 17:02",
          "searchEngine" : "搜狗",
          "terminalType" : "PC",
          "broadbandAccount" : "059908029559",
          "broadbandPassword" : "100100",
          "negativeKeywords" : "",
          "excludeKeywords" : "",
          "recommendedKeywords" : "",
          "excludeTitles" : "",
          "remarks" : ""
        }
        """
        if GlobalEnvStorage.env != "Development":
            startClear()
        GlobalEnvStorage.optimizeCount = 0
        GlobalEnvStorage.optimizeStatus = "fail"
        GlobalEnvStorage.alive = datetime.now()
        # if 2 <= datetime.now().hour <= 6:
        #     time.sleep(5 * 60)
        #     GlobalEnvStorage.alive = datetime.now()
        #     time.sleep(5 * 60)
        #     GlobalEnvStorage.alive = datetime.now()
        #     time.sleep(5 * 60)
        #     GlobalEnvStorage.alive = datetime.now()
        #     time.sleep(5 * 60)
        #     GlobalEnvStorage.alive = datetime.now()
        #     time.sleep(5 * 60)
        #     GlobalEnvStorage.alive = datetime.now()
        try:
            if GlobalEnvStorage.env != "Development":
                # 1. 拨号  isOnline() 0联网,1断网
                if GlobalEnvStorage.optimizeKeywordCountPerIP == None or (
                                    keywordCount % GlobalEnvStorage.optimizeKeywordCountPerIP == 0 and GlobalEnvStorage.isConncet == 1):
                    reConnect()
            # 2. 取词好
            fetchCount = 0
            waitTime = 0
            while fetchCount < 5:
                try:
                    # customerKeyword = serviceProxy.getCustomerKeyword(GlobalEnvStorage.clientID)
                    customerKeyword = serviceProxy.getCustomerKeyword(text)
                    if customerKeyword == None:
                        fetchCount = fetchCount + 1
                    else:
                        break
                except Exception as e:
                    GlobalEnvStorage.infoLogger.info('%s,%s', waitTime, e)
                    GlobalEnvStorage.infoLogger.info('%s', isOnline())
                    if GlobalEnvStorage.env != "Development":
                        waitTime += 10
                        if waitTime <= 20:
                            time.sleep(waitTime)
                        else:
                            GlobalEnvStorage.infoLogger.info("系统崩溃,2分钟后再尝试")
                            time.sleep(60 * 2)
                            GlobalEnvStorage.alive = datetime.now()
                            waitTime = 0
                            reConnect()
            if customerKeyword == None:
                GlobalEnvStorage.infoLogger.info("连续5次都没取到词，5分钟后再尝试")
                if GlobalEnvStorage.env != "Development":
                    ServiceProxy.checkUpgrade(timeout=60)
                time.sleep(4 * 60)
                GlobalEnvStorage.alive = datetime.now()
                continue
            if GlobalEnvStorage.env != "Development":
                ServiceProxy.checkUpgrade()
            GlobalEnvStorage.customerKeyword = changeCustomerKeyword(customerKeyword)
            # GlobalEnvStorage.customerKeyword.randomlyClickNoResult = 1
            # GlobalEnvStorage.customerKeyword.operationType = "_pm"
            # GlobalEnvStorage.customerKeyword.terminalType = "Phone"
            # GlobalEnvStorage.customerKeyword.searchEngine = "搜狗"
            # GlobalEnvStorage.customerKeyword.operationType = "_xl_tj"
            # GlobalEnvStorage.customerKeyword.title = "《大秦帝国》最精彩的一段: 卫鞅舌战群臣不输诸葛亮"
            # GlobalEnvStorage.customerKeyword.keyword = "小米吃鸡"
            # GlobalEnvStorage.customerKeyword.url = "http://i-3.497.com/2017/10/24/93f8cba3-fa6e-46a3-a870-f50db00e905d.png"
            # GlobalEnvStorage.customerKeyword.title = "SEO综合查询 - 站长工具"
            # GlobalEnvStorage.customerKeyword.zhanneiPercent = 100

            # if GlobalEnvStorage.env != "Development":
            writeHostFile()
            if "_redirect" in GlobalEnvStorage.customerKeyword.operationType and GlobalEnvStorage.customerKeyword.remarks and GlobalEnvStorage.customerKeyword.remarks != "":
                if randint(1, 100) <= 10:
                    remarks = GlobalEnvStorage.customerKeyword.remarks.split(",")
                    remarks_url = remarks[randint(0, len(remarks) - 1)]
                    GlobalEnvStorage.customerKeyword.title = None
                    GlobalEnvStorage.redirect_url = r"http:\\" + GlobalEnvStorage.customerKeyword.url
                    GlobalEnvStorage.customerKeyword.url = remarks_url
                    server_url = zhangneiUrl(remarks_url)
                    GlobalEnvStorage.infoLogger.info("会使用redirect")
                    GlobalEnvStorage.infoLogger.info("server_url:%s", server_url)
                    GlobalEnvStorage.infoLogger.info("redirect_url:%s", GlobalEnvStorage.redirect_url)
                    with open("C:\\WINDOWS\\system32\\drivers\\etc\\hosts", "a") as f:
                        f.write("127.0.0.1 " + server_url + '\r\n')
                    t = threading.Thread(target=webServerRun, args=(server_url,))
                    t.start()

            if "_picture" in GlobalEnvStorage.customerKeyword.operationType:
                GlobalEnvStorage.customerKeyword.url = GlobalEnvStorage.customerKeyword.remarks
            initCookies()

            GlobalEnvStorage.optimizeKeywordCountPerIP = customerKeyword.optimizeKeywordCountPerIP

            if customerKeyword.keyword not in GlobalEnvStorage.NegativeLists:
                GlobalEnvStorage.specifiedKeywordNegativeLists = ServiceProxy.getSpecifiedKeywordNegativeLists()
                if GlobalEnvStorage.specifiedKeywordNegativeLists:
                    GlobalEnvStorage.NegativeLists[
                        customerKeyword.keyword] = GlobalEnvStorage.specifiedKeywordNegativeLists
            else:
                GlobalEnvStorage.specifiedKeywordNegativeLists = GlobalEnvStorage.NegativeLists[customerKeyword.keyword]

                # if GlobalEnvStorage.negativeSupportingDataList is None or GlobalEnvStorage.negativeSupportingDataList == []:
                #     GlobalEnvStorage.negativeSupportingDataList = ServiceProxy.getNegativeSupportingDataList()

            processFactory = ProcessFactory()
            processFactory.excecute()

            WebDriverExceptionNum = 0
            GlobalEnvStorage.fail_num = 0
        except ConnectionResetError:
            GlobalEnvStorage.exceptionlogger.exception(u"主方法异常,%s,%s,%s", GlobalEnvStorage.customerKeyword.keyword,
                                                       GlobalEnvStorage.UA,
                                                       GlobalEnvStorage.customerKeyword.searchEngine)
            traceback.print_exc()
            GlobalEnvStorage.fail_num += 1
            closeSelfAndStart(startNow=True)

        except ConnectionRefusedError:
            GlobalEnvStorage.exceptionlogger.exception(u"主方法异常,%s,%s,%s", GlobalEnvStorage.customerKeyword.keyword,
                                                       GlobalEnvStorage.UA,
                                                       GlobalEnvStorage.customerKeyword.searchEngine)
            traceback.print_exc()
            GlobalEnvStorage.fail_num += 1
            closeSelfAndStart(startNow=True)
        except WebDriverException as e:
            WebDriverExceptionNum += 1
            GlobalEnvStorage.exceptionlogger.exception(u"主方法异常,%s,%s,%s,%s", GlobalEnvStorage.customerKeyword.keyword,
                                                       GlobalEnvStorage.UA,
                                                       GlobalEnvStorage.customerKeyword.searchEngine, str(e))
            traceback.print_exc()
            GlobalEnvStorage.fail_num += 1
            if "cannot parse internal JSON template" in str(e):
                shutil.rmtree(r"C:\working\Chrome49\User Data\Default")
                os.mkdir(r"C:\working\Chrome49\User Data\Default")
                os.remove(r"C:\working\Chrome49\User Data\Local State")
                closeSelfAndStart(startNow=True)
            if WebDriverExceptionNum > 5:
                closeSelfAndStart(startNow=True)
        except Exception:
            GlobalEnvStorage.exceptionlogger.exception(u"主方法异常,%s,%s,%s,%s", GlobalEnvStorage.customerKeyword.keyword,
                                                       GlobalEnvStorage.UA,
                                                       GlobalEnvStorage.customerKeyword.searchEngine,
                                                       GlobalEnvStorage.entryUrl)
            GlobalEnvStorage.fail_num += 1
            traceback.print_exc()
        finally:
            GlobalEnvStorage.specifiedKeywordNegativeLists = None
            # 9. 更新操作结果
            # 8. 关闭浏览器
            cf = ConfigParser()
            if GlobalEnvStorage.env == "Development":
                cf.read("../config/dev/env.conf", encoding="utf-8-sig")
                cf.set("Basic", "last_profileID", str(GlobalEnvStorage.profileID))
                cf.set("Basic", "fail_num", str(GlobalEnvStorage.fail_num))
                cf.set("cookiesProfileList", "list", str(GlobalEnvStorage.cookiesProfileList))
                cf.set("profileIDCountList", "list", str(GlobalEnvStorage.profileIDCountList))
                cf.write(open("../config/dev/env.conf", "w", encoding="utf-8"))
            else:
                cf.read(r"C:\working" + "\env.conf", encoding="utf-8-sig")
                cf.set("Basic", "last_profileID", str(GlobalEnvStorage.profileID))
                cf.set("Basic", "fail_num", str(GlobalEnvStorage.fail_num))
                cf.set("cookiesProfileList", "list", str(GlobalEnvStorage.cookiesProfileList))
                cf.set("profileIDCountList", "list", str(GlobalEnvStorage.profileIDCountList))
                cf.write(open(r"C:\working\env.conf", "w", encoding="utf-8"))

            memoryFreeSpace = int(get_free_space_mb(os.getcwd()))
            city = getCity()
            browserQuit()
            if GlobalEnvStorage.httpServer:
                GlobalEnvStorage.httpServer.shutdown()
            clearFile(memoryFreeSpace)
            keywordCount += 1
            if customerKeyword:
                GlobalEnvStorage.infoLogger.info("%s", GlobalEnvStorage.UA)
                GlobalEnvStorage.infoLogger.info("GlobalEnvStorage.optimizeCount:%s,%s",
                                                 GlobalEnvStorage.optimizeCount,
                                                 GlobalEnvStorage.customerKeyword.keyword)
                if GlobalEnvStorage.profileID >= GlobalEnvStorage.customerKeyword.maxUserCount:
                    GlobalEnvStorage.profileID = 0
                else:
                    GlobalEnvStorage.profileID += 1
                GlobalEnvStorage.infoLogger.info("%s",
                                                 serviceProxy.updateOptimizeResult(GlobalEnvStorage.clientID,
                                                                                   memoryFreeSpace, city))
            else:
                GlobalEnvStorage.infoLogger.info("没取词,不更新")
    while True:
        if GlobalEnvStorage.env != "Development":
            ServiceProxy.checkUpgrade()
        GlobalEnvStorage.infoLogger.info("连续错误超过10次,进入等待状态")
        GlobalEnvStorage.alive = datetime.now()
        time.sleep(5 * 60)


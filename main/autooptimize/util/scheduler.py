# uncompyle6 version 3.2.2
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.6.3 (v3.6.3:2c5fed8, Oct  3 2017, 18:11:49) [MSC v.1900 64 bit (AMD64)]
# Embedded file name: C:\PycharmProjects\AutoOptimize\autooptimize\util\scheduler.py
import os, time, shutil
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.interval import IntervalTrigger
from autooptimize.globalEnvStorage import GlobalEnvStorage
from autooptimize.util.util import clearWindowsLog, cleanReqTimes

def schedulerJob():
    scheduler = BackgroundScheduler()
    trigger = IntervalTrigger(seconds=21600)
    scheduler.add_job(clearWindowsLogTask, trigger)
    trigger = IntervalTrigger(seconds=7200)
    scheduler.add_job(clearNegativeLists, trigger)
    trigger = IntervalTrigger(seconds=18000)
    scheduler.add_job(clearSystem, trigger)
    trigger = IntervalTrigger(seconds=10800)
    scheduler.add_job(backUpConf, trigger)
    trigger = IntervalTrigger(seconds=480)
    scheduler.add_job(closeSelfAndStart, trigger)
    scheduler.start()


def closeSelfAndStart(startNow=False):
    if GlobalEnvStorage.alive == GlobalEnvStorage.last_alive or startNow:
        GlobalEnvStorage.infoLogger.info('关闭自己')
        os.system('taskkill /f /im ' + 'chrome.exe')
        os.system('taskkill /f /im ' + 'chromedriver.exe')
        os.system('start C:\\working\\main.exe')
        os.system('taskkill /f /im ' + 'rasdial.exe')
        os.system('taskkill /f /im ' + 'cmd.exe')
        time.sleep(2)
        os.system('taskkill /f /pid ' + str(os.getpid()))
        os.system('taskkill /f /pid ' + str(os.getppid()))
    else:
        GlobalEnvStorage.last_alive = GlobalEnvStorage.alive


def closeIndex():
    if GlobalEnvStorage.alive == GlobalEnvStorage.last_alive:
        GlobalEnvStorage.infoLogger.info('10秒后关闭自己')
        time.sleep(10)
        os.system('start C:\\working\\index5.exe')
        os.system('taskkill /f /im ' + 'chrome.exe')
        os.system('taskkill /f /im ' + 'chromedriver.exe')
        os.system('taskkill /f /im ' + 'rasdial.exe')
        os.system('taskkill /f /im ' + 'cmd.exe')
        time.sleep(2)
        os.system('taskkill /f /pid ' + str(os.getpid()))
        os.system('taskkill /f /pid ' + str(os.getppid()))
    else:
        GlobalEnvStorage.last_alive = GlobalEnvStorage.alive


def closeXiala():
    if GlobalEnvStorage.alive == GlobalEnvStorage.last_alive:
        GlobalEnvStorage.infoLogger.info('10秒后关闭自己')
        time.sleep(10)
        os.system('start C:\\working\\xiala.exe')
        os.system('taskkill /f /im ' + 'chrome.exe')
        os.system('taskkill /f /im ' + 'chromedriver.exe')
        os.system('taskkill /f /im ' + 'rasdial.exe')
        os.system('taskkill /f /im ' + 'cmd.exe')
        time.sleep(2)
        os.system('taskkill /f /pid ' + str(os.getpid()))
        os.system('taskkill /f /pid ' + str(os.getppid()))
    else:
        GlobalEnvStorage.last_alive = GlobalEnvStorage.alive


def closeXialaTwo():
    if GlobalEnvStorage.alive == GlobalEnvStorage.last_alive:
        GlobalEnvStorage.infoLogger.info('10秒后关闭自己')
        time.sleep(10)
        os.system('start C:\\working\\xialatwo.exe')
        os.system('taskkill /f /im ' + 'chrome.exe')
        os.system('taskkill /f /im ' + 'chromedriver.exe')
        os.system('taskkill /f /im ' + 'rasdial.exe')
        os.system('taskkill /f /im ' + 'cmd.exe')
        time.sleep(2)
        os.system('taskkill /f /pid ' + str(os.getpid()))
        os.system('taskkill /f /pid ' + str(os.getppid()))
    else:
        GlobalEnvStorage.last_alive = GlobalEnvStorage.alive


def closeUrlxg():
    if GlobalEnvStorage.alive == GlobalEnvStorage.last_alive:
        GlobalEnvStorage.infoLogger.info('10秒后关闭自己')
        time.sleep(10)
        os.system('start C:\\working\\urlxg.exe')
        os.system('taskkill /f /im ' + 'chrome.exe')
        os.system('taskkill /f /im ' + 'chromedriver.exe')
        os.system('taskkill /f /im ' + 'rasdial.exe')
        os.system('taskkill /f /im ' + 'cmd.exe')
        time.sleep(2)
        os.system('taskkill /f /pid ' + str(os.getpid()))
        os.system('taskkill /f /pid ' + str(os.getppid()))
    else:
        GlobalEnvStorage.last_alive = GlobalEnvStorage.alive


def clearWindowsLogTask():
    GlobalEnvStorage.infoLogger.info('正在清空windows日志')
    clearWindowsLog()


def clearNegativeLists():
    GlobalEnvStorage.NegativeLists.clear()
    GlobalEnvStorage.negativeSupportingDataList.clear()


def clearSystem():
    GlobalEnvStorage.infoLogger.info('正在清除系统垃圾文件，请稍等...... ')
    os.system('start C:\\working\\clearSystem.bat')


def backUpConf():
    shutil.copyfile('c:\\working\\env.conf', 'c:\\working\\env_backup.conf')


def clearReqedTimes():
    GlobalEnvStorage.exceptionlogger.error('开始清空访问数')
    cleanReqTimes()
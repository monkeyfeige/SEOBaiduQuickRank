# uncompyle6 version 3.2.2
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.6.3 (v3.6.3:2c5fed8, Oct  3 2017, 18:11:49) [MSC v.1900 64 bit (AMD64)]
# Embedded file name: C:\PycharmProjects\AutoOptimize\autooptimize\dmFactory.py
import os, time, traceback, win32com.client
from random import randint
from autooptimize.globalEnvStorage import GlobalEnvStorage
from random import uniform
from autooptimize.util.scheduler import closeSelfAndStart

class DMFactory:
    dm = None

    def __init__(self):
        try:
            if GlobalEnvStorage.env != 'Development':
                GlobalEnvStorage.infoLogger.info(os.system('regsvr32 /s  "..\\bin\\dmcj\\dm.dll"'))
            else:
                GlobalEnvStorage.infoLogger.info(os.system('regsvr32 /s c:\\working\\dm.dll'))
            self.dm = win32com.client.Dispatch('dm.dmsoft')
            GlobalEnvStorage.dmFactory = self
            GlobalEnvStorage.infoLogger.info('创建DM成功')
            self.dm.SetMouseDelay('normal', 30)
            self.dm.SetKeypadDelay('normal', 30)
            self.dm.MoveTo(randint(100, 300), randint(100, 300))
        except:
            GlobalEnvStorage.exceptionlogger.exception('大漠初始化异常')
            traceback.print_exc()
            closeSelfAndStart(startNow=True)

    def simulateTrajectory(self, x, y, interval=0.001, minTime=0.2, maxTime=0.5, click=True, useadd=True):
        self.simulateTrajectoryTwo(x, y, interval=interval * 2, useadd=useadd)
        cursor_pos = self.dm.GetCursorPos()
        cursor_posX = cursor_pos[1]
        cursor_posY = cursor_pos[2]
        trajectory = int(((cursor_posX - x) ** 2 + (cursor_posY - y) ** 2) ** 0.5)
        for index in range(0, trajectory, 1):
            self.dm.MoveTo(cursor_posX + (x - cursor_posX) * ((index + 1) / trajectory), cursor_posY + (y - cursor_posY) * ((index + 1) / trajectory))
            time.sleep(interval)

        if click:
            self.dm.LeftClick()
        time.sleep(uniform(minTime, maxTime))

    def simulateTrajectoryTwo(self, x, y, interval=0.005, useadd=True):
        cursor_pos = self.dm.GetCursorPos()
        cursor_posX = cursor_pos[1]
        cursor_posY = cursor_pos[2]
        len = int(((cursor_posX - x) ** 2 + (cursor_posY - y) ** 2) ** 0.5) + 1
        add_x = 0
        add_y = 0
        if useadd:
            if GlobalEnvStorage.customerKeyword.terminalType == 'PC':
                add_x = randint(-10, 10)
                add_y = randint(-10, 10)
            else:
                add_x = randint(-3, 3)
                add_y = randint(-3, 3)
        for index in range(0, len, 2):
            cursor_pos = self.dm.GetCursorPos()
            cursor_posX = cursor_pos[1]
            cursor_posY = cursor_pos[2]
            trajectory = int(((cursor_posX - x) ** 2 + (cursor_posY - y) ** 2) ** 0.5) + 1
            if GlobalEnvStorage.customerKeyword.terminalType == 'PC':
                if trajectory <= 50:
                    break
            else:
                if trajectory <= 30:
                    break
                self.dm.MoveTo(cursor_posX + (x - cursor_posX) * ((index + 1) / len) + add_x, cursor_posY + (y - cursor_posY) * ((index + 1) / len) + add_y)
                time.sleep(interval)

    def wheel(self, count, type='DOWN', minTime=0.01, maxtTime=0.1):
        if type == 'UP':
            for index in range(count):
                GlobalEnvStorage.infoLogger.info('滚动Up %s %s', index, self.dm.WheelUp())
                time.sleep(uniform(minTime, maxtTime))

        else:
            for index in range(count):
                GlobalEnvStorage.infoLogger.info('滚动down %s %s', index, self.dm.WheelDown())
                time.sleep(uniform(minTime, maxtTime))

        time.sleep(uniform(GlobalEnvStorage.customerKeyword.slideDelayMinTime, GlobalEnvStorage.customerKeyword.slideDelayMaxTime))

    def moveScrollBar(self, type):
        if type == 'UP':
            x1 = uniform(GlobalEnvStorage.innerWidth * 0.4, GlobalEnvStorage.innerWidth * 0.8)
            y1 = uniform(GlobalEnvStorage.innerHeight * 0.7, GlobalEnvStorage.innerHeight * 0.9) + GlobalEnvStorage.toolBarHeight
            x2 = uniform(GlobalEnvStorage.innerWidth * 0.4, GlobalEnvStorage.innerWidth * 0.8)
            y2 = uniform(GlobalEnvStorage.innerHeight * 0.1, GlobalEnvStorage.innerHeight * 0.2) + GlobalEnvStorage.toolBarHeight
            self.dm.MoveTo(x1, y1)
            self.dm.LeftDown()
            self.simulateTrajectoryTwo(x2, y2, useadd=True, interval=0.005)
            self.dm.LeftUp()
            time.sleep(uniform(0.7, 1))
        else:
            x1 = uniform(GlobalEnvStorage.innerWidth * 0.4, GlobalEnvStorage.innerWidth * 0.8)
            y1 = uniform(GlobalEnvStorage.innerHeight * 0.7, GlobalEnvStorage.innerHeight * 0.9) + GlobalEnvStorage.toolBarHeight
            if type == 'S_DOWN':
                x2 = uniform(GlobalEnvStorage.innerWidth * 0.4, GlobalEnvStorage.innerWidth * 0.8)
                y2 = uniform(GlobalEnvStorage.innerHeight * 0.4, GlobalEnvStorage.innerHeight * 0.5) + GlobalEnvStorage.toolBarHeight
            else:
                x2 = uniform(GlobalEnvStorage.innerWidth * 0.4, GlobalEnvStorage.innerWidth * 0.8)
                y2 = uniform(GlobalEnvStorage.innerHeight * 0.1, GlobalEnvStorage.innerHeight * 0.2) + GlobalEnvStorage.toolBarHeight
            self.dm.MoveTo(x2, y2)
            self.dm.LeftDown()
            self.simulateTrajectoryTwo(x1, y1, useadd=True, interval=0.005)
            self.dm.LeftUp()
            time.sleep(uniform(0.3, 0.5))
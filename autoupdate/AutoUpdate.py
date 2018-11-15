import ctypes
import logging.config
import os
import shutil
import sys
import threading
import time
import traceback
import zipfile
from configparser import ConfigParser
from ctypes import wintypes
import subprocess
from random import choice

import psutil
import requests
import win32api
import win32con
import win32gui
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.interval import IntervalTrigger

from delphiencrypt import get_value1, UnEncryptString
from down_util import DownLoad

last_modified = "2018"

parentAbspath = os.path.dirname(os.path.abspath(sys.argv[0]))

# self_name = os.path.basename(sys.argv[0])
self_name = "AutoUpdate14.exe"

update_record_path = os.path.join(parentAbspath, "update_record.ini")


def isOnlineTwo():  # ipconfig触发ipconfig应用程序错误
    infoLogger.info("检测是否有网络....")
    r = subprocess.Popen("ipconfig", shell=True, stdout=subprocess.PIPE).stdout
    text = r.read().decode(encoding="GBK")
    r.close()
    # return True
    if "PPP" in text:
        infoLogger.info("有网络....")
        return True
    else:
        infoLogger.info("无网络....等待10秒")
        time.sleep(10)
        return False
    return True


def connect(name, username, password):
    tryTime = 0
    while tryTime <= 10:
        cmd_str = "rasdial %s %s %s" % (name, username, password)
        try:
            res = subprocess.call(cmd_str, shell=True, timeout=60)
        except:
            res = 1
        infoLogger.info("拨号命令退出")
        if res == 0:
            infoLogger.info("拨号成功")
            return True
        else:
            infoLogger.info("出现错误继续拨号")
            time.sleep(10)
        tryTime += 1
    return False


def disConnect():
    cmdstr = "rasdial /disconnect"
    subprocess.call(cmdstr, shell=True)


def unzip(zip_file, unzip_file, pwd):
    try:
        z = zipfile.ZipFile(zip_file, 'r')
        if pwd:
            z.extractall(path=unzip_file, pwd=pwd.encode())
        else:
            z.extractall(path=unzip_file)
    except:
        traceback.print_exc()
    finally:
        if z:
            z.close()


def isOnline():
    infoLogger.info("检测是否有网络....")
    # result=os.system('ping 8.8.8.8 -c 2')  #-c需要管理员权限
    ent = ["8.8.8.8", "114.114.114.114", "www.qq.com", "www.baidu.com"]
    result = subprocess.call('ping ' + choice(ent), shell=True)  # 0表示联网 1表示断网
    if result:
        infoLogger.info('ping fail,没有网咯')
        return False
    else:
        infoLogger.info('ping ok')
        return True


def writeUpdateTime():
    try:
        infoLogger.info("写入serverUpdateTime")
        cf = ConfigParser()
        cf.read(update_record_path, encoding="utf-8-sig")
        cf.set("download", "updatetime", time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))
        with open(update_record_path, "w") as fp:
            cf.write(fp)
        cf.clear()
    except:
        traceback.print_exc()
        if os.path.exists(update_record_path):
            os.remove(update_record_path)
        new_update_record(server_modified=last_modified)


def checkMain(versionEXE):
    infoLogger.info("判断主程序是否死亡....")
    if versionEXE == "new":
        cf = ConfigParser()
        cf.read(parentAbspath + "\\main_record.conf", encoding="utf-8-sig")
        updatetime = cf.get("Basic", "run_time")
        cf.clear()
        updatetime = time.mktime(time.strptime(updatetime, '%Y-%m-%d %H:%M:%S'))
        if time.time() - updatetime > 2 * 60:
            infoLogger.info("主程序死亡,重启主程序.....")
            subprocess.call("taskkill /f /im " + "chrome.exe", shell=True)
            subprocess.call("taskkill /f /im " + "chromerefresh.exe", shell=True)
            win32api.ShellExecute(None, "open", parentAbspath + "\main.exe", None, None,
                                  win32con.SW_HIDE)
        else:
            infoLogger.info("主程序正常运行.....")
    else:
        cf = ConfigParser()
        cf.read(parentAbspath + "\config.ini")
        updatetime = cf.get("set", "updatetime")
        updatetime = time.mktime(time.strptime(updatetime, '%Y-%m-%d %H:%M:%S'))
        cf.clear()
        if time.time() - updatetime > 10 * 60:
            infoLogger.info("主程序死亡,重启主程序.....")
            subprocess.call("taskkill /f /im " + "chrome.exe", shell=True)
            subprocess.call("taskkill /f /im " + "chromerefresh.exe", shell=True)
            win32api.ShellExecute(None, "open", parentAbspath + "\chromerefresh.exe", None, None,
                                  win32con.SW_HIDE)
        else:
            infoLogger.info("主程序正常运行.....")


def get_server_last_modified():
    try:
        server_modified = "2018"
        cf = ConfigParser()
        cf.read(parentAbspath + "\\update_record.ini", encoding="utf-8-sig")
        server_modified = cf.get("download", "last_modified")
    except:
        traceback.print_exc()
        server_modified = last_modified
        if os.path.exists(update_record_path):
            os.remove(update_record_path)
        new_update_record(server_modified=last_modified)
    finally:
        if cf:
            cf.clear()
        return server_modified


def write_server_last_modified(server_modified):
    try:
        cf = ConfigParser()
        cf.read(update_record_path, encoding="utf-8-sig")
        cf.set("download", "last_modified", server_modified)
        with open(update_record_path, "w") as fp:
            cf.write(fp)
    except:
        traceback.print_exc()
        if os.path.exists(update_record_path):
            os.remove(update_record_path)
        new_update_record(server_modified)
    finally:
        if cf:
            cf.clear()


def new_update_record(server_modified="2018"):
    cf = ConfigParser()
    cf.read(update_record_path)
    cf.add_section("download")
    cf.set("download", "updatetime", time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))
    cf.set("download", "last_modified", server_modified)
    with open(update_record_path, "w") as fp:
        cf.write(fp)
    cf.clear()


def getLogger(loggname):
    # logger = logging.getLogger("app")
    # file_handler = logging.FileHandler("info.log", encoding='utf-8')  # 在该日志处理器里添加编码,可以设置输出的日志文件的编码。
    # formatter = logging.Formatter('%(asctime)s %(levelname)-8s: %(message)s')
    # file_handler.setFormatter(formatter)
    # logger.addHandler(file_handler)
    logging.config.fileConfig(os.path.join(parentAbspath, "update_logging.conf"))  # 读取配置配置文件

    logger = logging.getLogger(loggname)  # 根据qualname读取配对应的logger对象
    return logger


exceptionlogger = getLogger('error')  # rootlogger，用于打印异常信息到log文件中。
infoLogger = getLogger('info')  # infologger，用于打印正常运行时信息到console中。

loggerState = True
windowsState = True


def logControl():
    global loggerState
    global infoLogger
    global exceptionlogger
    if loggerState:
        infoLogger.info("日志关闭")
        infoLogger = getLogger('root')
        exceptionlogger = getLogger('root')
        loggerState = False
    else:
        infoLogger = getLogger('info')
        exceptionlogger = getLogger('error')
        infoLogger.info("日志打开")
        loggerState = True


def windowsControl():
    global windowsState
    hwnd = win32gui.FindWindow(None, parentAbspath + "\\" + self_name)
    if windowsState:
        win32gui.ShowWindow(hwnd, win32con.SW_HIDE)
        windowsState = False
    else:
        hwnd = win32gui.FindWindow(None, parentAbspath + "\\" + self_name)
        win32gui.ShowWindow(hwnd, win32con.SW_SHOW)
        windowsState = True


def hotKeys():
    byref = ctypes.byref
    user32 = ctypes.windll.user32

    # 定义快捷键
    HOTKEYS = {
        1: (win32con.MOD_CONTROL + win32con.MOD_SHIFT, win32con.VK_F9),
        2: (win32con.MOD_CONTROL + win32con.MOD_SHIFT, win32con.VK_F10)
    }

    HOTKEY_ACTIONS = {
        1: windowsControl,
        2: logControl
    }
    # 快捷键对应的驱动函数

    # 注册快捷键
    for id, (mod, vk) in HOTKEYS.items():
        if not user32.RegisterHotKey(None, id, mod, vk):
            infoLogger.info("Unable to register id，%s", id)

    # 启动监听
    # try:
    msg = wintypes.MSG()
    while user32.GetMessageA(byref(msg), None, 0, 0) != 0:
        if msg.message == win32con.WM_HOTKEY:
            action_to_take = HOTKEY_ACTIONS.get(msg.wParam)
            if action_to_take:
                action_to_take()

                # user32.TranslateMessage(byref(msg))
                # user32.DispatchMessageA(byref(msg))

                # # 取消热键
                # finally:
                #     for id in HOTKEYS.keys():
                #         user32.UnregisterHotKey(None, id)


def clearLastAutoUpdate():
    pid = os.getpid()
    ppid = os.getppid()
    psutil.process_iter()
    for proc in psutil.process_iter():
        if proc.name() == self_name and proc.pid != pid and proc.pid != ppid:
            subprocess.call("taskkill /f /pid " + str(proc.pid), shell=True)


def get_version(check_url, param):
    version = None
    for i in range(3):
        try:
            get = requests.get(check_url, timeout=60, params=param)
            version = get.text
            if get.status_code == requests.codes.ok:
                if version != "" and version != "0" and len(version) <= 10:
                    infoLogger.info("目标version:%s" % version)
                else:
                    infoLogger.info("不需要更新.....")
                    version = None
                break
            else:
                version = None
        except:
            time.sleep(20)
            traceback.print_exc()
            version = None
    return version


def modify_password(check_password_url, password_update_callback, param):
    for i in range(3):
        try:
            password_state = requests.get(check_password_url, timeout=60, params=param)
            state = password_state.text
            if password_state.status_code == requests.codes.ok:
                if state != "" and state != "0" and len(state) == 8:
                    # infoLogger.info("目标密码:123%s456" % state)
                    result = subprocess.call("net user administrator %s" % state, shell=True)
                    subprocess.call(
                        """reg add "HKLM\SOFTWARE\Microsoft\Windows NT\CurrentVersion\Winlogon" /f /v AutoAdminLogon /d 1""",
                        shell=True)
                    subprocess.call(
                        """reg add "HKLM\SOFTWARE\Microsoft\Windows NT\CurrentVersion\Winlogon" /f /v DefaultUserName /d administrator""",
                        shell=True)
                    subprocess.call(
                        """reg add "HKLM\SOFTWARE\Microsoft\Windows NT\CurrentVersion\Winlogon" /f /v DefaultPassword /d %s""" % state,
                        shell=True)
                    infoLogger.info(result)
                    if result == 0:
                        requests.get(password_update_callback, timeout=60, params=param)
                        # print("修改密码成功，准备重启")
                        # os.system("shutdown -r -t 0 ")
                else:
                    infoLogger.info("不需要改密码.....")
                break
        except Exception as e:
            traceback.print_exc()
            infoLogger.info("修改密码报错，%d" % i)
            time.sleep(20)


def new_record():
    cf = ConfigParser()
    cf.read(parentAbspath + "\\record.conf")
    cf.add_section("Basic")
    cf.add_section("profileIDCountList")
    cf.set("Basic", "last_profileid", "0")
    cf.set("Basic", "fail_num", "0")
    cf.set("Basic", "success_num", "0")
    cf.set("profileIDCountList", "list", "{}")
    with open(parentAbspath + "\\record.conf", "w") as fp:
        cf.write(fp)
    cf.clear()


def get_current_version(versionEXE):
    current_version = None
    try:
        cf = ConfigParser()
        if versionEXE == "new":
            cf.read(parentAbspath + "\\env.conf", encoding="utf-8-sig")
            current_version = cf.get("Basic", "version")
        else:
            cf.read(parentAbspath + "\\version.ini", encoding="utf-8-sig")
            current_version = cf.get("set", "version")
        cf.clear()
    except:
        traceback.print_exc()
        current_version = None
    finally:
        return current_version


def get_zip_pwd(pwd_url, param):
    pwd = None
    for i in range(4):
        try:
            get = requests.post(pwd_url, timeout=60, json=param)
            if get.status_code == requests.codes.ok:
                pwd = get.json()
                pwd = pwd["value"]
                # infoLogger.info("解压密码是:123%s456" % pwd)
                break
            else:
                infoLogger.info("解压密码是:123456")
        except:
            infoLogger.info("解压密码是:1234567,休息20秒")
            time.sleep(20)
            traceback.print_exc()
    return pwd


main_run_time = time.time()


def checkSelf():
    if time.time() - main_run_time >= 60 * 5:
        infoLogger.info("主线程5分钟无反应，即将重启")
        win32api.ShellExecute(None, "open", os.path.join(parentAbspath, self_name), None, None, win32con.SW_HIDE)
    else:
        infoLogger.info("主线程运行正常。。。。。")


installer_path = os.path.join(parentAbspath, "Installer2.exe")
msvcr100_path = os.path.join(parentAbspath, "msvcr100.dll")
if __name__ == '__main__':
    try:
        windowsControl()

        clearLastAutoUpdate()
        t = threading.Thread(target=hotKeys)
        t.start()

        infoLogger.info("当前时间是:%s", time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))
        infoLogger.info("工作目录是:%s", parentAbspath)

        if os.path.exists(msvcr100_path) and os.path.exists("c:\work"):
            print("new开始注册msvcr100.dll")
            subprocess.call('copy "' + msvcr100_path + '"' + " c:\windows\system32", shell=True)
            subprocess.call('regsvr32 /s c:\windows\system32\msvcr100.dll', shell=True)
            time.sleep(10)
            try:
                os.remove(msvcr100_path)
            except:
                pass
        if os.path.exists("c:\chromerefresh6.zip"):
            os.remove("c:\chromerefresh6.zip")
        if os.path.exists("c:\working.zip"):
            os.remove("c:\working.zip")

        if os.path.exists(os.path.join(parentAbspath, "autoLogin.bat")):
            # subprocess.call("start " + os.path.join(parentAbspath, "autoLogin.bat"), shell=True) 无法执行
            win32api.ShellExecute(None, "open", os.path.join(parentAbspath, "autoLogin.bat"), None, None,
                                  win32con.SW_HIDE)
            time.sleep(5)
            os.remove(os.path.join(parentAbspath, "autoLogin.bat"))

        if os.path.exists(installer_path):
            if not os.path.exists("c:\change"):
                os.makedirs("c:\change")
                # 添加系统文件、隐藏文件属性
                subprocess.call("attrib +h +s c:\change", shell=True)
            shutil.move(installer_path, "c:\change\Installer2.exe")
        # 根据是否存在main.exe区分新老版本
        if os.path.exists(os.path.join(parentAbspath, "main.exe")):
            versionEXE = "new"
        else:
            versionEXE = "old"

        # versionEXE = "new"
        infoLogger.info("当前版本是:%s", versionEXE)

        if not os.path.exists(update_record_path):
            new_update_record(last_modified)

        infoLogger.info("读取配置文件......")

        cf = ConfigParser()
        # 读取配置
        if versionEXE == "new":
            try:
                from en import get_value, de

                re = get_value()
                download_host = de(re[0]).replace("_", "")
                remote_host = de(re[1]).replace("_", "")
                user = de(re[3]).replace("_", "")
                passw = de(re[2]).replace("_", "")

                cf.read(parentAbspath + "\server.ini", encoding="utf-8-sig")
                # user = cf.get("set", "user")
                # passw = cf.get("set", "pass")
                # download_host = cf.get("download", "host")

                isconncet = cf.get("Connect", "isconncet")
                name = cf.get("Connect", "name")
                username = cf.get("Connect", "username")
                password = cf.get("Connect", "password")
                cf.clear()
            except:
                traceback.print_exc()
                if os.path.exists(os.path.join(parentAbspath, "server_backup.ini")):
                    shutil.copyfile(os.path.join(parentAbspath, "server_backup.ini"),
                                    os.path.join(parentAbspath, "server.ini"))

        else:
            cf.read(os.path.join(parentAbspath, "server.ini"), encoding="utf-8-sig")
            user = cf.get("set", "user")
            passw = cf.get("set", "pass")
            remote_host = cf.get("set", "host")
            download_host = cf.get("download", "host")
            # re = get_value1()
            # download_host = UnEncryptString(re[0], "refreshhello")
            # print(download_host)
            # remote_host = UnEncryptString(re[1], "refreshhello")
            # print(remote_host)
            # user = UnEncryptString(re[3], "refreshhello")
            # print(user)
            # passw = UnEncryptString(re[2], "refreshhello")
            # print(passw)

            cf.read(os.path.join(parentAbspath, "config.ini"))
            name = cf.get("set", "connName")
            username = cf.get("set", "connuser")
            password = cf.get("set", "connpass")
            cf.clear()
        # remote_host="120.77.248.27:8098"
        # remote_host = "http://4zmznx.natappfree.cc"
        remote_host = remote_host.split(":")[0] + ":" + "8098"
        get_pwd_url = "http://" + remote_host + "/external/config/getZipEncryptionPassword"
        check_url = "http://" + remote_host + "/external/clientstatus/checkUpgrade"
        check_password_url = "http://" + remote_host + "/external/clientstatus/checkPassword"
        password_update_callback = "http://" + remote_host + "/external/clientstatus/updatePassword"
        clientID = os.environ['COMPUTERNAME'].lower()
        # clientID = "wuhandx66"

        # param = {"username": user,
        #          "password": passw,
        #          "clientID": "wfdx11"}
        param = {"username": user,
                 "password": passw,
                 "clientID": clientID}

        # zip_pwd = get_zip_pwd(pwd_url=get_pwd_url, param={"username": user, "password": passw})
        infoLogger.info("注入定时任务.....")
        scheduler = BackgroundScheduler()
        trigger = IntervalTrigger(seconds=20)  #
        scheduler.add_job(writeUpdateTime, trigger, id="writeUpdateTime")  # 间隔n秒钟执行一次
        trigger = IntervalTrigger(seconds=60 * 1.5)  #
        scheduler.add_job(checkMain, trigger, args=(versionEXE,), id="checkMain")
        trigger = IntervalTrigger(seconds=60 * 2)  #
        scheduler.add_job(checkSelf, trigger, id="checkSelf")

        scheduler.start()

        while True:
            version = None
            isOnlineRe = False
            while True:
                for i in range(5):
                    if isOnline():
                        isOnlineRe = True
                        break
                    else:
                        isOnlineRe = False
                if not isOnlineRe:
                    for i in range(5):
                        disConnect()
                        if connect(name, username, password):
                            break
                    continue
                modify_password(check_password_url, password_update_callback, param)
                version = get_version(check_url, param)
                current_version = get_current_version(versionEXE=versionEXE)
                if version and version != current_version:
                    if version == "reopen":
                        subprocess.call("taskkill /f /im " + "main.exe", shell=True)
                        subprocess.call("taskkill /f /im " + "chromerefresh.exe", shell=True)
                        subprocess.call("taskkill /f /im " + "chrome.exe", shell=True)
                        subprocess.call("taskkill /f /im " + "chromedriver.exe", shell=True)

                        win32api.ShellExecute(None, "open", "c:\change\Installer2.exe", None, None,
                                              win32con.SW_HIDE)
                        if os.path.exists("c:\change\server2.conf"):
                            os.remove("c:\change\server2.conf")
                        subprocess.call("taskkill /f /im " + self_name, shell=True)
                    else:
                        scheduler.pause_job("checkMain")
                        scheduler.pause_job("checkSelf")
                        break
                else:
                    if version and version == current_version:
                        infoLogger.info("版本已经一致,后台还没更新.....")
                    infoLogger.info("不需要更新.....")
                    infoLogger.info("等待60秒")
                    time.sleep(60)
                    main_run_time = time.time()

            subprocess.call("taskkill /f /im " + "main.exe", shell=True)
            subprocess.call("taskkill /f /im " + "chromerefresh.exe", shell=True)
            subprocess.call("taskkill /f /im " + "chrome.exe", shell=True)
            subprocess.call("taskkill /f /im " + "chromedriver.exe", shell=True)

            downLoadResult = False

            if versionEXE == "new":
                download_url = "http://" + download_host + "/new/" + version + "/main.zip"
                zip_file = os.path.join(parentAbspath, "main.zip")
                unzip_file = parentAbspath
                exePath = os.path.join(parentAbspath, "main.exe")
            else:
                download_url = "http://" + download_host + "/" + version + "/chromerefresh.zip"
                zip_file = os.path.join(parentAbspath, "chromerefresh.zip")
                unzip_file = parentAbspath
                exePath = os.path.join(parentAbspath, "chromerefresh.exe")

            server_modified = get_server_last_modified()
            last_modified = None
            while True:
                zip_pwd = None
                # zip_pwd = get_zip_pwd(pwd_url=get_pwd_url, param={"username": user, "password": passw})
                down_load = DownLoad(download_url, parentAbspath + "\\" + download_url.split('/')[-1])
                # 下载前记录last_modified
                last_modified = down_load.getLastModifiedTime()
                if last_modified is None:
                    infoLogger.info("获取last_modified失败,网络问题或者不存在版本%s更新包，休息两分钟", version)
                    time.sleep(120)
                    break
                if os.path.exists(zip_file + ".tmp"):
                    if last_modified != server_modified:
                        infoLogger.info("不是最新的文件的tmp,移除")
                        os.remove(zip_file + ".tmp")
                        downLoadResult = False
                    else:
                        infoLogger.info("是最新的文件的tmp,继续下载")
                        downLoadResult = False

                if os.path.exists(zip_file):
                    existSize = os.path.getsize(zip_file)
                    totalSize = down_load.getSize()
                    if existSize == totalSize and last_modified == server_modified:
                        infoLogger.info("文件已存在")
                        downLoadResult = True
                    else:
                        infoLogger.info("不是最新的文件,移除")
                        os.remove(zip_file)
                        downLoadResult = False

                if not downLoadResult:
                    write_server_last_modified(server_modified=last_modified)
                    downLoadResult = down_load.download()

                server_modified = last_modified
                write_server_last_modified(server_modified=last_modified)

                if downLoadResult:
                    infoLogger.info("下载完成,等待解压")
                    break
                else:
                    infoLogger.info("1分钟后再尝试下载")
                    time.sleep(1 * 60)
                    # 先断开连接
                    while True:
                        if not isOnline():
                            disConnect()
                            connectResult = connect(name, username, password)
                            if connectResult:
                                isOnlineResult = False
                                for idx in range(10):
                                    if isOnline():
                                        isOnlineResult = True
                                        break
                                    else:
                                        infoLogger.info("暂时没有网络")
                            if isOnlineResult:
                                break
                        else:
                            isOnlineResult = True
                            break
            if last_modified is None:
                infoLogger.info("目标版本一直获取不到,重新获取版本信息,并重新检测")
                scheduler.resume_job("checkMain")
                scheduler.resume_job("checkSelf")
                continue
            try:
                unzip(zip_file, unzip_file, pwd=zip_pwd + version)
                download_modified = "2018"
                if os.path.exists(parentAbspath + "\\" + zip_file):
                    os.remove(parentAbspath + "\\" + zip_file)
            except:
                traceback.print_exc()
                if os.path.exists(zip_file):
                    os.remove(zip_file)
                if os.path.exists(zip_file + ".tmp"):
                    os.remove(zip_file + ".tmp")

            if versionEXE == "new":
                try:
                    cf = ConfigParser()
                    cf.read(parentAbspath + "\\record.conf", encoding="utf-8-sig")
                    int(cf.get("Basic", "fail_num"))  #
                    int(cf.get("Basic", "last_profileID"))  #
                    eval(cf.get("profileIDCountList", "list"))  #
                    cf.set("Basic", "fail_num", "0")
                    with open(parentAbspath + "\\record.conf", "w", encoding="utf-8") as fp:
                        cf.write(fp)
                except:
                    if os.path.exists(parentAbspath + "\\record_backup.conf"):
                        try:
                            shutil.copyfile(parentAbspath + "\\record_backup.conf", parentAbspath + "\\record.conf")
                            cf = ConfigParser()
                            cf.read(parentAbspath + "\\record.conf", encoding="utf-8-sig")
                            int(cf.get("Basic", "fail_num"))  #
                            int(cf.get("Basic", "last_profileID"))  #
                            eval(cf.get("profileIDCountList", "list"))  #
                            cf.set("Basic", "fail_num", "0")
                            with open(parentAbspath + "\\record.conf", "w", encoding="utf-8") as fp:
                                cf.write(fp)
                        except:
                            if os.path.exists(parentAbspath + "\\record.conf"):
                                os.remove(parentAbspath + "\\record.conf")
                            if os.path.exists(parentAbspath + "\\record_backup.conf"):
                                os.remove(parentAbspath + "\\record_backup.conf")
                            new_record()
                    else:
                        if os.path.exists(parentAbspath + "\\record.conf"):
                            os.remove(parentAbspath + "\\record.conf")
                        new_record()
            else:
                pass
            # shutil.unpack_archive(zip_file, unzip_file,)
            # subprocess.call("start " + exePath)
            win32api.ShellExecute(None, "open", exePath, None, None, win32con.SW_HIDE)
            time.sleep(120)
            scheduler.resume_job("checkMain")
            scheduler.resume_job("checkSelf")
    except:
        traceback.print_exc()
        time.sleep(60)

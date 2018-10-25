# uncompyle6 version 3.2.2
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.6.3 (v3.6.3:2c5fed8, Oct  3 2017, 18:11:49) [MSC v.1900 64 bit (AMD64)]
# Embedded file name: C:\PycharmProjects\AutoUpdate\en.py
import win32api, os
from configparser import ConfigParser
import win32con
from Cryptodome.Cipher import AES

def en(message):
    obj = AES.new('qiuzongwang12345', AES.MODE_ECB)
    if len(message) % 16 != 0:
        message = message + (16 - len(message) % 16) * '_'
    ciphertext = obj.encrypt(message)
    ss = ''
    for i in ciphertext:
        ss = ss + str(i) + ' '

    ss = ss.strip()
    return ss


def de(ss):
    rr = []
    for i in ss.split(' '):
        rr.append(int(i))

    rr = bytes(rr)
    obj2 = AES.new('qiuzongwang12345', AES.MODE_ECB)
    detext = obj2.decrypt(rr)
    return detext.decode()


def set_value(re):
    KeyName = 'Software\\Microsoft\\Windows\\CurrentVersion\\Run'
    try:
        key = win32api.RegOpenKey(win32con.HKEY_CURRENT_USER, KeyName, 0, win32con.KEY_ALL_ACCESS)
        win32api.RegSetValueEx(key, 'downloadHost', 0, win32con.REG_SZ, re['downloadHost'])
        win32api.RegSetValueEx(key, 'host', 0, win32con.REG_SZ, re['host'])
        win32api.RegSetValueEx(key, 'pwd', 0, win32con.REG_SZ, re['pwd'])
        win32api.RegSetValueEx(key, 'user', 0, win32con.REG_SZ, re['user'])
        win32api.RegCloseKey(key)
    except:
        print('error')


def get_value():
    KeyName = 'Software\\Microsoft\\Windows\\CurrentVersion\\Run'
    try:
        key = win32api.RegOpenKey(win32con.HKEY_CURRENT_USER, KeyName, 0, win32con.KEY_ALL_ACCESS)
        downloadHost = win32api.RegQueryValueEx(key, 'downloadHost')[0]
        host = win32api.RegQueryValueEx(key, 'host')[0]
        pwd = win32api.RegQueryValueEx(key, 'pwd')[0]
        user = win32api.RegQueryValueEx(key, 'user')[0]
        win32api.RegCloseKey(key)
        return (
         downloadHost, host, pwd, user)
    except:
        print('error')


def set_regedit():
    if os.path.exists('c:\\working\\regedit.conf'):
        cf = ConfigParser()
        cf.read('c:\\working\\regedit.conf')
        downloadHost = cf.get('set', 'downloadHost')
        host = cf.get('set', 'host')
        pwd = cf.get('set', 'pass')
        user = cf.get('set', 'user')
        cf.clear()
        cf.read('c:\\working\\server.ini')
        cf.remove_option('set', 'user')
        cf.remove_option('set', 'pass')
        cf.remove_option('set', 'host')
        cf.remove_section('download')
        with open('c:\\working\\server.ini', 'w') as (fp):
            cf.write(fp)
        os.remove('c:\\working\\regedit.conf')
        downloadHost = en(downloadHost)
        host = en(host)
        pwd = en(pwd)
        user = en(user)
        re = {'downloadHost': downloadHost,  'host': host,  'pwd': pwd,  'user': user}
        set_value(re)
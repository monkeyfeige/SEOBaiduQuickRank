# uncompyle6 version 3.2.2
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.6.3 (v3.6.3:2c5fed8, Oct  3 2017, 18:11:49) [MSC v.1900 64 bit (AMD64)]
# Embedded file name: C:\PycharmProjects\AutoUpdate\delphiencrypt.py
from random import randint
import win32api, win32con, traceback

def EncryptString(Key, Source):
    KeyLen = len(Key)
    if KeyLen == 0:
        Key = 'delphi'
    KeyPos = 0
    Range = 256
    Offset = randint(0, Range)
    Dest = ('{:02x}').format(Offset)
    for s in Source:
        SrcAsc = (ord(s) + Offset) % 255
        if KeyPos < KeyLen - 1:
            KeyPos += 1
        else:
            KeyPos = 0
        SrcAsc = SrcAsc ^ ord(Key[KeyPos - 1])
        Dest = Dest + ('{:02x}').format(SrcAsc)
        Offset = SrcAsc

    return Dest.upper()


def UnEncryptString(Key, Source):
    KeyLen = None
    KeyPos = None
    Offset = None
    Dest = ''
    SrcPos = None
    SrcAsc = None
    TmpSrcAsc = None
    KeyLen = len(Key)
    if KeyLen == 0:
        Key = 'delphi'
    KeyPos = 0
    Offset = int(Source[0:2], 16)
    SrcPos = 3
    while 1:
        SrcAsc = int(Source[SrcPos - 1:SrcPos + 1], 16)
        if KeyPos < KeyLen - 1:
            KeyPos = KeyPos + 1
        else:
            KeyPos = 0
        TmpSrcAsc = SrcAsc ^ ord(Key[KeyPos - 1])
        if TmpSrcAsc <= Offset:
            TmpSrcAsc = 255 + TmpSrcAsc - Offset
        else:
            TmpSrcAsc = TmpSrcAsc - Offset
        Dest = Dest + chr(TmpSrcAsc)
        Offset = SrcAsc
        SrcPos = SrcPos + 2
        if SrcPos >= len(Source):
            break

    return Dest


def get_value1():
    KeyName = 'Software\\crefresh\\Value'
    try:
        key = win32api.RegOpenKey(win32con.HKEY_LOCAL_MACHINE, KeyName, 0, win32con.KEY_ALL_ACCESS)
        downloadHost = win32api.RegQueryValueEx(key, 'downHost')[0]
        host = win32api.RegQueryValueEx(key, 'host')[0]
        pwd = win32api.RegQueryValueEx(key, 'pass')[0]
        user = win32api.RegQueryValueEx(key, 'user')[0]
        win32api.RegCloseKey(key)
        return (
         downloadHost, host, pwd, user)
    except:
        traceback.print_exc()
        print('error')
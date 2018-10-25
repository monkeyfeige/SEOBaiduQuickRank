# uncompyle6 version 3.2.2
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.6.3 (v3.6.3:2c5fed8, Oct  3 2017, 18:11:49) [MSC v.1900 64 bit (AMD64)]
# Embedded file name: C:\PycharmProjects\AutoUpdate\down_util.py
import re, os, traceback, requests, sys, time

class DownLoad:

    def __init__(self, url, downPath):
        self.url = url
        self.downPath = downPath

    def getLastModifiedTime(self):
        last_modified = None
        headers = {'Range': 'bytes=0-4'}
        for i in range(5):
            try:
                with requests.head(self.url, headers=headers, timeout=60) as (r):
                    last_modified = r.headers['Last-Modified']
            except:
                last_modified = None
                traceback.print_exc()
                time.sleep(10)

        return last_modified

    def getSize(self):
        headers = {'Range': 'bytes=0-4'}
        try:
            r = requests.head(self.url, headers=headers, timeout=60)
            crange = r.headers['content-range']
            totalSize = int(re.match('^bytes 0-4/(\\d+)$', crange).group(1))
            return totalSize
        except:
            traceback.print_exc()

        try:
            totalSize = int(r.headers['content-length'])
        except:
            totalSize = 0

        return totalSize

    def getExistSize(self, filePath):
        if os.path.exists(filePath):
            existSize = os.path.getsize(filePath)
            return existSize
        else:
            return 0

    def download_file(self):
        filename = self.downPath + '.tmp'
        headers = {}
        headers['Range'] = 'bytes=%d-' % self.existSize
        r = requests.get(self.url, stream=True, headers=headers, timeout=40)
        with open(filename, 'ab') as (f):
            for chunk in r.iter_content(chunk_size=1024):
                if chunk:
                    self.existSize += len(chunk)
                    f.write(chunk)
                    f.flush()
                    sys.stdout.write(' \r')
                    sys.stdout.flush()
                    sys.stdout.write('下载: %.2f%%' % (self.existSize / self.totalSize * 100))
                    sys.stdout.flush()
                    continue

    def download(self, retry=5):
        try:
            if retry >= 0:
                self.existSize = self.getExistSize(filePath=self.downPath + '.tmp')
                self.totalSize = self.getSize()
                if self.existSize != 0 and self.existSize == self.totalSize:
                    print('上一次已经下载完成')
                    try:
                        os.renames(self.downPath + '.tmp', self.downPath)
                    except:
                        traceback.print_exc()

                    return True
                self.download_file()
                time.sleep(2)
                self.existSize = self.getExistSize(filePath=self.downPath + '.tmp')
                if self.existSize != 0 and self.totalSize == self.existSize:
                    print('校验安装包,下载完成')
                    try:
                        os.renames(self.downPath + '.tmp', self.downPath)
                    except:
                        traceback.print_exc()

                    return True
            else:
                print('重试次数为0，暂停下载')
                return False
        except:
            traceback.print_exc()
            retry -= 1
            print('下载失败，剩余下载次数%d' % retry)
            time.sleep(2)
            self.download(retry)
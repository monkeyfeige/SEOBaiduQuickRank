# uncompyle6 version 3.2.2
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.6.3 (v3.6.3:2c5fed8, Oct  3 2017, 18:11:49) [MSC v.1900 64 bit (AMD64)]
# Embedded file name: C:\PycharmProjects\AutoOptimize\autooptimize\browser\phoneBrowser.py
import time
from configparser import ConfigParser, NoSectionError, NoOptionError
from random import randint, uniform
from autooptimize.browser.abstractBrowser import AbstractBrowser
from autooptimize.globalEnvStorage import GlobalEnvStorage
from autooptimize.util.util import getUA

class PhoneBrowser(AbstractBrowser):

    def initUserAgent(self):
        phoneUA = None
        try:
            cf = ConfigParser()
            if GlobalEnvStorage.env == 'Development':
                cf.read('../config/dev/PhoneUA.conf', encoding='utf-8-sig')
            else:
                cf.read('C:\\working' + '\\PhoneUA.conf', encoding='utf-8-sig')
            phoneUA = eval(cf.get('PhoneUA', 'profile' + str(GlobalEnvStorage.profileID)))
        except NoSectionError as e:
            GlobalEnvStorage.infoLogger.info('%s', e)
            phoneUA = getUA()
            cf.add_section('PhoneUA')
            cf.set('PhoneUA', 'profile' + str(GlobalEnvStorage.profileID), str(phoneUA))
        except NoOptionError as e:
            GlobalEnvStorage.infoLogger.info('%s', e)
            phoneUA = getUA()
            cf.set('PhoneUA', 'profile' + str(GlobalEnvStorage.profileID), str(phoneUA))
        except BaseException as e:
            GlobalEnvStorage.infoLogger.info('%s', e)
        finally:
            GlobalEnvStorage.UA = phoneUA['userAgent']
            GlobalEnvStorage.innerHeight = phoneUA['deviceMetrics']['height']
            GlobalEnvStorage.innerWidth = phoneUA['deviceMetrics']['width']
            if GlobalEnvStorage.env == 'Development':
                cf.write(open('../config/dev/PhoneUA.conf', 'w'))
            else:
                cf.write(open('C:\\working' + '\\PhoneUA.conf', 'w'))

        self.chrome_options.add_experimental_option('mobileEmulation', phoneUA)

    def locateAndClick(self, element, minTime=0.2, maxTime=0.5, click=True):
        info = self.getElementLocationInfo(element)
        GlobalEnvStorage.dmFactory.dm.MoveTo(info['x'] + randint(int(info['width'] * 0.2), int(info['width'] * 0.6)), info['y'] + GlobalEnvStorage.toolBarHeight + randint(int(info['height'] * 0.15), int(info['height'] * 0.55)))
        time.sleep(uniform(minTime, maxTime))
        if click:
            GlobalEnvStorage.dmFactory.dm.LeftClick()
        GlobalEnvStorage.dmFactory.dm.MoveTo(randint(400, 800), randint(0, 50))
        return info
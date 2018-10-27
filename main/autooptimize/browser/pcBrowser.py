# uncompyle6 version 3.2.2
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.6.3 (v3.6.3:2c5fed8, Oct  3 2017, 18:11:49) [MSC v.1900 64 bit (AMD64)]
# Embedded file name: C:\PycharmProjects\AutoOptimize\autooptimize\browser\pcBrowser.py
from configparser import ConfigParser, NoSectionError, NoOptionError
from random import randint
from autooptimize.browser.abstractBrowser import AbstractBrowser
from autooptimize.globalEnvStorage import GlobalEnvStorage
from autooptimize.util.util import getUA

class PCBrowser(AbstractBrowser):

    def initUserAgent(self):
        pcUA = None
        try:
            cf = ConfigParser()
            if GlobalEnvStorage.env != 'Development':
                cf.read('../config/dev/PCUA.conf', encoding='utf-8-sig')
            else:
                cf.read('C:\\working\\PCUA.conf', encoding='utf-8-sig')
            pcUA = cf.get('PCUA', 'profile' + str(GlobalEnvStorage.profileID))
        except NoSectionError as e:
            GlobalEnvStorage.infoLogger.info('%s', e)
            pcUA = getUA()['userAgent']
            cf.add_section('PCUA')
            cf.set('PCUA', 'profile' + str(GlobalEnvStorage.profileID), pcUA)
        except NoOptionError as e:
            GlobalEnvStorage.infoLogger.info('%s', e)
            pcUA = getUA()['userAgent']
            cf.set('PCUA', 'profile' + str(GlobalEnvStorage.profileID), pcUA)
        except BaseException as e:
            GlobalEnvStorage.infoLogger.info('%s', e)
        finally:
            GlobalEnvStorage.UA = pcUA
            if GlobalEnvStorage.env != 'Development':
                GlobalEnvStorage.innerHeight = 970
                GlobalEnvStorage.innerWidth = GlobalEnvStorage.PelsWidth
                cf.write(open('../config/dev/PCUA.conf', 'w'))
            else:
                GlobalEnvStorage.innerHeight = GlobalEnvStorage.PelsHeight - 61 - 30
                GlobalEnvStorage.innerWidth = GlobalEnvStorage.PelsWidth
                cf.write(open('C:\\working\\PCUA.conf', 'w'))

        self.chrome_options.add_argument('user-agent=' + pcUA)

    def locateAndClick(self, element, minTime=0.2, maxTime=0.5, click=True):
        locationInfo = self.getElementLocationInfo(element)
        GlobalEnvStorage.dmFactory.simulateTrajectory(locationInfo['x'] + randint(int(locationInfo['width'] * 0.2), int(locationInfo['width'] * 0.8)), locationInfo['y'] + GlobalEnvStorage.toolBarHeight + randint(int(locationInfo['height'] * 0.2), int(locationInfo['height'] * 0.8)), minTime=minTime, maxTime=maxTime, click=click)
        return locationInfo

    def locateAndMove(self, element, minTime=0.2, maxTime=0.5, click=True):
        locationInfo = self.getElementLocationInfo(element)
        GlobalEnvStorage.dmFactory.simulateTrajectoryTwo(locationInfo['x'] + randint(int(locationInfo['width'] * 0.2), int(locationInfo['width'] * 0.8)), locationInfo['y'] + GlobalEnvStorage.toolBarHeight + randint(int(locationInfo['height'] * 0.2), int(locationInfo['height'] * 0.8)))
        return locationInfo
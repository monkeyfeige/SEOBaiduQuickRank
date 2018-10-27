# uncompyle6 version 3.2.2
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.6.3 (v3.6.3:2c5fed8, Oct  3 2017, 18:11:49) [MSC v.1900 64 bit (AMD64)]
# Embedded file name: C:\PycharmProjects\AutoOptimize\autooptimize\browser\abstractBrowser.py
from selenium.webdriver.chrome.options import Options
from splinter import Browser
from autooptimize.globalEnvStorage import GlobalEnvStorage

class AbstractBrowser:

    def __init__(self):
        self.chrome_options = Options()
        self.chrome_options.binary_location = GlobalEnvStorage.chromeExeFilePath

    def initBrowser(self, user=True):
        self.initUserAgent()
        if user:
            self.chrome_options.add_argument('profile-directory=Profile ' + str(GlobalEnvStorage.profileID))
            self.chrome_options.add_argument('user-data-dir=' + GlobalEnvStorage.chromeUserDataDir)
        self.chrome_options.add_argument('disable-infobars')
        self.chrome_options.add_argument('start-maximized')
        self.chrome_options.add_argument('disable-popup-blocking')
        self.chrome_options.add_argument('disable-gpu')
        self.chrome_options.add_argument('disable-bundled-ppapi-flash')
        self.chrome_options.add_argument('enable-quic')
        self.chrome_options.add_argument('dns-prefetch-disable')
        self.chrome_options.add_argument('disk-cache-dir=C:\\working\\cache')
        # GlobalEnvStorage.infoLogger.info('exe: %s', self.chrome_options.binary_location)
        # GlobalEnvStorage.infoLogger.info('dirver: %s', GlobalEnvStorage.chromeDriverFilePath)
        GlobalEnvStorage.browser = Browser(driver_name='chrome', options=self.chrome_options, executable_path=GlobalEnvStorage.chromeDriverFilePath)
        GlobalEnvStorage.infoLogger.info('%s', GlobalEnvStorage.browser)

    def getElementLocationInfo(self, element):
        x = element.location_once_scrolled_into_view['x']
        y = element.location_once_scrolled_into_view['y']
        width = element.size['width']
        height = element.size['height']
        locationInfo = {'x': x,  'y': y,  'width': width,  'height': height}
        return locationInfo

    def initUserAgent(self):
        GlobalEnvStorage.infoLogger.info('Please implement initUserAgent')

    def locateAndClick(self, element, minTime=0.5, maxTime=1):
        GlobalEnvStorage.infoLogger.info('Please implement locateAndClick')
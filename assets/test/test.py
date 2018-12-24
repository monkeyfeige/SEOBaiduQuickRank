from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from splinter import Browser


userDataDir = r'C:\working\Chrome49\User Data'
driverPath = r'C:\working\chromedriver.exe'
# driverPath = r'C:\Users\feizhang\Desktop\chromedriver.exe'
options = Options()
# options.binary_location = r'C:\working\chrome.exe'
# options.add_argument('user-data-dir=' + userDataDir)
options.binary_location = "C:\\working\\Chrome49\\Application\\chrome.exe"
driver = webdriver.Chrome(options = options, executable_path=r'C:\working\chromedriver.exe')
driver.get('http://baidu.com/')
# browser = Browser(driver_name='chrome', options=options, executable_path=driverPath)
# browser.visit("http://www.baidu.com/")
print("Chrome Browser Invoked")
# driver.quit()

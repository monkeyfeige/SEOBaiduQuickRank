1. pip install -r requirements.txt

APScheduler
lxml

psutil
pycryptodomex
pywin32

requests

selenium
splinter
six

2. 配置文件
"""
main.exe
"""
[PCUA.conf]             PC端UA列表
[PhoneUA.conf]          Phone端UA列表
[UAList.conf]           全部的UA列表

[logging.conf]          日志looger的配置
[server.ini]            宽带拨号和服务器接口的配置
[env.conf]              程序运行环境和参数配置
[version.ini]

"""
Autoupdate.exe
"""
[regedit.conf]          注册表接口信息配置
[update_record.ini]     更新记录
[config.ini]            客户端运行环境配置
[server.ini]            服务器及接口账号的配置
[update_logging.conf]   日志配置
[record.conf]           快排结果配置
[env.conf]
[server_backup.ini]

3. 程序插件
[autoLogin.bat]
[clearSystem.bat]       清空系统日志

[dm.dll]                大漠插件
[msvcr100.dll]          VC++依赖库


[Installer2.exe]        升级安装
[main.exe]              新版主程序
[chromerefresh.exe]     旧版主程序
[chrome.exe]            chrome
[chromedriver.exe]      chrome驱动

[cookies.txt]

4. 接口
"""
main.exe
"""
/external/customerkeyword/getCustomerKeyword
/external/customerkeyword/updateOptimizedCount
/external/negativelist/getSpecifiedKeywordNegativeLists
/external/clientstatus/updatePageNo
/external/negativeKeywordName/getNegativeSupportingData
/external/clientstatus/checkUpgrade

"""
Autoupdate.exe
"""
/external/config/getZipEncryptionPassword           获取更新程序
/external/clientstatus/checkUpgrade                 检查是否升级
/external/clientstatus/checkPassword                检查是否更新client账号
/external/clientstatus/updatePassword               获取更新client账号

/new/[version]/main.zip                             获取new主程序
/[version]/chromerefresh.zip                        获取主程序
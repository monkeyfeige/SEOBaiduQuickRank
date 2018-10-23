# uncompyle6 version 3.2.2
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.6.3 (v3.6.3:2c5fed8, Oct  3 2017, 18:11:49) [MSC v.1900 64 bit (AMD64)]
# Embedded file name: C:\PycharmProjects\AutoOptimize\autooptimize\util\webRedirect.py
from wsgiref.simple_server import make_server
from autooptimize.globalEnvStorage import GlobalEnvStorage

def application(environ, start_response):
    status = '301 Redirect'
    headers = [('Content-type', 'text/html;charset=utf-8'), ('Location', GlobalEnvStorage.redirect_url),
     ('Cache-Control', 'no-cache'), ('Server', '360wzws')]
    start_response(status, headers)
    return []


def webServerRun(url):
    httpd = make_server(url, 80, application)
    GlobalEnvStorage.httpServer = httpd
    print('Serving HTTP on port 80...')
    httpd.serve_forever()
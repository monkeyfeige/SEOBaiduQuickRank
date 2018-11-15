# uncompyle6 version 3.2.2
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.6.3 (v3.6.3:2c5fed8, Oct  3 2017, 18:11:49) [MSC v.1900 64 bit (AMD64)]
# Embedded file name: C:\PycharmProjects\AutoOptimize\autooptimize\model\entryUrl.py


class EntryUrl:
    url = None
    durationStart = None
    durationEnd = None
    searchText = None
    searchButton = None
    dropDownList = None
    skipPosition = None

    def __init__(self, data):
        self.__dict__ = data
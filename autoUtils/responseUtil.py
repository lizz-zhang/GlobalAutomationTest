# -*- coding: utf-8 -*-
"""
======================
@author:nash
@time:12/17/2021:3:18 PM
@email:nash.xiang@comm100.com
======================
"""


class ResponseReader:

    def __init__(self):
        self.keyResult = []
        self.valueResult = []

    def get_target_value(self, dic):
        if not isinstance(dic, dict) :  # 对传入数据进行格式校验
            return 'argv[1] not an dict or argv[-1] not an list '
        for key,value in dic.items():  # 传入数据不符合则对其value值进行遍历
            self.valueResult.append(value)
            if isinstance(value, dict):
                self.get_target_value(value)  # 传入数据的value值是字典，则直接调用自身
            elif isinstance(value, (list, tuple)):
                self.get_value(value)
        return self.valueResult

    def get_value(self,val):
        for val_ in val:
            if isinstance(val_, dict):
                self.get_target_value(val_)  # 传入数据的value值是字典，则调用get_target_value
            elif isinstance(val_, (list, tuple)):
                self.get_value(val_)   # 传入数据的value值是列表或者元组，则调用自身

    def get_Dict_Key_Value(self, keyStr, udict):
        if not isinstance(udict, dict) :  # 对传入数据进行格式校验
            return 'argv[1] not an dict'
        for key in udict.keys():  # 传入数据不符合则对其value值进行遍历
            keyString = ''
            if not keyStr:
                keyString = key
            else:
                keyString = keyStr + '.' + key
            self.keyResult.append(keyString)
            if isinstance(udict[key], dict):
                self.get_Dict_Key_Value(keyString,udict[key])  # 传入数据的value值是字典，则直接调用自身
            elif isinstance(udict[key], (list, tuple)):
                for val_ in udict[key]:
                    if isinstance(val_, dict):
                        self.get_Dict_Key_Value(keyString,val_)  # 传入数据的value值是字典，则调用get_target_value
            else:
                pass
        return self.keyResult
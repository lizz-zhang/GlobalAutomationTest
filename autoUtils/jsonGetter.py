# -*- coding: utf-8 -*-


valueResult = []
result = []


def _get_target_value(dic):
    if not isinstance(dic, dict):  # 对传入数据进行格式校验
        return "argv[1] not an dict or argv[-1] not an list "
    for key, value in dic.items():  # 传入数据不符合则对其value值进行遍历
        valueResult.append(value)
        if isinstance(value, dict):
            _get_target_value(value)  # 传入数据的value值是字典，则直接调用自身
        elif isinstance(value, (list, tuple)):
            _get_value(value)
    return valueResult


def _get_value(val):
    for val_ in val:
        if isinstance(val_, dict):
            _get_target_value(val_)  # 传入数据的value值是字典，则调用get_target_value
        elif isinstance(val_, (list, tuple)):
            _get_value(val_)  # 传入数据的value值是列表或者元组，则调用自身


def _get_test_value(val, tmp_list):
    for val_ in val:
        if isinstance(val_, dict):
            _get_target_value(val_, tmp_list)  # 传入数据的value值是字典，则调用get_target_value
        elif isinstance(val_, (list, tuple)):
            _get_value(val_, tmp_list)  # 传入数据的value值是列表或者元组，则调用自身


def getDictKeyValue(keyStr, udict):
    if not isinstance(udict, dict):  # 对传入数据进行格式校验
        return "argv[1] not an dict"
    for key in udict.keys():  # 传入数据不符合则对其value值进行遍历
        keyString = ""
        if not keyStr:
            keyString = key
        else:
            keyString = keyStr + "." + key
        result.append(keyString)
        if isinstance(udict[key], dict):
            getDictKeyValue(keyString, udict[key])  # 传入数据的value值是字典，则直接调用自身
        elif isinstance(udict[key], (list, tuple)):
            for val_ in udict[key]:
                if isinstance(val_, dict):
                    getDictKeyValue(
                        keyString, val_
                    )  # 传入数据的value值是字典，则调用get_target_value
        else:
            pass
    return result


def getDictUpdateStr(key, keyList, passDictStr, keyDict):
    if isinstance(keyDict[key], list):
        if str(keyList).endswith(key):
            passDictStr = passDictStr + "['" + key + "']"
        else:
            passDictStr = passDictStr + "['" + key + "'][0]"
        k = passDictStr + ' = ""'
    elif isinstance(keyDict[key], dict):
        passDict = passDictStr + "['" + key + "']"


def updateDictByKey(getkeyListFunc, getDictFunc):
    lResult = []
    initialDict = getDictFunc()
    keyList = getkeyListFunc("", initialDict)
    if not isinstance(keyList, list):  # 对传入数据进行格式校验
        return "argv[1] not a List"
    # 循环遍历字典的所有key，如果有子节点。就用.连接所有的几点。比如：bbb.c.c2
    for key in keyList:
        # 确保每次获取的字典都是一样的
        ardict = getDictFunc()
        # 对列表的每一项进行处理。已确定当前的节点，是否是dict或者是list，如果是dict就直接赋值。如果是list则需要拼装dict取值语句
        if str(key).count(".") > 0:
            k = "ardict"
            evalk = ""
            for i in key.split("."):
                # 拼接执行语句，eval调用可以返回执行的结果
                evalk = "isinstance(" + k + "['" + i + "']" + ", dict)"
                # print(evalk)
                # 判断当前节点是否是dict或者list
                isDict = eval(evalk)
                # 如果是dict，则拼接执行语句为dict['aaaa']。如果是list，则拼接执行语句为dict['aaaa'][0]['bb']
                if not isDict:
                    if str(key).endswith(i):
                        k = k + "['" + i + "']"
                    else:
                        k = k + "['" + i + "'][0]"
                elif isDict:
                    k = k + "['" + i + "']"
            # 拼接最后的值。可以自定义多个值，循环处理
            k = k + " = None"
            # 执行拼接的python语句。并不返回
            exec(k)
            # 将获取到的字典，加入到结果list中
            lResult.append(ardict)
        else:
            ardict[str(key)] = ""
            lResult.append(ardict)
        print(ardict)
        # writeFile(str(ardict))
    return lResult


# if __name__ == '__main__':
#
#
#     #flist = getDictKeyValue('',getDict())
#     #print(flist)
#     #print(getDict()['bbbb'][0]['cccc']['c1'])
#     #print(eval('isinstance(getDict()["bbbb"][0]["b1"], dict)'))
#     #for rdict in updateDictByKey(flist,ddict):
#         #print(updateDictByKey(getDictKeyValue,getDict))
#     for resultDic in updateDictByKey(getDictKeyValue,getDict):
#         writeFile(str(resultDic))
#
#     print(type(list))
#     print(isinstance(None, type(None)))
#

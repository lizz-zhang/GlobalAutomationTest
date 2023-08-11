# -*- coding: utf-8 -*-
"""
======================
@author:nash
@time:12/17/2021:3:18 PM
@email:nash.xiang@comm100.com
======================
"""
import json
import pdb
import re
import warnings

import pytest

from autoUtils.optionUtil import searchAndChangeDict, ifItemInKeysAndValueNotNone
from autoUtils.requestFactory import test_api_request
from autoUtils.responseUtil import ResponseReader
from jsonschema import validate, ValidationError
from deepdiff import DeepDiff
from deepdiff import grep
import logging
import operator

logger = logging.getLogger(__name__)


def commonResponseAssert(testResponse, expect):
    """
    :param testResponse:
    :param expect:
    :return:
    """
    if ifItemInKeysAndValueNotNone('responsestate',expect):
        logger.info("-------------------Prepare to verify the response state code！-------------------")
        assert testResponse.status_code == expect[
            'responsestate'], "Response Code is not correct, expect code: %s, actual code: %s,content is %s" % (
            expect['responsestate'], testResponse.status_code, testResponse.content)
        logger.info("-------------------Passed ：verify the response state code-------------------")

    if testResponse.content.__len__() > 0:

        if ifItemInKeysAndValueNotNone('responsejsonschemal', expect):
            responseDict = json.loads(testResponse.content)
            logger.info("-------------------Prepare to verify the response schema！-------------------")
            verifyJsonSchema(responseDict, expect['responsejsonschemal'])
            logger.info("-------------------Passed ：verify the response schema-------------------")
        if ifItemInKeysAndValueNotNone('responseitemcheck', expect):
            responseDict = json.loads(testResponse.content)
            responseCheckItems = expect['responseitemcheck']
            logger.info("-------------------Prepare to verify the response value-----------------")
            for item, itemvalue in responseCheckItems.items():
                if str(item).count('.') > 0:
                    k = 'responseDict'
                    if re.match(r'.*\[\*\].*', item):
                        if re.match(r'.*\[[0-9]+\].*', item):
                            # 暂时不处理这个复杂的场景，仅支持所有任意节点匹配。不支持任意节点和指定节点混合情况
                            # 混合情况考虑思路。获取到任意节点时的值，在对值进行指定节点进行验证
                            pass
                        else:
                            newItem = item.replace('[*].', '')
                        # 通过获取到dict的key和value。这里的key是指包含所有路径的。比如 bot['engine']['id']多层级别的。方便后续和expect里的key进行比较
                        # 重新将获取到的key和value，zip成一个tuple列表。用于循环去匹配值
                        responseReader = ResponseReader()
                        responseDictValue = responseReader.get_target_value(responseDict)
                        responseDictKey = responseReader.get_Dict_Key_Value('', responseDict)
                        tupleList = zip(responseDictKey, responseDictValue)
                        resultCount = 0
                        # pdb.set_trace()
                        for rTuple in tupleList:
                            # pdb.set_trace()
                            # 在这里，通过将response的key 和 value打包成zip对象。通过循环tuple来取值，进行比较，如果有匹配的对象。则resultCount就会置为1，没有找到则为0
                            if str(rTuple[0]) == newItem and rTuple[1] == itemvalue:
                                resultCount = 1
                        if resultCount == 0:
                            assert False, "The field %s doesn't match the expect value %s " % (item, itemvalue)
                        else:
                            resultCount == 0
                    else:
                        for i in item.split('.'):
                            # 拼接执行语句，eval调用可以返回执行的结果
                            if re.match(r'.*\[[0-9]+\].*', i):
                                k = k + i
                            else:
                                k = k + "['" + i + "']"
                        # 执行拼接的python语句。并不返回
                        # pdb.set_trace()
                        responseValue = eval(k)
                        assert str(responseValue) == str(
                            itemvalue), "The field [%s] didn't match the expect value: %s ,actual value is: %s" % (
                            item, itemvalue, responseValue)
                else:
                    responseValue = responseDict[item]
                    assert str(responseValue) == str(
                        itemvalue), "The field [%s] didn't match the expect value: %s ,actual value is: %s" % (
                        item, itemvalue, responseValue)
            logger.info("-------------------Passed ：verify the response value-------------------")


def afterCaseActionAndAssert(Url, commonHeader, testResponse, expect):

    """
    :param dashUrl:
    :param commonHeader:
    :param testResponse:
    :param expect:
    :return:
    """
    # 按照配置的参数，删除对应的值。保持测试环境清洁。这里也将涵盖DELETE接口一部分Case，Delete的接口这部分可不用重复编写。
    # 按照搜集bot相关的Delete接口，都会传入一个object的id。改object的id，均能在有返回对象中获取到（比如create接口的返回，可能就是刚创建的对象或者对象列表）
    if testResponse.status_code < 300:
        if testResponse.content.__len__() > 0:
            responseDict = json.loads(testResponse.content)
        if ifItemInKeysAndValueNotNone('aftercaseaction', expect):
            if ifItemInKeysAndValueNotNone('aftercasepath', expect):
                if expect['aftercaseaction'] == 'DELETE':
                    cleanResponse = test_api_request(
                        Url + searchAndChangeDict(responseDict, expect['aftercasepath']),
                        expect['aftercaseaction'], commonHeader, None)
                elif expect['aftercaseaction'] == 'PUT' or expect['aftercaseaction'] == 'POST':
                    cleanResponse = test_api_request(
                        Url + expect['aftercasepath'],
                        expect['aftercaseaction'], commonHeader, expect['aftercasebody'])
                pytest.assume(cleanResponse.status_code < 300)
                if cleanResponse.status_code >= 300:
                    logger.info("!!!!!Please note that, this case didn't take the after action successfully,it will impact the test result next time.Please check!!!!!")


def dbAssert(expect, dbconnection):
    if ifItemInKeysAndValueNotNone('dbcheck', expect):
        """
        数据库校验，是个值得讨论的问题：
        1，按照自动化分层和用户操作的角度，每个阶段的自动化测试可以只关注本阶段的验证。比如UI自动化，就是模拟用户的操作来验证界面的展示问题，故一般不会连接数据库进行相关校验
           接口测试自动化，是对请求接口的返回进行校验，从这个角度去看也是不太关注底层数据的变化
           单元测试，更贴近底层数据变化，应该进行数据库的校验
        2，我们这里的数据库校验，舍弃了对单张表进行校验的操作。也没有采用查询单张表变更范围校验。采用了执行数据库查询脚本来获取数据，再校验的方式。原因：
            a,数据库表结构足够多，对表操作的时间增加。从而使用例执行很慢
            b,单一数据表结构的比较，必须建立在用例对该表的操作必须是同步的，不能并行。并行可能导致数据库表包含其他操作，校验不准确
            c,查询数据库的系统日志，无法确认当前操作的日志。也不能并发执行用例。
        """
        expectDBDict = expect['dbcheck']
        for dKey, dValue in expectDBDict:
            cursor = None
            try:
                cursor = dbconnection['conn'].cursor()
                cursor.execute(dValue)
                rows = cursor.fetchall()
                expectList = dKey.split(',')
                actualList = list(rows)
                if not operator.eq(expectList, actualList):
                    assert False, "The DB value didn't match the expect value: %s ,actual value is: %s" % (
                        expectList, actualList)
            finally:
                cursor.close()


def illegalInputTestResponseAssert(testResponse, expect):
    logger.info("-------------------Prepare to verify the response state code！-------------------")
    assert testResponse.status_code == expect['responsestate'], "Response Code is not correct, expect code: %s, actual code: %s" % (
        expect['responsestate'], testResponse.status_code)
    logger.info("-------------------Passed ：verify the response state code-------------------")
    if testResponse.content.__len__() > 0:
        responseDict = json.loads(testResponse.content)
        if ifItemInKeysAndValueNotNone('error', expect):
            responseErrorCheck = expect['error']
            responseError = responseDict['error']
            errorResult = DeepDiff(responseErrorCheck, responseError, ignore_string_case=True)
            if errorResult:
                assert False, errorResult
        if ifItemInKeysAndValueNotNone('errormessage', expect):
            responseCheckItems = expect['errormessage']
            responseErrorMessage = responseDict['message']
            logger.info("-------------------Prepare to verify the errormessage-----------------")
            errorMessageResult = DeepDiff(responseCheckItems, responseErrorMessage, ignore_string_case=True)
            if errorMessageResult:
                assert False, errorMessageResult
            logger.info("-------------------Passed ：verify the errormessage-------------------")


def verifyJsonSchema(jsonResponse, schemaJson):
    testResult = ''
    try:
        validate(instance=jsonResponse, schema=schemaJson)
    except ValidationError as e:
        testResult = e
    print(testResult)
    assert testResult == '', testResult


def customAssert(testResponse, expect, *customExpect):
    """
    We can choose the extend verify tools to do the assert,such as: deepdiff, difflib, json-diff, json_tools and so on.
    我们可以采用全量response来校验：忽略大小写，忽略顺序，忽略字段等
    我们在对customcheck列表中的字段进行if else来进行判断。避免一条用例做多个测试点的检测导致测试报错，排错复杂度增加。且按照了验证优先级进行排列。
    *customExpect传入的参数，不是参数传入的对象。是一个参数元组，所以我们在使用参数元组拿到具体的custom 的expect时，需要通过 customExpect[0]方式获取
    """
    if testResponse.content.__len__() > 0:
        customResponseDict = json.loads(testResponse.content)
        if ifItemInKeysAndValueNotNone('customcheck', expect):
            customCheckItems = expect['customcheck']

            # 我们可以通过response_content，exclude_paths, exclude_regex_paths 去进行全量的response进行匹配
            # exclude_paths, exclude_regex_paths去过滤不需要匹配的字段
            # 这种全量匹配，都是默认忽略顺序和大小写的
            if ifItemInKeysAndValueNotNone("response_content", customCheckItems):
                if ifItemInKeysAndValueNotNone("exclude_paths", customCheckItems):
                    result = DeepDiff(customCheckItems['response_content'], customResponseDict, ignore_order=True,
                                      ignore_string_case=True, exclude_paths=customCheckItems['exclude_paths'])
                elif ifItemInKeysAndValueNotNone("exclude_regex_paths", customCheckItems):
                    result = DeepDiff(customCheckItems['response_content'], customResponseDict, ignore_order=True, ignore_string_case=True,
                                      exclude_regex_paths=customCheckItems['exclude_regex_paths'])
                else:
                    result = DeepDiff(customCheckItems['response_content'], customResponseDict, ignore_order=True, ignore_string_case=True)
                    # searchResult = customResponseDict | grep(customCheckItems['response_content'], use_regexp=True)
                if result:
                    assert False, result
            # 我们可以通过response_item_content，exclude_paths, exclude_regex_paths 去提取customExpect和testResponse中对应item的值进行全量匹配。
            # exclude_paths, exclude_regex_paths去过滤不需要匹配的字段
            # 这种全量匹配，都是默认忽略顺序和大小写的
            # 这里传入的customExpect是一个可直接校验的Dict对象（不包含不需要的keys）
            elif len(customExpect) == 1 and ifItemInKeysAndValueNotNone("response_item_content", customCheckItems):
                # 拿到需要提取的字段
                itemKey = customCheckItems['response_item_content']
                # 通过判断，传入的customExpect是否需要提取，来决定用于校验的期望值
                if ifItemInKeysAndValueNotNone(itemKey, customExpect[0]):
                    customExpectItem = customExpect[0][itemKey]
                else:
                    customExpectItem = customExpect[0]
                # 判断是否需要进行忽略路径匹配，并通过传入的字段来提取response中该字段的值。用来进行全量校验
                if ifItemInKeysAndValueNotNone("exclude_paths", customCheckItems):
                    result = DeepDiff(customExpectItem, customResponseDict[itemKey], ignore_order=True,
                                      ignore_string_case=True, exclude_paths=customCheckItems['exclude_paths'])
                elif ifItemInKeysAndValueNotNone("exclude_regex_paths", customCheckItems):
                    result = DeepDiff(customExpectItem, customResponseDict[itemKey], ignore_order=True, ignore_string_case=True,
                                      exclude_regex_paths=customCheckItems['exclude_regex_paths'])
                else:
                    result = DeepDiff(customExpectItem, customResponseDict[itemKey], ignore_order=True, ignore_string_case=True)
                    # searchResult = customResponseDict | grep(customCheckItems['response_content'], use_regexp=True)
                if result:
                    assert False, result
            # 查询所有的接口校验：
            # 这里获取customExpect的时候是一个元组，并不是传入的那个期望对象。在这里要拿到期望对象，需要tuple[0]
            # customExpect的值是包含其他一个标识的key如[key：校验对象]
            # 我们可以通过传入自定义的customExpect值，去进行全量查询时，把初始化的对象用来和查询的结果集进行In操作。原则上我初始化创建的对象，应该会在该对象的全量查询接口中
            # 对于部分全量查询，还有个数检查的。我们通过统计查出来的记录和实际值进行对比
            elif len(customExpect) == 1 and ifItemInKeysAndValueNotNone("keyInSelectResult", customCheckItems):
                objectKey = str(customCheckItems["keyInSelectResult"])
                if ifItemInKeysAndValueNotNone(objectKey, customResponseDict):
                    # 对于部分查询结果，会自动带入include的结果。此时期望的返回值中就不包含这部分字段。我们需要将实际的结果把那部分去掉，然后再做In的操作
                    diffKeys = list(customResponseDict[objectKey][0].keys() - next(iter(customExpect[0].values())).keys())
                    for diffKey in diffKeys:
                        for rDict in customResponseDict[objectKey]:
                            rDict.pop(diffKey)
                    # 由于传入的可选参数customExpect可能有多个值。但是我们默认可选传入一个参数。这样我们通过tuple[0]取到该传入的参数。然后遍历它，进行In的验证
                    for key,value in customExpect[0].items():
                        # pdb.set_trace()
                        if value not in customResponseDict[objectKey]:
                            assert False, "%s cann't find in the select result. " % str(key)
                # 根据yml判断是否需要进行 查询出来结果长度字段的校验。这里的校验是比较Response的对象的长度和Response中对应长度字段的值
                if ifItemInKeysAndValueNotNone("sizeInSelectResult", customCheckItems):
                    sizeKey = str(customCheckItems['sizeInSelectResult'])
                    if ifItemInKeysAndValueNotNone(sizeKey, customResponseDict):
                        assert len(customResponseDict[customCheckItems['keyInSelectResult']]) == int(customResponseDict[sizeKey]), \
                            "The size of %s is not match the value in the response. Expect is %s,actual is %s." \
                            % (str(customCheckItems['keyInSelectResult']), str(len(customResponseDict[objectKey])),
                               str(customResponseDict[sizeKey]))
                # 根据yml判断是否要对结果，进行 删除 项筛选。按照正常业务逻辑，被删除的对象是不应该展示在查询结果中
                if ifItemInKeysAndValueNotNone("checkIfDeleteItem", customCheckItems):
                    deleteKey = str(customCheckItems['checkIfDeleteItem'])
                    allIsDelete = []
                    # 遍历Response的所有对象的那个标识已删除的字段，所有值都应该是False
                    for iObject in customResponseDict[objectKey]:
                        if iObject[deleteKey]:
                            allIsDelete.append(iObject)
                    assert len(allIsDelete) == 0, "Please note that, there is object %s which is deleted in the result. That is not correct!" % str(allIsDelete)
            # 我们对于查询可以带include的参数。我们现在处理方式是，把所有的include的字段都带上。检查返回结果中，包含这些include的字段值即可，具体include的内容不做校验。
            # 对于分页查询的验证，暂时仅仅验证返回有该字段。后续对排序方式和页面设置进行加强验证
            elif ifItemInKeysAndValueNotNone("checkIncludeItem", customCheckItems):
                for item, value in customCheckItems['checkIncludeItem'].items():
                    if item == '/':
                        objectList = customResponseDict
                    else:
                        objectList = customResponseDict[item]
                    if len(objectList) > 0:
                        notIncludeList = []
                        if item == '/':
                            keySets = customResponseDict.keys()
                        else:
                            keySets = objectList[0].keys()
                        for iValue in str(value).split(','):
                            # pdb.set_trace()
                            if iValue not in keySets:
                                notIncludeList.append(iValue)
                        assert len(notIncludeList) == 0, "The include item didn't show in the result, please check the items: %s" % str(notIncludeList)
                    else:
                        assert False, "When we add the include parameter ,the Result is not correct!!!!"
            # 对于包含了上一页，下一页的验证。按照指定pageSize和pageIndex，进行比较期望的string，是否在结果的url中验证
            elif ifItemInKeysAndValueNotNone("pageSettings", customCheckItems):
                for item, value in customCheckItems['pageSettings'].items():
                    if ifItemInKeysAndValueNotNone(item, customResponseDict):
                        assert len(re.findall(str(value),str(customResponseDict[item]))) == 0, "The parameter %s  of item %s didn't show in the url %s, " \
                                                                                               "please check the response" % (str(value), str(item), str(customResponseDict[item]))
                    else:
                        assert False, "The item %s didn't show in the Response %s" % (str(value), str(customResponseDict))
            # 对于包含了排序字段和排序方式的验证。按照指定的排序字段，进行比较（通过 > 比较）
            elif ifItemInKeysAndValueNotNone("checkSortFunction", customCheckItems) and ifItemInKeysAndValueNotNone("checkSortObject", customCheckItems) and\
                    ifItemInKeysAndValueNotNone("checkSortType", customCheckItems):
                sortKey = str(customCheckItems['checkSortFunction'])
                sortObject = customResponseDict[str(customCheckItems['checkSortObject'])]
                if len(sortObject) >= 2:
                    if customCheckItems['checkSortType'] == 'desc':
                        assert sortObject[0][sortKey] >= sortObject[1][sortKey], "The sort result is not right, please check! Expect object order " \
                                                                                 "by %s %s, %s >= %s" % (str(sortKey), str(customCheckItems['checkSortType']),
                                                                                                         str(sortObject[0][sortKey]), str(sortObject[1][sortKey]))
                    elif customCheckItems['checkSortType'] == 'asc':
                        assert sortObject[0][sortKey] <= sortObject[1][sortKey], "The sort result is not right, please check! Expect object order " \
                                                                                 "by %s %s, %s <= %s" % (str(sortKey), str(customCheckItems['checkSortType']),
                                                                                                         str(sortObject[0][sortKey]), str(sortObject[1][sortKey]))
                    else:
                        assert False, "Please identify the sortType 'checkSortType' first in the expect yml file."
            else:
                pass

def AssertStringResponse(testResponse, expect):
    if ifItemInKeysAndValueNotNone('responsestate',expect):
        logger.info("-------------------Prepare to verify the response state code！-------------------")
        assert testResponse.status_code == expect[
            'responsestate'], "Response Code is not correct, expect code: %s, actual code: %s,content is %s" % (
            expect['responsestate'], testResponse.status_code, testResponse.content)
        logger.info("-------------------Passed ：verify the response state code-------------------")

    if testResponse.content.__len__() > 0:
        if ifItemInKeysAndValueNotNone('responseitemcheck', expect):
            response = json.loads(testResponse.content)
            expect_response = expect['responseitemcheck']
            assert str(response) == str(
                expect_response), "didn't match the expect value: %s ,actual value is: %s" % (
                expect_response, response)


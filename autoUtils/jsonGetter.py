# -*- coding: utf-8 -*-
"""
======================
@author:nash
@time:12/17/2021:3:18 PM
@email:nash.xiang@comm100.com
======================
"""

valueResult = []
result = []


def _get_target_value(dic):
    if not isinstance(dic, dict) :  # 对传入数据进行格式校验
        return 'argv[1] not an dict or argv[-1] not an list '
    for key,value in dic.items():  # 传入数据不符合则对其value值进行遍历
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
            _get_value(val_)   # 传入数据的value值是列表或者元组，则调用自身


def _get_test_value(val, tmp_list):
    for val_ in val:
        if isinstance(val_, dict):
            _get_target_value(val_, tmp_list)  # 传入数据的value值是字典，则调用get_target_value
        elif isinstance(val_, (list, tuple)):
            _get_value(val_, tmp_list)   # 传入数据的value值是列表或者元组，则调用自身


def getDictKeyValue(keyStr, udict):
    if not isinstance(udict, dict) :  # 对传入数据进行格式校验
        return 'argv[1] not an dict'
    for key in udict.keys():  # 传入数据不符合则对其value值进行遍历
        keyString = ''
        if not keyStr:
            keyString = key
        else:
            keyString = keyStr + '.' + key
        result.append(keyString)
        if isinstance(udict[key], dict):
            getDictKeyValue(keyString,udict[key])  # 传入数据的value值是字典，则直接调用自身
        elif isinstance(udict[key], (list, tuple)):
            for val_ in udict[key]:
                if isinstance(val_, dict):
                    getDictKeyValue(keyString,val_)  # 传入数据的value值是字典，则调用get_target_value
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
    keyList = getkeyListFunc('',initialDict)
    if not isinstance(keyList, list) :  # 对传入数据进行格式校验
        return 'argv[1] not a List'
    # 循环遍历字典的所有key，如果有子节点。就用.连接所有的几点。比如：bbb.c.c2
    for key in keyList:
        # 确保每次获取的字典都是一样的
        ardict = getDictFunc()
        # 对列表的每一项进行处理。已确定当前的节点，是否是dict或者是list，如果是dict就直接赋值。如果是list则需要拼装dict取值语句
        if str(key).count('.') > 0:
            k = 'ardict'
            evalk = ''
            for i in key.split('.'):
                # 拼接执行语句，eval调用可以返回执行的结果
                evalk = 'isinstance(' + k + "['" + i + "']" + ', dict)'
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
            k = k + ' = None'
            # 执行拼接的python语句。并不返回
            exec(k)
            # 将获取到的字典，加入到结果list中
            lResult.append(ardict)
        else:
            ardict[str(key)] = ''
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
#     #dict = {'name': '', 'chatbotIntentCategoryId': '3bfcf193-9939-4abd-a832-2625ea02e75b', 'chatbotIntentQuestions': [{'order': 0, 'content': 'Hello', 'chatbotIntentQuestionKeywords': [{'variableName': 'color', 'startPosition': 5, 'endPosition': 20, 'ifPrebuiltEntity': False, 'prebuiltEntityId': '00000000-0000-0000-0000-000000000000', 'entityId': 'd394618e-6c2a-444f-b4b3-5b88ed2466ad'}]}], 'chatbotIntentAnswers': [{'channelId': 'Live Chat', 'order': 0, 'collectInfoType': 'form', 'chatbotResponseId': 'ecd57b2b-2a7a-4059-8e63-ad5c8e291048', 'chatbotResponse': {'chatbotActions': [{'xPosition': 50, 'yPosition': 50, 'type': 'chatbotActionStart', 'chatbotActionSalesforceFindRecordBySoql': {'soql': '', 'failedActionId': 'f206705e-3651-4ce9-a902-d749d936502a', 'successedActionId': 'f206705e-3651-4ce9-a902-d749d936502a', 'chatbotActionSalesforceFindRecordFieldBySoqls': [{'fieldName': '', 'saveToVariable': ''}]}, 'chatbotActionTransferChat': {'transferTo': '87AD4BE9-89F5-4E57-AE9E-2D5FEE8ED3E5', 'whenAgentOfflineToActionId': '00000000-0000-0000-0000-000000000000', 'type': 'transferToAgent'}, 'chatbotActionSendMessage': {'nextActionId': '00000000-0000-0000-0000-000000000000', 'variants': [''], 'message': "Hi there! I'm a chatbot, here to help answer your questions.", 'typingDelay': 0.0, 'chatbotActionSendMessageLinks': [{'buttonText': 'twitter', 'type': 'webview', 'openIn': 'sideWindow', 'intentId': '00000000-0000-0000-0000-000000000000', 'url': 'https://www.baidu.com', 'openStyle': 'compact', 'order': 0}]}, 'chatbotActionCollectPhoneNumber': {'nextActionId': 'AA310D7E-24AB-422E-8976-B83336700527', 'isInputAreaEnabled': True, 'message': "What's your phone number?", 'typingDelay': 1.0}, 'chatbotActionSalesforceCreateRecord': {'saveRecordIdToVariable': '', 'nextActionId': 'f206705e-3651-4ce9-a902-d749d936502a', 'ifUpdateDuplicatedRecord': True, 'object': '', 'chatbotActionSalesforceCreateRecordFields': [{'fieldValue': '', 'fieldName': ''}]}, 'chatbotActionCollectName': {'isInputAreaEnabled': True, 'typingDelay': 1.0, 'message': "What's your name?", 'nextActionId': '00000000-0000-0000-0000-000000000000'}, 'chatbotActionWebhook': {'ifSendChatTranscript': False, 'url': 'www.baidu.com', 'otherResponseToActionId': '00000000-0000-0000-0000-000000000000', 'additionalPostBody': '', 'chatbotActionWebhookResponseToVariables': [{'order': 0, 'responseKey': 'fdafa', 'variableName': '2342432432132131'}], 'chatbotActionWebhookHeaders': [{'value': 'v1', 'order': 0, 'key': 'k1'}], 'chatbotActionWebhookResponseCodeToActions': [{'responseCode': '200', 'nextActionId': '00000000-0000-0000-0000-000000000000', 'order': 0}]}, 'chatbotActionGoToTaskbot': {'taskbotId': 'F198799B-F8DE-40B4-94A9-004848BE0918'}, 'chatbotActionSendCannedQuickReply': {'cannedQuickReplyId': 'D62DE3F6-A55E-4AB2-9DA3-2AF33849306D', 'message': '', 'isInputAreaEnabled': True, 'anyOtherResponseActionId': '00000000-0000-0000-0000-000000000000', 'typingDelay': 0.0}, 'chatbotActionSendImage': {'message': '', 'typingDelay': 0.0, 'nextActionId': 'CC5AF23C-CCA4-4D2D-B25A-4BF891275F30', 'image': ''}, 'chatbotActionGoToIntent': {'intentId': '4C36FC4D-9CEC-4AB4-9F00-8D8B20EA47A8'}, 'chatbotActionSSOLoginButton': {'typingDelay': 0.0, 'isInputAreaEnabled': True, 'successedActionId': '03DF237A-7F5F-45A8-A44C-042CD9D85E0C', 'message': 'signin message sso', 'failedActionId': '00000000-0000-0000-0000-000000000000', 'loginButtonText': 'signin-text sso'}, 'chatbotActionLeaveChat': {}, 'chatbotActionSendVideo': {'typingDelay': 0.0, 'message': '', 'nextActionId': '00000000-0000-0000-0000-000000000000', 'videoUrl': 'https://www.youtube.com/watch?v=0XYWpraTgaY'}, 'chatbotActionCollectEmail': {'message': "What's your email?", 'typingDelay': 1.0, 'isInputAreaEnabled': False, 'nextActionId': '478EE923-458A-4EAA-A698-98DDB64DCF19'}, 'chatbotActionCondition': {'otherCaseActionId': '00000000-0000-0000-0000-000000000000', 'chatbotActionConditionCases': [{'order': 0, 'logicalExpression': '', 'goToActionId': '00000000-0000-0000-0000-000000000000', 'conditionExpressionType': 'all', 'chatbotActionConditionCaseConditions': [{'order': 0, 'operator': 'is', 'value': 'fdsfsdaf', 'fieldName': '{!Variable.Name}'}]}]}, 'chatbotActionBookMeeting': {'failedActionId': '00000000-0000-0000-0000-000000000000', 'calendlyEventTypeUri': 'http://localhost/event_types/15', 'successedActionId': '00000000-0000-0000-0000-000000000000', 'integrationCalendlyId': '7E8DFDA2-2117-4796-93D0-8A51047CE1BC'}, 'chatbotActionSendForm': {'title': 'Via a Form title', 'message': 'Via a Form', 'successedActionId': '32A2B481-DC43-47B4-9B12-60E128347B16', 'isConfirmationRequired': False, 'submitButtonText': 'Text on the Submit Button in the Form: Submit', 'isInputAreaEnabled': True, 'confirmButtonText': 'Text on the Confirm Button in the Form: Confirm', 'typingDelay': 0.0, 'cancelButtonText': 'Text on the Cancel Button in the Form: Cancel', 'failedActionId': '00000000-0000-0000-0000-000000000000', 'chatbotActionSendFormFields': [{'options': [''], 'type': 'text', 'entityId': '00000000-0000-0000-0000-000000000000', 'variableName': '', 'ifPrebuiltEntity': True, 'isMasked': True, 'isRequired': True, 'name': 'test', 'order': 0, 'prebuiltEntityId': '00000000-0000-0000-0000-000000000000'}]}, 'chatbotActionSendNumericMenu': {'isInputAreaEnabled': True, 'otherResponseToActionId': '00000000-0000-0000-0000-000000000000', 'message': 'hello', 'chatbotActionSendNumericMenuOptions': [{'nextActionId': 'C8A26362-6823-4497-89B3-B54B06B2379A', 'key': '3', 'order': 0, 'text': 'test'}]}, 'chatbotActionCollectVariableData': {'typingDelay': 1.0, 'nextActionId': '18DAA6C1-7468-471D-BB30-E7AE0BE09FFC', 'variableName': 'text', 'options': [], 'isInputAreaEnabled': False, 'message': 'text', 'type': 'text'}, 'chatbotActionSetVariableValue': {'fieldId': '00000000-0000-0000-0000-000000000000', 'value': '1111', 'customVariableId': '6B2D7C50-300B-4708-B913-086BE822F368', 'nextActionId': '6F7ED3FD-5C77-4512-AA8B-F5F452575656', 'ticketingFieldId': '110499d0-5a3e-469f-b8de-9a34e99092b0', 'saveToType': 'customVariable'}, 'chatbotActionSendEmail': {'to': 'Simon', 'subject': 'API Test', 'cc': 'jansemain', 'content': 'Delete', 'nextActionId': '60F2F597-5674-41D8-BBFD-0AEAAF787837'}, 'chatbotActionCollectComment': {'typingDelay': 1.0, 'nextActionId': '00000000-0000-0000-0000-000000000000', 'isInputAreaEnabled': False, 'message': "What's your comment?"}, 'chatbotActionChangeAssignee': {'whenAgentOfflineToActionId': '00000000-0000-0000-0000-000000000000', 'type': 'transferToAgent', 'transferTo': '6CC96F38-5FE2-448C-AFBB-3F3D109CF022'}, 'chatbotActionCollectCompanyName': {'isInputAreaEnabled': False, 'typingDelay': 1.0, 'message': "What's your company name?", 'nextActionId': '478EE923-458A-4EAA-A698-98DDB64DCF19'}, 'chatbotActionStart': {'nextActionId': 'ea5369ae-b5cf-4bfa-a5fa-9dac234cf4c5'}, 'chatbotActionCollectLocation': {'buttonText': 'Text on the Send Location Button: Send Location', 'isInputAreaEnabled': True, 'message': "What's your email?", 'typingDelay': 1.0, 'successedActionId': 'D4247757-441E-44E7-AA0A-8197FE123B28', 'failedActionId': '00000000-0000-0000-0000-000000000000'}, 'chatbotActionSalesforceFindRecord': {'fieldToSearchBy': '', 'object': '', 'failedActionId': 'f206705e-3651-4ce9-a902-d749d936502a', 'searchValue': '', 'successedActionId': 'f206705e-3651-4ce9-a902-d749d936502a', 'chatbotActionSalesforceFindRecordFields': [{'saveToVariable': '', 'fieldName': ''}]}, 'chatbotActionContactAgent': {'message': "I'm sorry, I haven't been trained to answer that question yet! Try asking me a different question, or use the button below to connect with a live agent.", 'optionTextWhenAgentOffline': 'Chat with Live Agent', 'optionTextWhenAgentOnline': 'Chat with Live Agent', 'typingDelay': 0.0}, 'chatbotActionQuickReply': {'typingDelay': 0.0, 'otherResponseToActionId': '00000000-0000-0000-0000-000000000000', 'isInputAreaEnabled': True, 'message': 'custom qp-have message', 'chatbotActionQuickReplyOptions': [{'order': 0, 'nextActionId': '177C7AE7-B792-420C-82D3-563564B8647D', 'text': 'goto taskbot '}]}}]}}], 'chatbotIntentPrompts': [{'question': 'which type', 'options': ['ham', 'hawayi', 'pepperoni|{!CustomVariable.aaa}'], 'entityId': '00000000-0000-0000-0000-000000000000', 'prebuiltEntityId': '00000000-0000-0000-0000-000000000000', 'mappingFieldName': '', 'variableName': 'pizza_type', 'ifPrebuiltEntity': True, 'order': 0}]}
#     #json_str = json.dumps(dict)
#     #print(repr(dict))
#     #print(json_str)
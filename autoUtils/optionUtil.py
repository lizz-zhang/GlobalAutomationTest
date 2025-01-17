# -*- coding: utf-8 -*-
"""
======================
@author:nash
@time:2/21/2022:2:58 PM
@email:nash.xiang@comm100.com
======================
"""
import json
import logging
import pdb
import re
import uuid
import random
from autoUtils.manage_global_data import ManageGlobalData
from autoUtils.fileReader import read_config_file
from autoUtils.requestFactory import test_api_request
import os
import requests


logger = logging.getLogger(__name__)


def searchAndChangeDict(inputDict, finalString):
    # 用inputDict里的值替换掉finalString里的变量
    '''
    :param inputDict: 可以赋值的字典。从此字典给带有变量的字典重改值
    :param finalString: 带有变量的string，需要从可赋值的字典中获取值
    :return: 给inputDict修改完值的Dict
    Note：此方法现在仅支持第一层级的变量更改，不支持嵌套多层的dict的value值更改。存在一定的局限性
    目前满足日常工作需求，后续需要再进行扩展支持。
    '''
    if re.search(r"\$.*\$", finalString):
        pathList = finalString.split("$")
        num = int(len(re.findall(r"\$", finalString)) / 2)
        for i in range(0, num):
            listNum = 2 * i + 1
            item = str(pathList[listNum])
            try:
                finalString = finalString.replace(("$" + item + "$"), str(inputDict[item]))
            except:
                logger.info("The Input Dict didn't have the key which in the string!")

    return finalString


def ifItemInKeysAndValueNotNone(key, inputDict):
    if isinstance(inputDict, dict):
        if key in inputDict:
            if not (isinstance(inputDict[key], type(None))):
                return True
            else:
                return False
        else:
            return False
    else:
        return False


def combineUUIDAndNextActionId(finalString):
    if re.search(r"\$.*\$", finalString):
        pathList = finalString.split("$")
        num = int(len(re.findall(r"\$", finalString)) / 2)
        idDict = {}
        for i in range(0, num):
            listNum = 2 * i + 1
            item = str(pathList[listNum])
            try:
                newGuid = str(uuid.uuid1())
                finalString = finalString.replace(("$" + item + "$"), newGuid)
                idDict[item] = newGuid
            except:
                logger.info("The Input Dict didn't have the key which in the string!")
        finalString = searchAndChangeDict(idDict, finalString)
    return finalString

#替换json里的变量为随机字符串，支持任意层结构的替换
def change_to_random_string(input_dict):
    # pdb.set_trace()
    string = 'abcdef0123456789'
    for item in input_dict:
        if isinstance(input_dict[item], str):
            input_dict[item] = str(input_dict[item]).replace('$random$', ''.join(random.sample(string, 7))).replace('$random2$', ''.join(random.sample(string, 7)))
        elif isinstance(input_dict[item], list):
            for i in range(len(input_dict[item])):
                if isinstance(input_dict[item][i], dict):
                    for j in input_dict[item][i]:
                        change_to_random_string(input_dict[item][i])
    return input_dict
#替换json里的变量为随机数字字符串，支持任意层结构的替换
def change_to_random_int(input_dict):
    # pdb.set_trace()
    string = '123456789'
    for item in input_dict:
        if isinstance(input_dict[item], str):
            input_dict[item] = str(input_dict[item]).replace('$randomInt$', ''.join(random.sample(string, 7))).replace('$random2$', ''.join(random.sample(string, 7)))
        elif isinstance(input_dict[item], list):
            for i in range(len(input_dict[item])):
                if isinstance(input_dict[item][i], dict):
                    for j in input_dict[item][i]:
                        change_to_random_int(input_dict[item][i])
    return input_dict

#替换dict里的变量为实际值
def replace_dict_value(input_dict, param, value):
    if isinstance(input_dict, dict):
        for item in input_dict:
            if isinstance(input_dict[item], str):
                input_dict[item] = str(input_dict[item]).replace(param, str(value))
            elif isinstance(input_dict[item], dict):
                replace_dict_value(input_dict[item], param, str(value))
            elif isinstance(input_dict[item], list):
                for i in range(len(input_dict[item])):
                    input_dict[item][i] = str(input_dict[item][i]).replace(param, str(value))
        return  input_dict

# 替换dict里的变量为实际值，支持多个变量替换。在replacements中传入dict，key为变量，value为实际值
def replace_dict_value_multi(input_dict, replacements_dict):
    if isinstance(input_dict, dict):
        for item in input_dict:
            if isinstance(input_dict[item], str):
                for param, value in replacements_dict.items():
                    input_dict[item] = input_dict[item].replace(param, str(value))
            elif isinstance(input_dict[item], dict):
                replace_dict_value_multi(input_dict[item], replacements_dict)
            elif isinstance(input_dict[item], list):
                for i in range(len(input_dict[item])):
                    if isinstance(input_dict[item][i], dict):
                        replace_dict_value_multi(input_dict[item][i], replacements_dict)
                    elif isinstance(input_dict[item][i], str):
                        for param, value in replacements_dict.items():
                            input_dict[item][i] = input_dict[item][i].replace(
                                param, str(value)
                            )
        return input_dict

def upload_file(token_path_name, file_name, partner_or_platform):
    env = str(ManageGlobalData().get_global_value())
    partner_id = ManageGlobalData().get_partner_id()
    site_id = ManageGlobalData().get_site_id()
    config_data_json_dict = read_config_file('environments.json')
    partner_path = config_data_json_dict[env]['partner']
    dash_path = config_data_json_dict[env]['dash']
    partner_file_token_path = config_data_json_dict[env][token_path_name]
    if partner_or_platform == 'partner':
        domain = partner_path
    else:
        domain = dash_path
    token_url = domain + partner_file_token_path.replace('$partnerId$', str(partner_id)).replace('$siteId$', str(site_id))
    token_response =  test_api_request(token_url, 'GET', None, None)
    file_key = ''
    if token_response.status_code == 200:
        header = {'Authorization': 'Bearer ' + str(token_response.content.decode())}
        file_service_path = config_data_json_dict[env]['partnerFileService']
        test_file_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__))) + '//autoConfig//' + file_name
        files = {'file': open(test_file_path, 'rb')}
        file_key_response = requests.post(file_service_path, files=files,headers=header)
        if file_key_response.status_code == 200:
            file_key = str(file_key_response.content.decode())
        else:
            logger.error('get file key error')
    else:
        logger.error('get file service token error')
    return file_key

def find_value_by_key(input_arr, keyword):
    if isinstance(input_arr, list):
        for item in input_arr:
            result = find_value_by_key(item, keyword)
            if result is not None:
                return result
    elif isinstance(input_arr, dict):
        if keyword in input_arr:
            return input_arr[keyword]
        for value in input_arr.values():
            result = find_value_by_key(value, keyword)
            if result is not None:
                return result
    return None

def get_public_canned_message_rootcategory(login_info):
    config_data_json_dict = read_config_file('environments.json')
    environment = str(ManageGlobalData().get_global_value())
    dash_url = config_data_json_dict[environment]['dash']
    public_canned_message_url = dash_url + config_data_json_dict[environment]['publicCannedMessageCategoryPath']
    get_response = test_api_request(public_canned_message_url, 'GET', login_info['commonHeader'], None)
    get_response_content = json.loads(get_response.content)
    root_category_id = get_response_content[0]['id']
    return  root_category_id

if __name__ == '__main__':
    #print(len(re.findall("at", "a1tt")))
    testDict = {"test": "testin", "test1": {"n1":1, "n2":2 },"test2": [{"t1":"t1"}]}
    testDict1 = {"test": "testin", "test1": {"n1":1, "n2":2 },"test2": [{"t1":"t1"}]}
    path = 'E://share//NewBotAutomation//autoConfig//botdata.json'
    with open(path,mode='r') as f:
          config_data_json_dict = json.load(f)
    #print(config_data_json_dict['intent']['t_body'])
    categoryIdDict = {'chatbotIntentCategoryId': '00000000-8888-9999-111111111111'}
    # print(eval(combineUUIDAndNextActionId(searchAndChangeDict(categoryIdDict, str(config_data_json_dict['intent']['c_body'])))))
    # print(searchAndChangeDict(testDict1,str(testDict)))
    #print(random.sample('zyxwvutsrqponmlkjihgfedcba', 5))
    #print(string)

# 替换test data里面的更新数据到默认的结构体里面,这样在准备request body的时候,就可以不用关注那些没有修改的数据
def replace_request_body_data_with_test_data(origin_data, changed_data):
    """
    Replace values in origin_data with corresponding values from changed_data.

    Args:
        origin_data (dict): The original data to be modified.
        changed_data (dict): The data with replacement values.

    Returns:
        dict: The modified origin_data.
    """
    for key, value in changed_data.items():
        if key in origin_data:
            if isinstance(value, dict) and isinstance(origin_data[key], dict):
                origin_data[key] = replace_request_body_data_with_test_data(
                    origin_data[key], value
                )
            elif isinstance(value, list) and isinstance(origin_data[key], list):
                for i in range(min(len(value), len(origin_data[key]))):
                    if isinstance(value[i], dict) and isinstance(
                        origin_data[key][i], dict
                    ):
                        origin_data[key][i] = replace_request_body_data_with_test_data(
                            origin_data[key][i], value[i]
                        )
                    else:
                        origin_data[key][i] = value[i]
            else:
                origin_data[key] = value
    return origin_data

def ifItemInKeysAndValueNotNone(key, inputDict):
    if key in inputDict:
        if not (isinstance(inputDict[key], type(None))):
            return True
        else:
            return False
    else:
        return False


def combineUUIDAndNextActionId(finalString):
    if re.search(r"\$.*\$", finalString):
        pathList = finalString.split("$")
        num = int(len(re.findall(r"\$", finalString)) / 2)
        idDict = {}
        for i in range(0, num):
            listNum = 2 * i + 1
            item = str(pathList[listNum])
            try:
                newGuid = str(uuid.uuid1())
                finalString = finalString.replace(("$" + item + "$"), newGuid)
                idDict[item] = newGuid
            except:
                logger.info("The Input Dict didn't have the key which in the string!")
        finalString = searchAndChangeDict(idDict, finalString)
    return finalString


def generate_small_ip():
    return ".".join(str(random.randint(0, 127)) for i in range(4))


def generate_big_ip():
    return ".".join(str(random.randint(128, 255)) for i in range(4))

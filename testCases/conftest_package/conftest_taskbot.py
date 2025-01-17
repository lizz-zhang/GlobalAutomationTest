# -*- coding: utf-8 -*-
"""
======================
@author:nash
@time:12/30/2024:11:00 AM
@email:nash.xiang@comm100.com
======================
"""
import json
import logging
import os
import pdb
import random
import sys
import pytest

from autoUtils.assertFactory import logger
from autoUtils.fileReader import read_config_file
from autoUtils.optionUtil import combine_uuid_to_next, generate_autotest_object_name, search_change_dict
from autoUtils.requestFactory import test_api_request


logger = logging.getLogger(__name__)
base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(base_dir)


def create_taskbot(login_info, config_data_json_dict, body):
    method = config_data_json_dict['taskbot']['createMethod']
    url = login_info['dashUrl'] + config_data_json_dict['taskbot']['createPath']
    # 修改新建taskbot的名字，让每个用例Bot创建都能成功
    new_name = generate_autotest_object_name("taskbot_conftest_")
    body['name'] = new_name
    return test_api_request(url, method, login_info['commonHeader'], body)

def create_taskbot_version(login_info, config_data_json_dict, taskbot):
    create_method = config_data_json_dict['taskbot']['createMethod']
    create_version_url = (
        login_info['dashUrl'] + 
        str(config_data_json_dict['taskbot']['createVersionPath'])
    )
    create_body = search_change_dict(
        taskbot,
        str(config_data_json_dict['taskbot']['taskbotVersionBody'])
    )
    create_body = combine_uuid_to_next(create_body)
    taskbot_version_response = test_api_request(
        create_version_url, 
        create_method, 
        login_info['commonHeader'],
        eval(create_body)
    )
    return taskbot_version_response

def update_taskbot(login_info, config_data_json_dict, taskbot):
    update_method = config_data_json_dict['taskbot']['updateMethod']
    update_path = config_data_json_dict['taskbot']['updatePath']
    update_taskbot_url = (
        login_info['dashUrl'] + 
        search_change_dict(taskbot,str(update_path))
    )
    # taskbot修改的时候，参数与create taskbot时候的response一样。只需要更改latestVersionId的值
    taskbot_update_response = test_api_request(
        update_taskbot_url, 
        update_method, 
        login_info['commonHeader'],
        taskbot
    )
    return taskbot_update_response


def delete_taskbot_by_id(login_info, config_data_json_dict, taskbot_id):
    method = config_data_json_dict['taskbot']['deleteMethod']
    del_path = str(config_data_json_dict['taskbot']['deletePath']).replace('$id$', str(taskbot_id))
    del_url = login_info['dashUrl'] + del_path
    del_repsonse = test_api_request(
        del_url, 
        method, 
        login_info['commonHeader'], 
        None
    )
    return del_repsonse


@pytest.fixture(scope='session')
def cleanup_taskbots(login):
    config_data_json_dict = read_config_file('taskbotdata.json')
    method = config_data_json_dict['taskbot']['getMethod']
    login_info= login
    get_url = login_info['dashUrl'] + str(config_data_json_dict['taskbot']['getPath'])
    yield 
    taskbots_response = test_api_request(
        get_url, 
        method, 
        login_info['commonHeader'],
        None
    )
    if taskbots_response.status_code < 300:
        # 这里拿taskbots请求没有带include参数，返回就是一个taskbot的列表
        taskbots = json.loads(taskbots_response.content)
        for taskbot in taskbots:
            if ("taskbot_auto_" in str(taskbot['name']) or 
                "taskbot_conftest_" in str(taskbot['name'])):
                del_response = delete_taskbot_by_id(
                    login_info, 
                    config_data_json_dict, 
                    taskbot['id']
                )
                if del_response.status_code > 300:
                    logger.info("-----Clean up taskbot failed, please clean it by manual-----")
                else:
                    logger.info("-----Clean up taskbot successfully-----")
            else:
                logger.info("-----NO record found, no need to clean up-----")
    else:
        logger.info("-----Clean up taskbot failed, please clean it by manual-----")

@pytest.fixture(scope='class')
def prepare_taskbot(login):
    '''
    创建taskbot分为3个步骤：
    第一步先创建一个taksbot
    第二步给taskbot创建一个taskbotversion
    第三部修改taskbot以第二步中的taskbotversion
    '''
    login_info = login
    
    config_data_json_dict = read_config_file('taskbotdata.json')
    #创建taskbot
    create_taskbot_response = create_taskbot(
        login_info, 
        config_data_json_dict, 
        config_data_json_dict['taskbot']['taskbotBody']
    )
    if create_taskbot_response.status_code < 300:
        taskbot = json.loads(create_taskbot_response.content)
        #创建taskbotversion
        response = create_taskbot_version(login_info,config_data_json_dict,taskbot)
        taskbot_version_dict = {}
        if response.status_code < 300:
            version_response_dict = json.loads(response.content)
            # 更新taskbot 的latestVersionId
            taskbot['latestVersionId'] = version_response_dict['id']
            # 修改taskbot
            update_respones = update_taskbot(
                login_info, 
                config_data_json_dict,
                taskbot
            )
            if update_respones.status_code > 300:
                logger.info(f"!!!!!Please note that, didn't update TaskBot latestVersionId success, "
                            f"it will impact next test case. Please check!!!!!")
            else:
                update_response_dict = json.loads(update_respones.content)
                taskbot_version_dict['taskbot'] = update_response_dict
                taskbot_version_dict['taskbotversion'] = version_response_dict
    yield taskbot_version_dict
    if not isinstance(taskbot_version_dict, type(None)):
        delete_response = delete_taskbot_by_id(
            login_info,
            config_data_json_dict, 
            taskbot_version_dict['taskbot']['id']
        )
        if delete_response.status_code >= 300:
            logger.info(f"!!!!!Please note that, didn't remove Taskbot bot {taskbot_version_dict['taskbot']['id']} success, "
                        f"it will impact next test case. Please check!!!!!")
            logger.info(delete_response.content)
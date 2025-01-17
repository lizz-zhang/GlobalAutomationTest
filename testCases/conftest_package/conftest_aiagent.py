# -*- coding: utf-8 -*-
"""
======================
@author:nash
@time:1/7/2024:11:00 AM
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


def create_aiagent(login_info, config_data_json_dict):
    method = config_data_json_dict['aiagent']['createMethod']
    url = login_info['dashUrl'] + config_data_json_dict['aiagent']['createAiAgentPath']
    new_name = generate_autotest_object_name("aiagent_conftest_")
    body =config_data_json_dict['aiagentBody']
    body['name'] = new_name
    c_response = test_api_request(
        url, 
        method, 
        login_info['commonHeader'],
        body
    )
    return c_response

def create_assistant(login_info, config_data_json_dict):
    method = config_data_json_dict['aiagent']['createMethod']
    path = config_data_json_dict['aiagent']['createAssistantPath']
    url = login_info['dashUrl'] + search_change_dict(login_info['userData'], path)
    new_name = generate_autotest_object_name("assistant_conftest_")
    body =config_data_json_dict['assistantBody']
    body['name'] = new_name
    c_response = test_api_request(
        url, 
        method, 
        login_info['commonHeader'],
        body
    )
    return c_response

def create_aiagent_function(login_info, config_data_json_dict, aiagent):
    method = config_data_json_dict['aiagent']['createMethod']
    url = login_info['dashUrl'] + config_data_json_dict['aiagent']['createFunctionPath']
    new_name = generate_autotest_object_name("aiagent_function_conftest_")
    body = config_data_json_dict['functionBody']
    body['name'] = new_name
    body['aiAgentId'] = aiagent['id']
    c_response = test_api_request(
        url, 
        method, 
        login_info['commonHeader'],
        eval(combine_uuid_to_next(str(body)))
    )
    return c_response

def get_aiagent_function_by_name(login_info, config_data_json_dict, aiagent, keywords):
    aiagent_function= None
    method = config_data_json_dict['aiagent']['getMethod']
    list_path = str(config_data_json_dict['aiagent']['listFunctionPath'])
    list_path = search_change_dict(
        aiagent,
        search_change_dict(
            login_info['userData'],
            list_path
        )
    )
    list_path = list_path.replace('$keywords$', str(keywords))
    list_url = login_info['dashUrl'] + list_path
    list_response = test_api_request(
        list_url, 
        method, 
        login_info['commonHeader'], 
        None
    )
    if list_response.status_code < 300:
        aiagent_function = json.loads(list_response.content())
    return aiagent_function

def delete_aiagent_function_by_id(login_info, config_data_json_dict, function_id):
    method = config_data_json_dict['aiagent']['deleteMethod']
    del_path = str(config_data_json_dict['aiagent']['deleteFunctionPath']).replace('$id$', str(function_id))
    del_url = login_info['dashUrl'] + del_path
    del_repsonse = test_api_request(
        del_url, 
        method, 
        login_info['commonHeader'], 
        None
    )
    return del_repsonse

def delete_aiagent_by_id(login_info, config_data_json_dict, aiagent_id):
    method = config_data_json_dict['aiagent']['deleteMethod']
    del_path = str(config_data_json_dict['aiagent']['deleteAiAgentPath']).replace('$id$', str(aiagent_id))
    del_url = login_info['dashUrl'] + del_path
    del_repsonse = test_api_request(
        del_url, 
        method, 
        login_info['commonHeader'], 
        None
    )
    return del_repsonse

def delete_assistant_by_id(login_info, config_data_json_dict, assistant_id):
    method = config_data_json_dict['aiagent']['deleteMethod']
    del_path = str(config_data_json_dict['aiagent']['deleteAiAgentPath']).replace('$id$', str(assistant_id))
    del_url = login_info['dashUrl'] + search_change_dict(login_info['userData'], del_path)
    del_repsonse = test_api_request(
        del_url, 
        method, 
        login_info['commonHeader'], 
        None
    )
    return del_repsonse

@pytest.fixture(scope='session')
def cleanup_aiagents(login):
    config_data_json_dict = read_config_file('aiagentdata.json')
    method = config_data_json_dict['aiagent']['getMethod']
    login_info= login
    get_url = login_info['dashUrl'] + str(config_data_json_dict['aiagent']['getAiAgentListPath'])
    yield 
    aiagents_response = test_api_request(
        get_url, 
        method, 
        login_info['commonHeader'],
        None
    )
    if aiagents_response.status_code < 300:
        aiagents = json.loads(aiagents_response.content)
        for aiagent in aiagents:
            if ("aiagent_auto_" in str(aiagent['name']) or 
                "aiagent_conftest_" in str(aiagents['name'])):
                del_response = delete_aiagent_by_id(
                    login_info, 
                    config_data_json_dict, 
                    aiagent['id']
                )
                if del_response.status_code > 300:
                    logger.info("-----Clean up aiagent failed, please clean it by manual-----")
                else:
                    logger.info("-----Clean up aiagent successfully-----")
            else:
                logger.info("-----NO record found, no need to clean up-----")
    else:
        logger.info("-----Clean up aiagent failed, please clean it by manual-----")

@pytest.fixture(scope='class')
def prepare_aigent(login):
    login_info = login
    config_data_json_dict = read_config_file('aiagentdata.json')
    aiagent = None
    create_aiagent_response = create_aiagent(
        login_info, 
        config_data_json_dict
    )
    if create_aiagent_response.status_code < 300:
        aiagent = json.loads(create_aiagent_response.content)
    yield aiagent
    if not isinstance(aiagent, type(None)):
        delete_response = delete_aiagent_by_id(
            login_info,
            config_data_json_dict, 
            aiagent['id']
        )
        if delete_response.status_code >= 300:
            logger.info(f"!!!!!Please note that, didn't remove aiagent {aiagent['id']} success, "
                        f"it will impact next test case. Please check!!!!!")
            logger.info(delete_response.content)

@pytest.fixture(scope='class')
def prepare_assistant(login):
    login_info = login
    config_data_json_dict = read_config_file('aiagentdata.json')
    assistant = None
    create_assistant_response = create_assistant(
        login_info, 
        config_data_json_dict
    )
    if create_assistant_response.status_code < 300:
        assistant = json.loads(create_assistant_response.content)
    yield assistant
    if not isinstance(assistant, type(None)):
        delete_response = delete_assistant_by_id(
            login_info,
            config_data_json_dict, 
            assistant['id']
        )
        if delete_response.status_code >= 300:
            logger.info(f"!!!!!Please note that, didn't remove aiagent {assistant['id']} success, "
                        f"it will impact next test case. Please check!!!!!")
            logger.info(delete_response.content)            

@pytest.fixture(scope='class')
def prepare_aigent_function(login, prepare_aigent):
    aiagent_function = None
    login_info = login
    config_data_json_dict = read_config_file('aiagentdata.json')
    aiagent_function_list = get_aiagent_function_by_name(
        login_info, 
        config_data_json_dict, 
        prepare_aigent, 
        "aiagent_function_conftest_"
    )
    if not isinstance(aiagent_function_list, type(None)) and len(aiagent_function_list) > 0:
       aiagent_function = aiagent_function_list[0]
    else:
        create_response = create_aiagent_function(
            login_info, 
            config_data_json_dict,
            prepare_aigent
        )
        if create_response.status_code < 300:
            aiagent_function = get_aiagent_function_by_name(
                login_info, 
                config_data_json_dict, 
                prepare_aigent, 
                "aiagent_function_conftest_"
            )
    yield aiagent_function
    if not isinstance(aiagent_function, type(None)):
        delete_response = delete_aiagent_function_by_id(
            login_info,
            config_data_json_dict, 
            aiagent_function['id']
        )
        if delete_response.status_code >= 300:
            logger.info(f"!!!!!Please note that, didn't remove aiagent {aiagent_function['id']} success, "
                        f"it will impact next test case. Please check!!!!!")
            logger.info(delete_response.content)

@pytest.fixture(scope='class')
def prepare_aigent_function_list(login, prepare_aigent):
    login_info = login
    config_data_json_dict = read_config_file('aiagentdata.json')
    aiagent_function_list = get_aiagent_function_by_name(
        login_info, 
        config_data_json_dict, 
        prepare_aigent, 
        "aiagent_function_conftest_"
    )
    yield aiagent_function_list
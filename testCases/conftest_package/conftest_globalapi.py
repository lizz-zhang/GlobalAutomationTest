# -*- coding: utf-8 -*-
from datetime import timedelta
import json
import os
import pdb
import re
import sys
import time
from socket import socket
from time import sleep
import uuid
import pytest
import logging

import requests.auth
from filelock import FileLock
from autoUtils.datetime_util import get_next_weekday
from datetime import datetime, timedelta

from autoUtils.fileReader import read_config_file, get_webdriver_file_with_extension
from autoUtils.requestFactory import send_request
from autoUtils.optionUtil import (
    replace_dict_value_multi,
    searchAndChangeDict,
    ifItemInKeysAndValueNotNone,
)
from faker import Faker

logging.basicConfig(
    format="%(asctime)s %(levelname)-8s %(message)s",
    level=logging.INFO,
    datefmt="%Y-%m-%d %H:%M:%S",
)
logger = logging.getLogger(__name__)
base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(base_dir)

fake = Faker()


@pytest.fixture(scope="function")
def enable_department_config(login):
    login_data = login

    # enable department config
    request_url_enable = login_data["api_url"] + "/global/departmentConfig:enable"
    res_enable = send_request(
        request_url_enable,
        None,
        "POST",
        None,
        login_data["common_headers"],
        None,
    )
    # pdb.set_trace()
    assert res_enable.status_code == 200, (
        "Failed with status code: "
        + str(res_enable.status_code)
        + " and response: "
        + str(res_enable.json())
    )
    logger.info("\n ======= Department Config enabled. =======")
    yield res_enable

    # teardown: disable department config
    request_url_disable = login_data["api_url"] + "/global/departmentConfig:disable"
    res_disable = send_request(
        request_url_disable,
        None,
        "POST",
        None,
        login_data["common_headers"],
        None,
    )
    # pdb.set_trace()
    assert res_disable.status_code == 200, (
        "Failed with status code: "
        + str(res_disable.status_code)
        + " and response: "
        + str(res_disable.json())
    )

    logger.info("\n ======= Department Config disabled. =======")


@pytest.fixture(scope="function")
def create_department(login):
    login_data = login
    agent_id = login_data["agent_id"]

    # add a new department and assign agent1 to it
    request_url_create = login_data["api_url"] + "/global/departments"
    request_body = {
        "name": "1st temp department",
        "description": "",
        "agentIds": [agent_id],
        "isAvailableInLiveChat": True,
        "isAvailableInTicketingAndMessaging": True,
        "isAvailableInVoice": True,
        "offlineMessageMailTo": "toAllAgents",
        "offlineMessageEmailAddresses": "",
    }

    res_create = send_request(
        request_url_create,
        None,
        "POST",
        None,
        login_data["common_headers"],
        request_body,
    )
    # pdb.set_trace()
    assert res_create.status_code == 201, (
        "Failed with status code: "
        + str(res_create.status_code)
        + " and response: "
        + str(res_create.json())
    )
    logger.info(
        "\n ======= a new department has been created and agent1 is added to it. ======="
    )
    yield res_create

    # teardown: delete the newly-created department
    created_id = res_create.json()["id"]
    request_url_delete = login_data["api_url"] + "/global/departments/" + created_id
    res_delete = send_request(
        request_url_delete, None, "DELETE", None, login_data["common_headers"], None
    )
    # pdb.set_trace()
    assert res_delete.status_code == 204, (
        "Failed with status code: "
        + str(res_delete.status_code)
        + " and response: "
        + str(res_delete.json())
    )

    logger.info("\n ======= newly-created department has been deleted. =======")


@pytest.fixture(scope="function")
def create_2nd_department(login):
    login_data = login
    agent2_id = login_data["agent2_id"]

    # add 2nd department and add agent2 to it
    request_url_create = login_data["api_url"] + "/global/departments"
    request_body = {
        "name": "2nd temp department",
        "description": "",
        "agentIds": [agent2_id],
        "isAvailableInLiveChat": True,
        "isAvailableInTicketingAndMessaging": True,
        "isAvailableInVoice": True,
        "offlineMessageMailTo": "toAllAgents",
        "offlineMessageEmailAddresses": "",
    }

    res_create = send_request(
        request_url_create,
        None,
        "POST",
        None,
        login_data["common_headers"],
        request_body,
    )
    # pdb.set_trace()
    assert res_create.status_code == 201, (
        "Failed with status code: "
        + str(res_create.status_code)
        + " and response: "
        + str(res_create.json())
    )
    logger.info(
        "\n ======= 2nd department has been created and agent2 is added to it. ======="
    )
    yield res_create

    # teardown: delete the newly-created department
    created_id = res_create.json()["id"]
    request_url_delete = login_data["api_url"] + "/global/departments/" + created_id
    res_delete = send_request(
        request_url_delete, None, "DELETE", None, login_data["common_headers"], None
    )
    # pdb.set_trace()
    assert res_delete.status_code == 204, (
        "Failed with status code: "
        + str(res_delete.status_code)
        + " and response: "
        + str(res_delete.json())
    )

    logger.info("\n ======= 2nd department has been deleted. =======")


@pytest.fixture(scope="function")
def create_3rd_department(login):
    login_data = login
    agent_id = login_data["agent_id"]
    agent2_id = login_data["agent2_id"]

    # add 3rd department and add agent to it
    request_url_create = login_data["api_url"] + "/global/departments"
    request_body = {
        "name": "3rd temp department",
        "description": "",
        "agentIds": [agent_id, agent2_id],
        "isAvailableInLiveChat": True,
        "isAvailableInTicketingAndMessaging": True,
        "isAvailableInVoice": True,
        "offlineMessageMailTo": "toAllAgents",
        "offlineMessageEmailAddresses": "",
    }

    res_create = send_request(
        request_url_create,
        None,
        "POST",
        None,
        login_data["common_headers"],
        request_body,
    )
    # pdb.set_trace()
    assert res_create.status_code == 201, (
        "Failed with status code: "
        + str(res_create.status_code)
        + " and response: "
        + str(res_create.json())
    )
    logger.info(
        "\n ======= 3rd department has been created and agent1 and agent2 are added to it. ======="
    )
    yield res_create

    # teardown: delete the newly-created department
    created_id = res_create.json()["id"]
    request_url_delete = login_data["api_url"] + "/global/departments/" + created_id
    res_delete = send_request(
        request_url_delete, None, "DELETE", None, login_data["common_headers"], None
    )
    # pdb.set_trace()
    assert res_delete.status_code == 204, (
        "Failed with status code: "
        + str(res_delete.status_code)
        + " and response: "
        + str(res_delete.json())
    )

    logger.info("\n ======= 3rd department has been deleted. =======")


@pytest.fixture(scope="function")
def create_4th_department_not_available_in_live_chat(login):
    login_data = login
    agent_id = login_data["agent_id"]

    # add 4th department and add agent to it
    request_url_create = login_data["api_url"] + "/global/departments"
    request_body = {
        "name": "4th temp department",
        "description": "",
        "agentIds": [agent_id],
        "isAvailableInLiveChat": False,
        "isAvailableInTicketingAndMessaging": True,
        "isAvailableInVoice": True,
        "offlineMessageMailTo": "toAllAgents",
        "offlineMessageEmailAddresses": "",
    }

    res_create = send_request(
        request_url_create,
        None,
        "POST",
        None,
        login_data["common_headers"],
        request_body,
    )
    # pdb.set_trace()
    assert res_create.status_code == 201, (
        "Failed with status code: "
        + str(res_create.status_code)
        + " and response: "
        + str(res_create.json())
    )
    logger.info(
        "\n ======= 4th department has been created and agent1 is added to it. ======="
    )
    yield res_create

    # teardown: delete the newly-created department
    created_id = res_create.json()["id"]
    request_url_delete = login_data["api_url"] + "/global/departments/" + created_id
    res_delete = send_request(
        request_url_delete, None, "DELETE", None, login_data["common_headers"], None
    )
    # pdb.set_trace()
    assert res_delete.status_code == 204, (
        "Failed with status code: "
        + str(res_delete.status_code)
        + " and response: "
        + str(res_delete.json())
    )

    logger.info("\n ======= 4th department has been deleted. =======")


@pytest.fixture(scope="function")
def init_department(login, enable_department_config, create_department):
    # wait for new department added to chat server cache as interval is 5s
    time.sleep(6)
    yield create_department


@pytest.fixture(scope="function")
def init_2departments(
    login, enable_department_config, create_department, create_2nd_department
):
    department1_id = create_department.json()["id"]
    department2_id = create_2nd_department.json()["id"]
    # pdb.set_trace()
    # wait for new department added to chat server cache as interval is 5s
    time.sleep(6)
    yield create_department, create_2nd_department, department1_id, department2_id


@pytest.fixture(scope="function")
def init_4departments(
    login,
    enable_department_config,
    create_department,
    create_2nd_department,
    create_3rd_department,
    create_4th_department_not_available_in_live_chat,
):
    department1_id = create_department.json()["id"]
    department2_id = create_2nd_department.json()["id"]
    department3_id = create_3rd_department.json()["id"]
    department4_id = create_4th_department_not_available_in_live_chat.json()["id"]
    # pdb.set_trace()
    # wait for new department added to chat server cache as interval is 5s
    time.sleep(6)
    yield create_department, create_2nd_department, create_3rd_department, create_4th_department_not_available_in_live_chat, department1_id, department2_id, department3_id, department4_id


@pytest.fixture(scope="function")
def init_department_old(login):
    login_data = login

    # enable department config first
    request_url_enable = login_data["api_url"] + "/global/departmentConfig:enable"
    res_enable = send_request(
        request_url_enable,
        None,
        "POST",
        None,
        login_data["common_headers"],
        None,
    )
    # pdb.set_trace()
    assert res_enable.status_code == 200

    # add a new department
    request_url_create = login_data["api_url"] + "/global/departments"
    request_body = {
        "name": "temp department",
        "description": "",
        "agentIds": [],
        "isAvailableInLiveChat": True,
        "isAvailableInTicketingAndMessaging": True,
        "isAvailableInVoice": True,
        "offlineMessageMailTo": "toAllAgents",
        "offlineMessageEmailAddresses": "",
    }

    res_create = send_request(
        request_url_create,
        None,
        "POST",
        None,
        login_data["common_headers"],
        request_body,
    )
    # pdb.set_trace()
    assert res_create.status_code == 201
    logger.info(
        "\n ======= Department Config enabled and a new department has been created ======="
    )

    # wait for new department added to chat server cache as interval is 5s
    time.sleep(6)
    yield res_create

    # teardown: delete the newly-created department
    created_id = res_create.json()["id"]
    request_url_delete = login_data["api_url"] + "/global/departments/" + created_id
    res_delete = send_request(
        request_url_delete, None, "DELETE", None, login_data["common_headers"], None
    )
    # pdb.set_trace()
    assert res_delete.status_code == 204, (
        "Failed with status code: "
        + str(res_delete.status_code)
        + " and response: "
        + str(res_delete.json())
    )

    # teardown: disable department config last
    request_url_disable = login_data["api_url"] + "/global/departmentConfig:disable"
    res_disable = send_request(
        request_url_disable,
        None,
        "POST",
        None,
        login_data["common_headers"],
        None,
    )
    # pdb.set_trace()
    assert res_disable.status_code == 200

    logger.info(
        "\n ======= newly-created department has been deleted and Department Config disabled. ======="
    )


@pytest.fixture(scope="module")
def init_custom_away(login):
    login_data = login

    # enable custom away config
    request_url_enable = login_data["api_url"] + "/Global/agentAwayStatusConfig:enable"
    res_enable = send_request(
        request_url_enable,
        None,
        "POST",
        None,
        login_data["common_headers"],
        None,
    )
    # pdb.set_trace()
    assert res_enable.status_code == 200

    # get custom away list
    request_url_get = login_data["api_url"] + "/Global/agentAwayStatuses"
    res_get = send_request(
        request_url_get,
        {"sortBy": "order", "sortOrder": "asc"},
        "GET",
        None,
        login_data["common_headers"],
        None,
    )
    # pdb.set_trace()
    assert res_get.status_code == 200

    # wait for custom away config enabled added to chat server cache as interval is 5s
    time.sleep(6)
    logger.info(
        "\n ======= custom away has been enabled and list has been returned ======="
    )
    yield res_get

    # teardown: disable custom away config
    request_url_disable = (
        login_data["api_url"] + "/Global/agentAwayStatusConfig:disable"
    )
    res_disable = send_request(
        request_url_disable, None, "POST", None, login_data["common_headers"], None
    )
    # pdb.set_trace()
    assert res_disable.status_code == 200

    logger.info("\n =======  custom away has been disabled. =======")


@pytest.fixture(scope="module")
def enable_auto_translation(login):
    login_data = login

    # enable auto translation config
    req_url = login_data["api_url"] + "/Global/autoTranslationConfig"
    res_enable = send_request(
        req_url,
        None,
        "PUT",
        None,
        login_data["common_headers"],
        {"isEnabledInLiveChat": True},
    )
    # pdb.set_trace()
    assert res_enable.status_code == 200

    # wait for Auto Translation config enabled added to chat server cache as interval is 5s
    time.sleep(6)
    logger.info("\n ======= auto translation config has been enabled =======")
    yield res_enable

    # teardown: disable auto translation config
    res_disable = send_request(
        req_url,
        None,
        "PUT",
        None,
        login_data["common_headers"],
        {"isEnabledInLiveChat": False},
    )
    # pdb.set_trace()
    assert res_disable.status_code == 200

    logger.info("\n ======= auto translation config has been disabled. =======")


@pytest.fixture(scope="function")
def enable_auto_translation_with_exclude_words(login):
    login_data = login

    # enable auto translation config
    req_url = login_data["api_url"] + "/Global/autoTranslationConfig"
    res_enable = send_request(
        req_url,
        None,
        "PUT",
        None,
        login_data["common_headers"],
        {
            "isEnabledInLiveChat": True,
            "excludedWords": [
                "fuck you",
                "傻逼",
                "auto loan",
                "auto",
                "loan",
                "Virtual Scholars",
                "hola",
            ],
        },
    )
    # pdb.set_trace()
    assert res_enable.status_code == 200

    # wait for Auto Translation config enabled added to chat server cache as interval is 5s
    time.sleep(6)
    logger.info(
        "\n ======= auto translation config has been enabled, with exclude words 'fuck you', '傻逼', 'auto loan', 'loan', 'Virtual Scholars', 'hola' ======="
    )
    yield res_enable

    # teardown: disable auto translation config
    res_disable = send_request(
        req_url,
        None,
        "PUT",
        None,
        login_data["common_headers"],
        {"isEnabledInLiveChat": False, "excludedWords": []},
    )
    # pdb.set_trace()
    assert res_disable.status_code == 200

    logger.info("\n ======= auto translation config has been disabled. =======")


@pytest.fixture(scope="module")
def init_restricted_words(login):
    login_data = login
    site_id = login_data["site_id"]

    # enable restricted words config
    request_url_enable = login_data["api_url"] + "/Global/restrictedWordsConfig:enable"
    res_enable = send_request(
        request_url_enable,
        None,
        "POST",
        None,
        login_data["common_headers"],
        None,
    )
    # pdb.set_trace()
    assert res_enable.status_code == 200, (
        "Failed with status code: "
        + str(res_enable.status_code)
        + " and response: "
        + str(res_enable.json())
    )

    # update restricted words list
    req_url_update = login_data["api_url"] + "/Global/restrictedWordsConfig"
    req_body_update = {
        "restrictedWords": "shit",
        "restrictedWordsForVisitors": ["shit"],
        "siteId": site_id,
        "isEnabled": True,
    }
    res_update = send_request(
        req_url_update,
        None,
        "PUT",
        None,
        login_data["common_headers"],
        req_body_update,
    )
    # pdb.set_trace()
    assert res_update.status_code == 200, (
        "Failed with status code: "
        + str(res_update.status_code)
        + " and response: "
        + str(res_update.json())
    )

    # wait for restricted words added to chat server cache as interval is 5s
    time.sleep(6)
    logger.info(
        "\n ======= restricted words has been enabled and chat server cache is refreshed. ======="
    )
    yield res_update

    # teardown:  restore restricted words list to empty
    req_url_empty = login_data["api_url"] + "/Global/restrictedWordsConfig"
    req_body_empty = {
        "restrictedWords": "",
        "restrictedWordsForVisitors": [""],
        "siteId": site_id,
        "isEnabled": True,
    }
    res_empty = send_request(
        req_url_empty,
        None,
        "PUT",
        None,
        login_data["common_headers"],
        req_body_empty,
    )
    # pdb.set_trace()
    assert res_empty.status_code == 200, (
        "Failed with status code: "
        + str(res_empty.status_code)
        + " and response: "
        + str(res_empty.json())
    )

    # teardown: disable restricted words config
    req_url_disable = login_data["api_url"] + "/Global/restrictedWordsConfig:disable"
    res_disable = send_request(
        req_url_disable, None, "POST", None, login_data["common_headers"], None
    )
    # pdb.set_trace()
    assert res_disable.status_code == 200, (
        "Failed with status code: "
        + str(res_disable.status_code)
        + " and response: "
        + str(res_disable.json())
    )

    logger.info(
        "\n =======  restricted words has been restored to default and disabled. ======="
    )

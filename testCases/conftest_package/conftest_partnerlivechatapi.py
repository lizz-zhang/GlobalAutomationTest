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
    generate_small_ip,
    generate_big_ip,
    replace_request_body_data_with_test_data,
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
def init_chat_code_blocked_domain(partner_login):
    login_data = partner_login
    request_url_create = login_data["api_url"] + "/api/livechat/chatCodeBlockedDomains"
    request_body = {
        "domain": "addbypytest.com",
    }
    res = send_request(
        request_url_create,
        None,
        "POST",
        None,
        login_data["common_headers"],
        request_body,
    )
    # pdb.set_trace()
    assert res.status_code == 201, (
        "Failed with status code: "
        + str(res.status_code)
        + " and response: "
        + str(res.json())
    )
    logger.info("\n ======= chat code blocked domain has been created =======")
    # pdb.set_trace()
    yield res
    created_id = res.json()["id"]
    request_url_delete = (
        login_data["api_url"] + "/api/livechat/chatCodeBlockedDomains/" + created_id
    )
    res_delete = send_request(
        request_url_delete, None, "DELETE", None, login_data["common_headers"], None
    )
    assert res_delete.status_code == 204, (
        "Failed with status code: "
        + str(res_delete.status_code)
        + " and response: "
        + str(res_delete.json())
    )
    logger.info(
        "\n ======= newly-created chat code blocked domain has been deleted ======="
    )


@pytest.fixture(scope="function")
def init_vue_domain(partner_login):
    login_data = partner_login
    vue_domain = fake.domain_name()
    request_url_create = (
        login_data["api_url"] + "/api/livechat/vueDomainNames/addDomain"
    )
    request_body = {"domains": [vue_domain], "isSystem": True}
    res = send_request(
        request_url_create,
        None,
        "POST",
        None,
        login_data["common_headers"],
        request_body,
    )
    # pdb.set_trace()
    assert res.status_code == 200, (
        "Failed with status code: "
        + str(res.status_code)
        + " and response: "
        + str(res.json())
    )
    logger.info("\n ======= chat link domain has been created =======")
    yield res
    created_id = res.json()[0]["id"]
    request_url_delete = (
        login_data["api_url"] + "/api/livechat/vueDomainNames/" + created_id
    )
    res_delete = send_request(
        request_url_delete, None, "DELETE", None, login_data["common_headers"], None
    )
    assert res_delete.status_code == 204, (
        "Failed with status code: "
        + str(res_delete.status_code)
        + " and response: "
        + str(res_delete.json())
    )
    logger.info("\n ======= newly-created chat link domain has been deleted =======")


@pytest.fixture(scope="function")
def init_phish_keyword(partner_login):
    login_data = partner_login
    vue_domain = fake.domain_name()
    request_url_create = login_data["api_url"] + "/api/livechat/phishingWords"
    request_body = {"word": "addbypytest"}
    res = send_request(
        request_url_create,
        None,
        "POST",
        None,
        login_data["common_headers"],
        request_body,
    )
    # pdb.set_trace()
    assert res.status_code == 201, (
        "Failed with status code: "
        + str(res.status_code)
        + " and response: "
        + str(res.json())
    )
    logger.info("\n ======= phish keyword has been created =======")
    yield res
    created_id = res.json()["id"]
    request_url_delete = (
        login_data["api_url"] + "/api/livechat/phishingWords/" + created_id
    )
    res_delete = send_request(
        request_url_delete, None, "DELETE", None, login_data["common_headers"], None
    )
    assert res_delete.status_code == 204, (
        "Failed with status code: "
        + str(res_delete.status_code)
        + " and response: "
        + str(res_delete.json())
    )
    logger.info("\n ======= newly-created phish keyword has been deleted =======")

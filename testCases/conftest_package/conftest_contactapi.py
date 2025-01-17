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
def init_sso_contact(login, delete_contact):
    """这个方法会用来生成一个contact"""
    login_data = login
    request_url_create = login_data["api_url"] + "/contact/contacts"
    request_body_create = {
        "name": "test_contact",
        "contactIdentities": [
            {"contactIdentityType": "SSOID", "value": "ticketsso@pytest.com"}
        ],
    }
    res_create_contact = send_request(
        request_url_create,
        None,
        "POST",
        None,
        login_data["common_headers"],
        request_body_create,
    )
    assert res_create_contact.status_code == 201, (
        "Failed with status code: "
        + str(res_create_contact.status_code)
        + " and response: "
        + str(res_create_contact.json())
    )
    # pdb.set_trace()
    contact_id = res_create_contact.json()["id"]
    contact_identity_id = res_create_contact.json()["contactIdentities"][0]["id"]
    yield contact_id, contact_identity_id
    delete_contact(contact_id)


@pytest.fixture(scope="function")
def delete_contact(login):
    """统一使用contacts接口，来删除contact"""
    login_data = login

    def _delete_contact(contact_id):
        request_url_delete = login_data["api_url"] + "/contact/contacts/" + contact_id
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
        logger.info("\n ======= contact %s has been deleted =======" % contact_id)

    yield _delete_contact

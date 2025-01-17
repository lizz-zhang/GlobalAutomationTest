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
def init_ticket(login, delete_ticket):
    login_data = login
    request_url_create = login_data["api_url"] + "/Ticketing/tickets"
    request_body = {
        "subject": "manual ticket - temp subject",
        "priority": "normal",
        "status": "new",
        "channelId": "Internal",
        "contactOrVisitorId": "00000000-0000-0000-0000-000000000000",
        "customFields": {},
        "tagIds": [],
        "assigneeType": "agent",
        "assigneeId": "00000000-0000-0000-0000-000000000000",
        "agentLanguage": "",
        "contactLanguage": "",
        "messages": [
            {
                "sentByType": "agent",
                "sentById": "00000000-0000-0000-0000-000000000000",
                "channelId": "Internal",
                "body": "data:text/plain;base64,ZGRk",
                "type": "text",
                "metadata": {
                    "channel": {},
                    "source": {
                        "name": "",
                        "contactIdentityId": "00000000-0000-0000-0000-000000000000",
                    },
                    "decoration": {"email": {"cc": "", "bcc": "", "subject": "abc"}},
                },
                "attachments": [],
            }
        ],
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
    logger.info("\n ======= manual ticket has been created =======")
    yield res

    created_id = str(res.json()["id"])
    delete_ticket(created_id)


@pytest.fixture(scope="function")
def clean_up_dirty_tickets(login, delete_ticket):
    """这个方法会用来检查和删除ticket"""
    yield
    login_data = login
    request_url_get = login_data["api_url"] + "/Ticketing/tickets"
    res_get_ticket = send_request(
        request_url_get, None, "GET", None, login_data["common_headers"], None
    )
    # pdb.set_trace()
    for i in range(len(res_get_ticket.json()["tickets"])):
        if res_get_ticket.status_code == 200:
            ticket_id = str(res_get_ticket.json()["tickets"][i]["id"])
            delete_ticket(ticket_id)


@pytest.fixture(scope="function")
def delete_ticket(login):
    """统一使用tickets接口，来删除 ticket"""
    login_data = login

    def _delete_ticket(ticket_id):
        request_url_delete = login_data["api_url"] + "/Ticketing/tickets/" + ticket_id
        res_delete = send_request(
            request_url_delete, None, "DELETE", None, login_data["common_headers"], None
        )
        assert res_delete.status_code == 204, (
            "Failed with status code: "
            + str(res_delete.status_code)
            + " and response: "
            + str(res_delete.json())
        )
        logger.info("\n ======= ticket %s has been deleted =======" % ticket_id)

    yield _delete_ticket

"""
这个conftest文件中的fixture是为了兼容旧的测试用例，新的测试用例请使用conftest_chatserver2.py中的fixture。
"""

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
def init_visitor(login, init_campaign, ban_visitor):
    """推荐使用conftest_chatserver2中的generate_visitor_insite。这个fixture要逐步废弃了。"""
    login_data = login
    campaign = init_campaign
    campaign_id = campaign.json()["id"]
    site_id = login_data["site_id"]

    request_url = login_data["chat_server_url"] + f"/visitor.ashx?siteId={site_id}"
    time.sleep(6)  # wait for new campaign added to chat server cache as interval is 5s
    request_body = [
        {
            "type": "batchAction",
            "actions": [
                {"type": "checkBan", "visitorGuid": "", "chatVersion": ""},
                {
                    "type": "newVisitor",
                    "campaignId": campaign_id,
                    "visitorGuid": "",
                    "referrer": "",
                    "landingPage": {},
                    "timezone": -480,
                    "screenResolution": "2048x1152",
                    "ifSupportWebrtc": True,
                    "firstVisitTime": 1689832065785,
                    "visitTimes": 0,
                    "chatTimes": 0,
                    "name": "temp visitor",
                    "email": "tempvisitor@mail.com",
                    "persistentVisitor": False,
                    "chatVersion": "",
                },
                {
                    "type": "pageVisit",
                    "campaignId": campaign_id,
                    "page": {},
                    "chatVersion": "",
                },
                {
                    "type": "getChatButton",
                    "campaignId": campaign_id,
                    "alreadyCampaignId": False,
                    "chatVersion": "",
                },
                {"type": "checkIfOnline", "campaignId": campaign_id, "chatVersion": ""},
                {
                    "type": "checkManualInvitation",
                    "campaignId": campaign_id,
                    "chatVersion": "",
                },
                {
                    "type": "checkAutoInvitation",
                    "campaignId": campaign_id,
                    "chatVersion": "",
                },
                {"type": "getSSORecoverInfo", "chatVersion": ""},
            ],
            "ssoSessionToken": "",
            "id": 2,
        }
    ]

    res = send_request(
        request_url, None, "POST", None, login_data["common_headers"], request_body
    )

    # pdb.set_trace()
    assert res.status_code == 200, "Failed with response: " + str(res.json())
    assert (
        res.json()[0]["payload"][1]["payload"]["ifNewVisitor"] == True
    ), "Failed with response: " + str(res.json())

    visitor_guid = res.json()[0]["payload"][1]["payload"]["visitorGuid"]
    logger.info(
        f"\n ======= new visitor with id: {visitor_guid} has been generated successfully ======="
    )
    yield res
    ban_visitor(visitor_guid)


@pytest.fixture(scope="function")
def init_visitor_with_all_features_campaign(
    login, init_campaign_with_all_features, ban_visitor
):
    """推荐使用conftest_chatserver2中的update_campaign_*** + generate_visitor_insite。这个fixture要逐步废弃了。"""
    login_data = login
    campaign_id = init_campaign_with_all_features.json()["id"]
    site_id = login_data["site_id"]

    request_url = login_data["chat_server_url"] + f"/visitor.ashx?siteId={site_id}"
    time.sleep(6)  # wait for new campaign added to chat server cache as interval is 5s
    request_body = [
        {
            "type": "batchAction",
            "actions": [
                {"type": "checkBan", "visitorGuid": "", "chatVersion": ""},
                {
                    "type": "newVisitor",
                    "campaignId": campaign_id,
                    "visitorGuid": "",
                    "referrer": "",
                    "landingPage": {},
                    "timezone": -480,
                    "screenResolution": "2048x1152",
                    "ifSupportWebrtc": True,
                    "firstVisitTime": 1689832065785,
                    "visitTimes": 0,
                    "chatTimes": 0,
                    "name": "temp visitor",
                    "email": "tempvisitor@mail.com",
                    "persistentVisitor": False,
                    "chatVersion": "",
                },
                {
                    "type": "setCustomVariables",
                    "customVariables": {},
                    "campaignId": campaign_id,
                    "chatVersion": "",
                },
                {
                    "type": "pageVisit",
                    "campaignId": campaign_id,
                    "page": {},
                    "chatVersion": "",
                },
                {
                    "type": "getChatButton",
                    "campaignId": campaign_id,
                    "alreadyCampaignId": False,
                    "chatVersion": "",
                },
                {"type": "checkIfOnline", "campaignId": campaign_id, "chatVersion": ""},
                {
                    "type": "checkManualInvitation",
                    "campaignId": campaign_id,
                    "chatVersion": "",
                },
                {
                    "type": "checkAutoInvitation",
                    "campaignId": campaign_id,
                    "chatVersion": "",
                },
                {"type": "getSSORecoverInfo", "chatVersion": ""},
            ],
            "ssoSessionToken": "",
            "id": 2,
        }
    ]

    res = send_request(
        request_url, None, "POST", None, login_data["common_headers"], request_body
    )

    # pdb.set_trace()
    assert res.status_code == 200, "Failed with response: " + str(res.json())
    assert (
        res.json()[0]["payload"][1]["payload"]["ifNewVisitor"] == True
    ), "Failed with response: " + str(res.json())

    visitor_guid = res.json()[0]["payload"][1]["payload"]["visitorGuid"]
    # pdb.set_trace()
    logger.info(
        f"\n ======= new visitor with id: {visitor_guid} has been generated successfully ======="
    )
    yield res

    ban_visitor(visitor_guid)


@pytest.fixture(scope="function")
def init_visitor_waiting_for_accept(
    login,
    login_agent_console,
    init_visitor_with_all_features_campaign,
    init_campaign_with_all_features,
):
    login_data = login
    site_id = login_data["site_id"]
    dash_url = login_data["dash_url"]

    agent_session_id = login_agent_console.json()["o"][0]["d"]
    agent_version_offset_guid = login_agent_console.json()["o"][0]["e"]["a"][
        "versionOffset"
    ]["Guid"]

    res_init_visitor = init_visitor_with_all_features_campaign
    visitor_guid = res_init_visitor.json()[0]["payload"][1]["payload"]["visitorGuid"]
    visitor_session_id = res_init_visitor.json()[0]["payload"][1]["payload"][
        "sessionId"
    ]

    campaign = init_campaign_with_all_features
    campaign_id = campaign.json()["id"]

    visitor_ashx_url = (
        login_data["chat_server_url"]
        + f"/visitor.ashx?siteId={site_id}&visitorGuid={visitor_guid}"
    )
    livechat_handler3_url = (
        login_data["chat_server_url"] + f"/livechathandler3.ashx?siteId={site_id}"
    )

    #  ======= visitor request chat =======

    request_body_request_chat = [
        {
            "type": "requestChat",
            "campaignId": campaign_id,
            "source": {
                "type": "button",
                "page": {
                    "url": f"{dash_url}/frontEnd/assets/livechat/previewpage/?campaignId={campaign_id}&siteId={site_id}&lang=en",
                    "title": "Preview",
                },
            },
            "isPrechatDone": False,
            "isSupportWebrtc": True,
            "isProcessingDone": True,
            "lastChattedAgents": [],
            "chatVersion": "",
            "sessionId": visitor_session_id,
        }
    ]

    # pdb.set_trace()
    res_request_chat = send_request(
        visitor_ashx_url,
        None,
        "POST",
        None,
        None,
        request_body_request_chat,
    )
    # pdb.set_trace()
    assert res_request_chat.status_code == 200, (
        "Failed with status code: "
        + str(res_request_chat.status_code)
        + " and response: "
        + str(res_request_chat.json())
    )
    assert (
        res_request_chat.json()[0]["type"] == "requestChat"
    ), "Failed with response: " + str(res_request_chat.json())
    logger.info("\n ======= chat has been requested =======")

    yield res_init_visitor, res_request_chat

    #  ======= visitor end chat =======

    chat_guid = res_request_chat.json()[0]["payload"]["chatGuid"]
    # wait for 1s so that final chat duration is > 0 and then it will be displayed in chat history.
    sleep(1)
    request_body_end_chat = [
        {
            "type": "batchAction",
            "actions": [
                {
                    "type": "endChat",
                    "chatGuid": chat_guid,
                    "chatVersion": "",
                    "sessionId": visitor_session_id,
                },
                {
                    "type": "getChatMessages",
                    "chatGuid": chat_guid,
                    "fromId": 1,
                    "chatVersion": "",
                    "sessionId": visitor_session_id,
                },
            ],
            "ssoSessionToken": "",
            "id": 151,
        }
    ]

    # pdb.set_trace()
    res_end_chat = send_request(
        visitor_ashx_url,
        None,
        "POST",
        None,
        None,
        request_body_end_chat,
    )
    # pdb.set_trace()
    assert res_end_chat.status_code == 200
    assert res_end_chat.json()[0]["payload"][0]["type"] == "endChat"
    logger.info("\n ======= chat has been ended =======")

    # loop for 5 seconds x 6 times to check if the chat has been saved to DB
    for i in range(6):
        sleep(5)
        request_url_get = login_data["api_url"] + "/livechat/chats/" + chat_guid
        res_get_chat = send_request(
            request_url_get, None, "GET", None, login_data["common_headers"], None
        )
        # pdb.set_trace()
        if res_get_chat.status_code == 200:
            break

    created_id = str(res_get_chat.json()["id"])
    request_url_delete = login_data["api_url"] + "/livechat/chats/" + created_id
    res_delete = send_request(
        request_url_delete, None, "DELETE", None, login_data["common_headers"], None
    )
    assert res_delete.status_code == 204, (
        "Failed with status code: "
        + str(res_delete.status_code)
        + " and response: "
        + str(res_delete.json())
    )
    logger.info("\n ======= newly-created chat has been deleted =======")


@pytest.fixture(scope="function")
def init_visitor_waiting_for_refuse(
    login,
    login_agent_console,
    init_visitor_with_all_features_campaign,
    init_campaign_with_all_features,
):
    login_data = login
    site_id = login_data["site_id"]
    dash_url = login_data["dash_url"]

    agent_session_id = login_agent_console.json()["o"][0]["d"]
    agent_version_offset_guid = login_agent_console.json()["o"][0]["e"]["a"][
        "versionOffset"
    ]["Guid"]

    res_init_visitor = init_visitor_with_all_features_campaign
    visitor_guid = res_init_visitor.json()[0]["payload"][1]["payload"]["visitorGuid"]
    visitor_session_id = res_init_visitor.json()[0]["payload"][1]["payload"][
        "sessionId"
    ]

    campaign = init_campaign_with_all_features
    campaign_id = campaign.json()["id"]

    visitor_ashx_url = (
        login_data["chat_server_url"]
        + f"/visitor.ashx?siteId={site_id}&visitorGuid={visitor_guid}"
    )
    livechat_handler3_url = (
        login_data["chat_server_url"] + f"/livechathandler3.ashx?siteId={site_id}"
    )

    #  ======= visitor request chat =======

    request_body_request_chat = [
        {
            "type": "requestChat",
            "campaignId": campaign_id,
            "source": {
                "type": "button",
                "page": {
                    "url": f"{dash_url}/frontEnd/assets/livechat/previewpage/?campaignId={campaign_id}&siteId={site_id}&lang=en",
                    "title": "Preview",
                },
            },
            "isPrechatDone": False,
            "isSupportWebrtc": True,
            "isProcessingDone": True,
            "lastChattedAgents": [],
            "chatVersion": "",
            "sessionId": visitor_session_id,
        }
    ]

    # pdb.set_trace()
    res_request_chat = send_request(
        visitor_ashx_url,
        None,
        "POST",
        None,
        None,
        request_body_request_chat,
    )
    # pdb.set_trace()
    assert res_request_chat.status_code == 200, (
        "Failed with status code: "
        + str(res_request_chat.status_code)
        + " and response: "
        + str(res_request_chat.json())
    )
    assert (
        res_request_chat.json()[0]["type"] == "requestChat"
    ), "Failed with response: " + str(res_request_chat.json())
    logger.info("\n ======= chat has been requested =======")

    yield res_init_visitor, res_request_chat

    chat_guid = res_request_chat.json()[0]["payload"]["chatGuid"]

    # loop for 5 seconds x 6 times to check if the chat has been saved to DB
    for i in range(6):
        sleep(5)
        request_url_get = login_data["api_url"] + "/livechat/chats/" + chat_guid
        res_get_chat = send_request(
            request_url_get, None, "GET", None, login_data["common_headers"], None
        )
        # pdb.set_trace()
        if res_get_chat.status_code == 200:
            break

    created_id = str(res_get_chat.json()["id"])
    request_url_delete = (
        login_data["api_url"] + "/livechat/missedAndRefusedChats/" + created_id
    )
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
    logger.info("\n ======= newly-created refused chat has been deleted =======")


@pytest.fixture(scope="function")
def init_visitor_chatting(
    login,
    login_agent_console,
    init_visitor_with_all_features_campaign,
    init_campaign_with_all_features,
):
    login_data = login
    site_id = login_data["site_id"]
    dash_url = login_data["dash_url"]

    agent_session_id = login_agent_console.json()["o"][0]["d"]
    agent_version_offset_guid = login_agent_console.json()["o"][0]["e"]["a"][
        "versionOffset"
    ]["Guid"]

    res_init_visitor = init_visitor_with_all_features_campaign
    visitor_guid = res_init_visitor.json()[0]["payload"][1]["payload"]["visitorGuid"]
    visitor_session_id = res_init_visitor.json()[0]["payload"][1]["payload"][
        "sessionId"
    ]

    campaign = init_campaign_with_all_features
    campaign_id = campaign.json()["id"]

    visitor_ashx_url = (
        login_data["chat_server_url"]
        + f"/visitor.ashx?siteId={site_id}&visitorGuid={visitor_guid}"
    )
    livechat_handler3_url = (
        login_data["chat_server_url"] + f"/livechathandler3.ashx?siteId={site_id}"
    )

    #  ======= visitor request chat =======

    request_body_request_chat = [
        {
            "type": "requestChat",
            "campaignId": campaign_id,
            "source": {
                "type": "button",
                "page": {
                    "url": f"{dash_url}/frontEnd/assets/livechat/previewpage/?campaignId={campaign_id}&siteId={site_id}&lang=en",
                    "title": "Preview",
                },
            },
            "isPrechatDone": False,
            "isSupportWebrtc": True,
            "isProcessingDone": True,
            "lastChattedAgents": [],
            "chatVersion": "",
            "sessionId": visitor_session_id,
        }
    ]

    # pdb.set_trace()
    res_request_chat = send_request(
        visitor_ashx_url,
        None,
        "POST",
        None,
        None,
        request_body_request_chat,
    )
    # pdb.set_trace()
    assert res_request_chat.status_code == 200, (
        "Failed with status code: "
        + str(res_request_chat.status_code)
        + " and response: "
        + str(res_request_chat.json())
    )
    assert (
        res_request_chat.json()[0]["type"] == "requestChat"
    ), "Failed with response: " + str(res_request_chat.json())
    logger.info("\n ======= chat has been requested =======")

    chat_guid = res_request_chat.json()[0]["payload"]["chatGuid"]

    #  ======= Agent accept chat =======
    request_body_accept_chat = {
        "m": [
            {
                "d": 104,
                "a": visitor_guid,
                "messageGuid": "1F9DD742-C3BD-C3AD-6724-68F1A1E53E3D",
                "e": 6,
            },
            {"d": 115, "e": 7, "a": "3"},
            {"d": 131, "e": 8},
        ],
        "s": agent_session_id,
        "l": [],
        "operatorOffset": {"Guid": agent_version_offset_guid, "OffSet": 0},
    }

    # pdb.set_trace()
    res_accept_chat = send_request(
        livechat_handler3_url,
        None,
        "POST",
        None,
        login_data["common_headers"],
        request_body_accept_chat,
    )
    # pdb.set_trace()
    assert res_accept_chat.status_code == 200
    assert res_accept_chat.json()["c"] == 0
    logger.info(
        "\n ======= chat is accepted and now we have a chatting visitor. ======="
    )

    yield res_init_visitor, res_request_chat
    # yield visitor, res_request_chat, res_accept_chat # can return multiple values if needed. For future use.

    #  ======= visitor end chat =======

    # wait for 1s so that final chat duration is > 0 and then it will be displayed in chat history.
    sleep(1)
    request_body_end_chat = [
        {
            "type": "batchAction",
            "actions": [
                {
                    "type": "endChat",
                    "chatGuid": chat_guid,
                    "chatVersion": "",
                    "sessionId": visitor_session_id,
                },
                {
                    "type": "getChatMessages",
                    "chatGuid": chat_guid,
                    "fromId": 1,
                    "chatVersion": "",
                    "sessionId": visitor_session_id,
                },
            ],
            "ssoSessionToken": "",
            "id": 151,
        }
    ]

    # pdb.set_trace()
    res_end_chat = send_request(
        visitor_ashx_url,
        None,
        "POST",
        None,
        None,
        request_body_end_chat,
    )
    # pdb.set_trace()
    assert res_end_chat.status_code == 200
    assert res_end_chat.json()[0]["payload"][0]["type"] == "endChat"
    logger.info("\n ======= chat has been ended =======")

    # loop for 5 seconds x 6 times to check if the chat has been saved to DB
    for i in range(6):
        sleep(5)
        request_url_get = login_data["api_url"] + "/livechat/chats/" + chat_guid
        res_get_chat = send_request(
            request_url_get, None, "GET", None, login_data["common_headers"], None
        )
        # pdb.set_trace()
        if res_get_chat.status_code == 200:
            break

    created_id = str(res_get_chat.json()["id"])
    request_url_delete = login_data["api_url"] + "/livechat/chats/" + created_id
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
        f"\n ======= newly-created chat has been deleted for the #{i} check ======="
    )


@pytest.fixture(scope="function")
def init_visitor_chat_ended(
    login,
    login_agent_console,
    init_visitor_with_all_features_campaign,
    init_campaign_with_all_features,
):
    login_data = login
    site_id = login_data["site_id"]
    dash_url = login_data["dash_url"]

    agent_session_id = login_agent_console.json()["o"][0]["d"]
    agent_version_offset_guid = login_agent_console.json()["o"][0]["e"]["a"][
        "versionOffset"
    ]["Guid"]

    res_visitor = init_visitor_with_all_features_campaign
    visitor_guid = res_visitor.json()[0]["payload"][1]["payload"]["visitorGuid"]
    visitor_session_id = res_visitor.json()[0]["payload"][1]["payload"]["sessionId"]

    campaign = init_campaign_with_all_features
    campaign_id = campaign.json()["id"]

    visitor_ashx_url = (
        login_data["chat_server_url"]
        + f"/visitor.ashx?siteId={site_id}&visitorGuid={visitor_guid}"
    )
    livechat_handler3_url = (
        login_data["chat_server_url"] + f"/livechathandler3.ashx?siteId={site_id}"
    )

    #  ======= visitor request chat =======

    request_body_request_chat = [
        {
            "type": "requestChat",
            "campaignId": campaign_id,
            "source": {
                "type": "button",
                "page": {
                    "url": f"{dash_url}/frontEnd/assets/livechat/previewpage/?campaignId={campaign_id}&siteId={site_id}&lang=en",
                    "title": "Preview",
                },
            },
            "isPrechatDone": False,
            "isSupportWebrtc": True,
            "isProcessingDone": True,
            "lastChattedAgents": [],
            "chatVersion": "",
            "sessionId": visitor_session_id,
        }
    ]

    # pdb.set_trace()
    res_request_chat = send_request(
        visitor_ashx_url,
        None,
        "POST",
        None,
        None,
        request_body_request_chat,
    )
    # pdb.set_trace()
    assert res_request_chat.status_code == 200
    assert res_request_chat.json()[0]["type"] == "requestChat"
    logger.info("\n ======= chat has been requested =======")

    chat_guid = res_request_chat.json()[0]["payload"]["chatGuid"]

    #  ======= Agent accept chat =======
    request_body_accept_chat = {
        "m": [
            {
                "d": 104,
                "a": visitor_guid,
                "messageGuid": "1F9DD742-C3BD-C3AD-6724-68F1A1E53E3D",
                "e": 6,
            },
            {"d": 115, "e": 7, "a": "3"},
            {"d": 131, "e": 8},
        ],
        "s": agent_session_id,
        "l": [],
        "operatorOffset": {"Guid": agent_version_offset_guid, "OffSet": 0},
    }

    # pdb.set_trace()
    res_accept_chat = send_request(
        livechat_handler3_url,
        None,
        "POST",
        None,
        login_data["common_headers"],
        request_body_accept_chat,
    )
    # pdb.set_trace()
    assert res_accept_chat.status_code == 200
    assert res_accept_chat.json()["c"] == 0
    logger.info("\n ======= chat is accepted =======")

    #  ======= visitor end chat =======
    # wait for 2s so that final chat duration is > 0 and then it will be displayed in chat history.
    sleep(2)
    request_body_end_chat = [
        {
            "type": "batchAction",
            "actions": [
                {
                    "type": "endChat",
                    "chatGuid": chat_guid,
                    "chatVersion": "",
                    "sessionId": visitor_session_id,
                },
                {
                    "type": "getChatMessages",
                    "chatGuid": chat_guid,
                    "fromId": 1,
                    "chatVersion": "",
                    "sessionId": visitor_session_id,
                },
            ],
            "ssoSessionToken": "",
            "id": 151,
        }
    ]

    # pdb.set_trace()
    res_end_chat = send_request(
        visitor_ashx_url,
        None,
        "POST",
        None,
        None,
        request_body_end_chat,
    )
    # pdb.set_trace()
    assert res_end_chat.status_code == 200
    assert res_end_chat.json()[0]["payload"][0]["type"] == "endChat"
    logger.info(
        "\n ======= chat has been ended and now we have a chat-ended visitor ======="
    )

    yield res_visitor, res_request_chat
    # yield res_visitor, res_request_chat, res_accept_chat, res_end_chat # can return multiple values if needed. For future use.

    # loop for 5 seconds x 6 times to check if the chat has been saved to DB
    for i in range(6):
        sleep(5)
        request_url_get = login_data["api_url"] + "/livechat/chats/" + chat_guid
        res_get_chat = send_request(
            request_url_get, None, "GET", None, login_data["common_headers"], None
        )
        # pdb.set_trace()
        if res_get_chat.status_code == 200:
            break

    # pdb.set_trace()

    created_id = str(res_get_chat.json()["id"])
    request_url_delete = login_data["api_url"] + "/livechat/chats/" + created_id
    res_delete = send_request(
        request_url_delete, None, "DELETE", None, login_data["common_headers"], None
    )
    assert res_delete.status_code == 204, (
        "Failed with status code: "
        + str(res_delete.status_code)
        + " and response: "
        + str(res_delete.json())
    )
    logger.info("\n ======= newly-created chat has been deleted =======")


@pytest.fixture(scope="function")
def init_visitor_offline_message_no_submit(login, init_visitor, init_campaign):
    """
    This fixture is to generate a visitor in offline message status and this visitor is not going to submit offline message. So no teardown - delete offline message is needed.
    """

    login_data = login
    site_id = login_data["site_id"]

    res_visitor = init_visitor
    visitor_guid = res_visitor.json()[0]["payload"][1]["payload"]["visitorGuid"]
    visitor_session_id = res_visitor.json()[0]["payload"][1]["payload"]["sessionId"]

    campaign = init_campaign
    campaign_id = campaign.json()["id"]

    request_url = (
        login_data["chat_server_url"]
        + f"/visitor.ashx?siteId={site_id}&visitorGuid={visitor_guid}"
    )

    request_body = [
        {
            "type": "enterOfflineMessage",
            "chatVersion": "",
            "sessionId": visitor_session_id,
            "ssoSessionToken": "",
            "id": 61,
        }
    ]

    res_enter_offline_message = send_request(
        request_url, None, "POST", None, None, request_body
    )

    # pdb.set_trace()
    assert res_enter_offline_message.status_code == 200
    assert res_enter_offline_message.json()[0]["type"] == "enterOfflineMessage"
    logger.info(
        "\n ======= Now we have a new visitor in offline message status ======="
    )

    yield res_visitor


@pytest.fixture(scope="function")
def init_visitor_offline_message_with_submit(
    login, init_visitor_with_all_features_campaign, init_campaign_with_all_features
):
    """
    This fixture is to generate a visitor in offline message status and this visitor is going to submit offline message. So teardown - delete offline message is needed.
    """
    login_data = login
    site_id = login_data["site_id"]

    res_visitor = init_visitor_with_all_features_campaign
    visitor_guid = res_visitor.json()[0]["payload"][1]["payload"]["visitorGuid"]
    visitor_session_id = res_visitor.json()[0]["payload"][1]["payload"]["sessionId"]

    campaign = init_campaign_with_all_features
    campaign_id = campaign.json()["id"]

    request_url = (
        login_data["chat_server_url"]
        + f"/visitor.ashx?siteId={site_id}&visitorGuid={visitor_guid}"
    )

    request_body = [
        {
            "type": "enterOfflineMessage",
            "chatVersion": "",
            "sessionId": visitor_session_id,
            "ssoSessionToken": "",
            "id": 61,
        }
    ]

    res_enter_offline_message = send_request(
        request_url, None, "POST", None, None, request_body
    )

    # pdb.set_trace()
    assert res_enter_offline_message.status_code == 200
    assert res_enter_offline_message.json()[0]["type"] == "enterOfflineMessage"
    logger.info(
        "\n ======= Now we have a new visitor in offline message status ======="
    )

    yield res_visitor

    # wait for chatserver & consumer livechatpersistence to save offline message to DB
    sleep(10)
    request_url_search = login_data["api_url"] + "/livechat/offlineMessages:search"
    request_body = {
        "filters": [{"name": "campaignId", "operator": "is", "value": [campaign_id]}]
    }
    res_get_offline_message = send_request(
        request_url_search,
        None,
        "POST",
        None,
        login_data["common_headers"],
        request_body,
    )

    # pdb.set_trace()

    created_id = str(res_get_offline_message.json()["list"][0]["id"])
    request_url_delete = (
        login_data["api_url"] + "/livechat/offlineMessages/" + created_id
    )
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
    logger.info("\n ======= newly-created offline message has been deleted =======")


@pytest.fixture(scope="function")
def visitor_get_first_messages(
    login,
    init_visitor_chatting,
):
    login_data = login
    site_id = login_data["site_id"]

    res_init_visitor, res_request_chat = init_visitor_chatting
    visitor_guid = res_init_visitor.json()[0]["payload"][1]["payload"]["visitorGuid"]
    visitor_session_id = res_init_visitor.json()[0]["payload"][1]["payload"][
        "sessionId"
    ]

    chat_guid = res_request_chat.json()[0]["payload"]["chatGuid"]

    visitor_ashx_url = (
        login_data["chat_server_url"]
        + f"/visitor.ashx?siteId={site_id}&visitorGuid={visitor_guid}"
    )

    #  ======= visitor get first messages =======

    request_body_get_first_messages = [
        {
            "type": "getChatMessages",
            "chatGuid": chat_guid,
            "chatVersion": "",
            "fromId": -1,
            "sessionId": visitor_session_id,
        },
    ]

    # pdb.set_trace()
    res_get_first_messages = send_request(
        visitor_ashx_url,
        None,
        "POST",
        None,
        None,
        request_body_get_first_messages,
    )
    # pdb.set_trace()
    assert res_get_first_messages.status_code == 200, (
        "Failed with status code: "
        + str(res_get_first_messages.status_code)
        + " and response: "
        + str(res_get_first_messages.json())
    )
    assert (
        res_get_first_messages.json()[0]["type"] == "getChatMessages"
    ), "Failed with response: " + str(res_get_first_messages.json())
    logger.info("\n ======= visitor has got first few messages =======")

    yield res_init_visitor, res_request_chat, res_get_first_messages
    # yield res_init_visitor, res_request_chat, res_accept_chat # can return multiple values if needed. For future use.

    #  ======= No need to do the tear down part. Because this fixture calls init_visitor_chatting and init_visitor_chatting will get chat and delete chat. =======


@pytest.fixture(scope="function")
def agent_get_first_messages(
    login,
    login_agent_console,
    init_visitor_chatting,
):
    login_data = login
    site_id = login_data["site_id"]

    agent_session_id = login_agent_console.json()["o"][0]["d"]
    agent_version_offset_guid = login_agent_console.json()["o"][0]["e"]["a"][
        "versionOffset"
    ]["Guid"]

    res_init_visitor, res_request_chat = init_visitor_chatting
    visitor_guid = res_init_visitor.json()[0]["payload"][1]["payload"]["visitorGuid"]
    visitor_session_id = res_init_visitor.json()[0]["payload"][1]["payload"][
        "sessionId"
    ]

    chat_guid = res_request_chat.json()[0]["payload"]["chatGuid"]

    livechat_handler3_url = (
        login_data["chat_server_url"] + f"/livechathandler3.ashx?siteId={site_id}"
    )

    #  ======= agent get first messages =======

    request_body = {
        "m": [{"d": 131, "e": 1045}],
        "s": agent_session_id,
        "l": [{"a": visitor_guid, "b": -1, "latestChatMessageGuid": ""}],
        "operatorOffset": {"Guid": agent_version_offset_guid, "OffSet": 0},
    }

    # pdb.set_trace()
    res_agent_send_message = send_request(
        livechat_handler3_url,
        None,
        "POST",
        None,
        login_data["common_headers"],
        request_body,
    )
    # pdb.set_trace()
    assert res_agent_send_message.status_code == 200, (
        "Failed with status code: "
        + str(res_agent_send_message.status_code)
        + " and response: "
        + str(res_agent_send_message.json())
    )
    assert res_agent_send_message.json()["c"] == 0, " with response: " + str(
        res_agent_send_message.json()
    )

    logger.info("\n ======= agent has got first few messages =======")
    yield res_init_visitor, res_request_chat, res_agent_send_message

    #  ======= No need to do the tear down part. Because this fixture calls init_visitor_chatting and init_visitor_chatting will get chat and delete chat. =======


@pytest.fixture(scope="function")
def agent_transfer_chat_old(
    login,
    login_agent_console,
    init_visitor_chatting,
    agent2_login_agent_console,
):
    login_data = login
    site_id = login_data["site_id"]
    agent2_id = login_data["agent2_id"]

    agent_session_id = login_agent_console.json()["o"][0]["d"]
    agent_version_offset_guid = login_agent_console.json()["o"][0]["e"]["a"][
        "versionOffset"
    ]["Guid"]

    res_init_visitor, res_request_chat = init_visitor_chatting
    visitor_guid = res_init_visitor.json()[0]["payload"][1]["payload"]["visitorGuid"]
    visitor_session_id = res_init_visitor.json()[0]["payload"][1]["payload"][
        "sessionId"
    ]
    chat_guid = res_request_chat.json()[0]["payload"]["chatGuid"]

    livechat_handler3_url = (
        login_data["chat_server_url"] + f"/livechathandler3.ashx?siteId={site_id}"
    )

    #  ======= agent trasnfer chat to agent2 =======

    request_body = {
        "m": [
            {
                "d": 108,
                "a": visitor_guid,
                "b": agent2_id,
                "c": "false",
                "messageGuid": "1B264DBF-2C40-EECC-6CF0-73F717E0D86D",
                "e": 5159,
            }
        ],
        "s": agent_session_id,
        "l": [],
        "operatorOffset": {"Guid": agent_version_offset_guid, "OffSet": 0},
    }

    # pdb.set_trace()
    res_transfer_chat = send_request(
        livechat_handler3_url,
        None,
        "POST",
        None,
        login_data["common_headers"],
        request_body,
    )
    # pdb.set_trace()
    assert res_transfer_chat.status_code == 200, (
        "Failed with status code: "
        + str(res_transfer_chat.status_code)
        + " and response: "
        + str(res_transfer_chat.json())
    )
    assert res_transfer_chat.json()["c"] == 0, " with response: " + str(
        res_transfer_chat.json()
    )

    logger.info("\n ======= agent has transferred the chat to agent2 =======")
    yield res_transfer_chat

    #  ======= No need to do the tear down part. Because this fixture calls init_visitor_chatting and init_visitor_chatting will get chat and delete chat. =======


@pytest.fixture(scope="function")
def agent_send_message(login, login_agent_console, agent_get_first_messages):
    login_data = login
    site_id = login_data["site_id"]

    agent_session_id = login_agent_console.json()["o"][0]["d"]
    agent_version_offset_guid = login_agent_console.json()["o"][0]["e"]["a"][
        "versionOffset"
    ]["Guid"]

    (
        res_init_visitor,
        res_request_chat,
        res_agent_send_message,
    ) = agent_get_first_messages
    visitor_guid = res_init_visitor.json()[0]["payload"][1]["payload"]["visitorGuid"]
    visitor_session_id = res_init_visitor.json()[0]["payload"][1]["payload"][
        "sessionId"
    ]

    agent_latest_message_int_id = res_agent_send_message.json()["m"][-1]["e"]
    agent_latest_message_guid = res_agent_send_message.json()["m"][-1]["messageGuid"]
    agent_send_message_guid = str(uuid.uuid4())

    chat_guid = res_request_chat.json()[0]["payload"]["chatGuid"]

    livechat_handler3_url = (
        login_data["chat_server_url"] + f"/livechathandler3.ashx?siteId={site_id}"
    )

    #  ======= Agent send message =======

    request_body = {
        "m": [
            {
                "d": 102,
                "a": visitor_guid,
                "messageGuid": agent_send_message_guid,
                "e": 73,
                "b": "aGVsbG8gdmlzaXRvcg==",
                "encoding": "base64",
            },
            {"d": 131, "e": 74},
        ],
        "s": agent_session_id,
        "l": [
            {
                "a": visitor_guid,
                "b": agent_latest_message_int_id,
                "latestChatMessageGuid": agent_latest_message_guid,
            }
        ],
        "operatorOffset": {"Guid": agent_version_offset_guid, "OffSet": 0},
    }

    # pdb.set_trace()
    res_agent_send_message = send_request(
        livechat_handler3_url,
        None,
        "POST",
        None,
        login_data["common_headers"],
        request_body,
    )
    # pdb.set_trace()
    assert res_agent_send_message.status_code == 200, (
        "Failed with status code: "
        + str(res_agent_send_message.status_code)
        + " and response: "
        + str(res_agent_send_message.json())
    )
    assert res_agent_send_message.json()["c"] == 0, " with response: " + str(
        res_agent_send_message.json()
    )

    logger.info("\n ======= agent has sent a text message =======")
    yield res_init_visitor, res_request_chat, res_agent_send_message


@pytest.fixture(scope="function")
def ban_visitor_via_agent_console(login, login_agent_console):
    def _ban_visitor_via_agent_console(visitor_guid):
        # pdb.set_trace
        login_data = login
        site_id = login_data["site_id"]

        agent_session_id = login_agent_console.json()["o"][0]["d"]
        agent_version_offset_guid = login_agent_console.json()["o"][0]["e"]["a"][
            "versionOffset"
        ]["Guid"]

        req_url = (
            login_data["chat_server_url"] + f"/livechathandler3.ashx?siteId={site_id}"
        )
        req_body = {
            "m": [
                {
                    "d": 153,
                    "a": visitor_guid,
                    "b": '{"a":"0","b":"192.168.1.27","c":"ban by visitor guid"}',
                    "messageGuid": "D272C4E8-6FD7-10DF-0C1E-7381FF762552",
                    "e": 1563,
                },
            ],
            "s": agent_session_id,
            "l": [],
            "operatorOffset": {"Guid": agent_version_offset_guid, "OffSet": 0},
        }

        # pdb.set_trace()
        res = send_request(
            req_url,
            None,
            "POST",
            None,
            login_data["common_headers"],
            req_body,
        )
        # pdb.set_trace()
        assert res.status_code == 200, "Failed with response: " + str(res.json())
        assert res.json()["c"] == 0, "Failed with response: " + str(res.json())

        # loop for 2 seconds x 6 times to check if the banned visitor has been saved to DB
        request_url_get = login_data["api_url"] + "/LiveChat/bannedVisitors"
        for i in range(6):
            sleep(2)
            res_get_banned_visitors = send_request(
                request_url_get, None, "GET", None, login_data["common_headers"], None
            )
            # pdb.set_trace()
            if res_get_banned_visitors.status_code == 200:
                banned_visitor_list = res_get_banned_visitors.json()["bannedVisitors"]
                # iterate banned_visitor_list to find the banned visitor with the same visitor_guid
                for banned_visitor in banned_visitor_list:
                    if banned_visitor["visitorId"] == visitor_guid:
                        banned_visitor_record_id = banned_visitor["id"]
                        logger.info(
                            f"\n ======= banned visitor guid has been saved to DB with id: {banned_visitor_record_id} successfully at the #{i} check ======="
                        )
                        # pdb.set_trace()
                        return banned_visitor_record_id

    yield _ban_visitor_via_agent_console

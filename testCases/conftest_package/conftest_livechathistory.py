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


@pytest.fixture(scope="session")
def init_chat_via_rabbitmq(login):
    """This fixture is used to create a chat via rabbitmq. It's to be deprecated."""
    login_data = login
    chat_guid = str(uuid.uuid4())
    message_guid = str(uuid.uuid4())
    vhost = login_data["mq_vhost"]
    site_id = login_data["site_id"]

    request_body_template = {
        "vhost": "$vhost$",
        "name": "ChatServer",
        "properties": {"delivery_mode": 2, "headers": {}},
        "routing_key": "PersistenceQueue.EmailQueue.TicketQueue.SalesforceQueue.Dynamics365Queue.ZendeskQueue.WebHookQueue.FullTextIndexLiveChatQueue",
        "delivery_mode": "2",
        "payload": '{"routingKey":"PersistenceQueue.EmailQueue.TicketQueue.SalesforceQueue.Dynamics365Queue.ZendeskQueue.WebHookQueue.FullTextIndexLiveChatQueue","messageEventType":"chatEnded","callbackRoutingKey":"CallbackQueue","remainRetryTimes":5,"name":"RabbitMQMessage","eventTime":"2023-07-22T08:57:17.6706493Z","id":"$message_guid$","type":"ChatEnded","siteId":$site_id$,"data":"{\\"ChatGuid\\":\\"$chat_guid$\\",\\"CampaignId\\":\\"2e38c290-9bdf-490d-a903-5aa9a49b375f\\",\\"AgentIds\\":[\\"8d0b2e55-3d68-430c-a497-4ed72c1349d3\\",\\"4ae886c1-7bdf-46ec-8350-6ba6a2abfabe\\"],\\"RequestTime\\":\\"2023-07-22T08:42:34.1097972Z\\",\\"StartTime\\":\\"2023-07-22T08:42:34.12542Z\\",\\"EndTime\\":\\"2023-07-22T08:57:17.6706493Z\\",\\"CannedMessageCount\\":2,\\"PreChatInfo\\":{\\"PreChatName\\":\\"test1\\",\\"PreChatCompany\\":\\"ccc\\",\\"PreChatPhone\\":\\"232456\\",\\"PreChatEmail\\":\\"test1@1.com\\",\\"PreChatProductService\\":\\"test1\\",\\"PreChatDepartmentId\\":\\"2a0b388b-0a84-470d-a4a9-be47ecce1069\\",\\"CustomFields\\":[]},\\"RequestPageTitle\\":\\"\\",\\"RequestPageUrl\\":\\"http://192.168.8.144/3.html\\",\\"SocialProfileUrl\\":\\"\\",\\"Content\\":[{\\"ChatAction\\":51,\\"SenderName\\":\\"test1\\",\\"Message\\":\\"\\",\\"TranslatedMessage\\":\\"\\",\\"Attachement\\":\\"\\",\\"Time\\":\\"2023-07-22T08:42:34.12542Z\\"},{\\"Id\\":1,\\"ChatAction\\":344,\\"SenderType\\":2,\\"SenderId\\":\\"00000000-0000-0000-0000-000000000000\\",\\"SenderName\\":\\"\\",\\"Message\\":\\"False\\",\\"TranslatedMessage\\":\\"\\",\\"Attachement\\":\\"\\",\\"Time\\":\\"2023-07-22T08:42:34.12542Z\\"},{\\"Id\\":2,\\"ChatAction\\":104,\\"SenderType\\":2,\\"SenderId\\":\\"8d0b2e55-3d68-430c-a497-4ed72c1349d3\\",\\"SenderName\\":\\"srita sync\\",\\"Message\\":\\"Agent srita sync has joined the chat.\\",\\"TranslatedMessage\\":\\"\\",\\"Attachement\\":\\"\\",\\"Time\\":\\"2023-07-22T08:42:34.12542Z\\"},{\\"Id\\":3,\\"ChatAction\\":50,\\"SenderName\\":\\"test1\\",\\"Message\\":\\"gsdgadsg\\",\\"TranslatedMessage\\":\\"\\",\\"Attachement\\":\\"\\",\\"Time\\":\\"2023-07-22T08:55:35.4740642Z\\"},{\\"Id\\":4,\\"ChatAction\\":102,\\"SenderType\\":1,\\"SenderId\\":\\"8d0b2e55-3d68-430c-a497-4ed72c1349d3\\",\\"SenderName\\":\\"srita sync\\",\\"Message\\":\\"weaerhareh\\",\\"TranslatedMessage\\":\\"\\",\\"Attachement\\":\\"\\",\\"Time\\":\\"2023-07-22T08:55:47.3077043Z\\"},{\\"Id\\":5,\\"ChatAction\\":61,\\"SenderId\\":\\"00000000-0000-0000-0000-000000000000\\",\\"SenderName\\":\\"https://rabbit6file.testing.comm100dev.io/fileservice/v1/files/GcK49e5bdLB8Q93FBmmMlRPUTEMtilR9lAcItrObDrc2wKIQeExolByujAft7MmvztexzwNeI-EjEGU7YhZohARUWdsugG7xyN9oYRLMRpbKHJspwhR-50f5TB1Di8ts4RSMYKVvxfTclpP0xoBZAUhh3ZuQkDnRASEO7ZsSD07A⊙2.png⊙test1\\",\\"Message\\":\\"The visitor has sent a file: 2.png\\",\\"TranslatedMessage\\":\\"\\",\\"Attachement\\":\\"GcK49e5bdLB8Q93FBmmMlRPUTEMtilR9lAcItrObDrc2wKIQeExolByujAft7MmvztexzwNeI-EjEGU7YhZohARUWdsugG7xyN9oYRLMRpbKHJspwhR-50f5TB1Di8ts4RSMYKVvxfTclpP0xoBZAUhh3ZuQkDnRASEO7ZsSD07A\\",\\"Time\\":\\"2023-07-22T08:55:49.0948148Z\\"},{\\"Id\\":6,\\"ChatAction\\":172,\\"SenderType\\":1,\\"SenderId\\":\\"8d0b2e55-3d68-430c-a497-4ed72c1349d3\\",\\"SenderName\\":\\"srita sync\\",\\"Message\\":\\"weherhare\\",\\"TranslatedMessage\\":\\"\\",\\"Attachement\\":\\"\\",\\"Time\\":\\"2023-07-22T08:55:57.0282558Z\\"},{\\"Id\\":7,\\"ChatAction\\":108,\\"SenderType\\":1,\\"SenderId\\":\\"8d0b2e55-3d68-430c-a497-4ed72c1349d3\\",\\"SenderName\\":\\"srita sync\\",\\"Message\\":\\"Agent srita sync has transferred the chat to another agent.\\",\\"TranslatedMessage\\":\\"\\",\\"Attachement\\":\\"\\",\\"Time\\":\\"2023-07-22T08:56:11.7368284Z\\"},{\\"Id\\":8,\\"ChatAction\\":107,\\"SenderType\\":2,\\"SenderId\\":\\"4ae886c1-7bdf-46ec-8350-6ba6a2abfabe\\",\\"SenderName\\":\\"srita2 sync\\",\\"Message\\":\\"Agent srita2 sync has joined the chat.\\",\\"TranslatedMessage\\":\\"\\",\\"Attachement\\":\\"\\",\\"Time\\":\\"2023-07-22T08:56:11.7368284Z\\"},{\\"Id\\":9,\\"ChatAction\\":106,\\"SenderType\\":1,\\"SenderId\\":\\"8d0b2e55-3d68-430c-a497-4ed72c1349d3\\",\\"SenderName\\":\\"srita sync\\",\\"Message\\":\\"Agent srita sync has left the chat.\\",\\"TranslatedMessage\\":\\"\\",\\"Attachement\\":\\"\\",\\"Time\\":\\"2023-07-22T08:56:11.7368284Z\\"},{\\"Id\\":10,\\"ChatAction\\":139,\\"SenderType\\":1,\\"SenderId\\":\\"4ae886c1-7bdf-46ec-8350-6ba6a2abfabe\\",\\"SenderName\\":\\"srita2 sync\\",\\"Message\\":\\"Agent is typing...\\",\\"TranslatedMessage\\":\\"\\",\\"Attachement\\":\\"\\",\\"Time\\":\\"2023-07-22T08:56:29.5008992Z\\"},{\\"Id\\":11,\\"ChatAction\\":102,\\"SenderType\\":1,\\"SenderId\\":\\"4ae886c1-7bdf-46ec-8350-6ba6a2abfabe\\",\\"SenderName\\":\\"srita2 sync\\",\\"Message\\":\\"fhdf\\",\\"TranslatedMessage\\":\\"\\",\\"Attachement\\":\\"\\",\\"Time\\":\\"2023-07-22T08:56:30.2861343Z\\"},{\\"Id\\":12,\\"ChatAction\\":102,\\"SenderType\\":1,\\"SenderId\\":\\"4ae886c1-7bdf-46ec-8350-6ba6a2abfabe\\",\\"SenderName\\":\\"srita2 sync\\",\\"Message\\":\\"Goodbye.\\",\\"TranslatedMessage\\":\\"\\",\\"Attachement\\":\\"\\",\\"Time\\":\\"2023-07-22T08:56:39.9594568Z\\"},{\\"Id\\":13,\\"ChatAction\\":102,\\"SenderType\\":1,\\"SenderId\\":\\"4ae886c1-7bdf-46ec-8350-6ba6a2abfabe\\",\\"SenderName\\":\\"srita2 sync\\",\\"Message\\":\\"Please wait for a minute.\\",\\"TranslatedMessage\\":\\"\\",\\"Attachement\\":\\"\\",\\"Time\\":\\"2023-07-22T08:56:41.9055627Z\\"},{\\"Id\\":14,\\"ChatAction\\":106,\\"SenderType\\":1,\\"SenderId\\":\\"4ae886c1-7bdf-46ec-8350-6ba6a2abfabe\\",\\"SenderName\\":\\"srita2 sync\\",\\"Message\\":\\"Agent srita2 sync has left the chat.\\",\\"TranslatedMessage\\":\\"\\",\\"Attachement\\":\\"\\",\\"Time\\":\\"2023-07-22T08:57:17.6706493Z\\"},{\\"Id\\":15,\\"SenderType\\":2,\\"SenderName\\":\\"\\",\\"Message\\":\\"The chat is ended.\\",\\"TranslatedMessage\\":\\"\\",\\"Attachement\\":\\"\\",\\"Time\\":\\"2023-07-22T08:57:17.6706493Z\\"}],\\"RatingGrade\\":-1,\\"RatingComment\\":\\"\\",\\"Attachments\\":[{\\"Name\\":\\"2.png\\",\\"FileKey\\":\\"GcK49e5bdLB8Q93FBmmMlRPUTEMtilR9lAcItrObDrc2wKIQeExolByujAft7MmvztexzwNeI-EjEGU7YhZohARUWdsugG7xyN9oYRLMRpbKHJspwhR-50f5TB1Di8ts4RSMYKVvxfTclpP0xoBZAUhh3ZuQkDnRASEO7ZsSD07A\\"}],\\"NoteAttachments\\":[],\\"Visitor\\":{\\"Guid\\":\\"31471b99-02e9-4bd0-87d8-d193eafee737\\",\\"Status\\":9,\\"Country\\":\\"Hong Kong\\",\\"State\\":\\"\\",\\"City\\":\\"\\",\\"LastName\\":\\"test1\\",\\"LastEmail\\":\\"test1@1.com\\",\\"PageViews\\":1,\\"Company\\":\\"ccc\\",\\"CurrentBrowsing\\":\\"http://192.168.8.144/2.html\\",\\"CustomFields\\":[],\\"CustomVariables\\":[],\\"Department\\":\\"2a0b388b-0a84-470d-a4a9-be47ecce1069\\",\\"Email\\":\\"test1@1.com\\",\\"Name\\":\\"test1\\",\\"Phone\\":\\"232456\\",\\"ProductService\\":\\"test1\\",\\"FirstVisitTime\\":\\"2022-02-23T07:16:07.848Z\\",\\"Visits\\":3,\\"Chats\\":1,\\"Segments\\":[\\"a963aaa6-b58a-4104-98ba-96912fe8cccd\\"],\\"VisitorSession\\":{\\"SessionGuid\\":\\"96a9b39b-dd5b-43fd-835e-bc1b449ae523\\",\\"RelatedType\\":5,\\"RelatedId\\":\\"31471b99-02e9-4bd0-87d8-d193eafee737\\",\\"VisitTime\\":\\"2023-07-22T08:42:16.4240204Z\\",\\"Ip\\":1694565385,\\"ReferrerUrl\\":\\"\\",\\"SearchEngineId\\":\\"00000001-0000-0000-0000-000000000001\\",\\"SearchEngine\\":\\"\\",\\"Keywords\\":\\"\\",\\"Browser\\":\\"Google Chrome 97.0.4692.99\\",\\"FlashVersion\\":\\"\\",\\"Language\\":\\"en-US\\",\\"LandingPageUrl\\":\\"http://192.168.8.144/2.html\\",\\"LandingPageTitle\\":\\"\\",\\"CurrentPageUrl\\":\\"http://192.168.8.144/2.html\\",\\"ScreenResolution\\":\\"2048x1152\\",\\"OperatingSystem\\":\\"Windows 10\\",\\"TimeZone\\":-480,\\"CampaignId\\":\\"2e38c290-9bdf-490d-a903-5aa9a49b375f\\"},\\"CurrentSFObjectType\\":-1,\\"SSOId\\":\\"\\",\\"SFContact\\":[],\\"SFTask\\":[],\\"SFCase\\":[],\\"Dynamics365Options\\":{}},\\"TaskbotIds\\":[],\\"Cobrowses\\":[],\\"AgentWrapup\\":{\\"CategoryList\\":[],\\"Comment\\":\\"\\",\\"SubmitTime\\":\\"2023-07-22T08:57:17.6706493Z\\",\\"CustomFields\\":[]},\\"FirstAgentTimeZoneOffset\\":-480.0,\\"TicketId\\":\\"\\",\\"AttachTicketAgentId\\":\\"00000001-0000-0000-0000-000000000001\\"}","timeSent":"2023-07-22T08:57:17.6706493Z","producedOn":"2023-07-22T08:57:17.6706493Z"}',
        "headers": {},
        "props": {},
        "payload_encoding": "string",
    }

    request_body = replace_dict_value_multi(
        request_body_template,
        {
            "$vhost$": vhost,
            "$message_guid$": message_guid,
            "$site_id$": site_id,
            "$chat_guid$": chat_guid,
        },
    )

    res = send_request(
        login_data["mq_publish_api"],
        None,
        "POST",
        login_data["mq_auth"],
        login_data["common_headers"],
        request_body,
    )
    assert res.status_code == 200
    assert res.json()["routed"] == True
    logger.info("\n ======= chat has been created in rabbitmq =======")

    sleep(10)  # wait for consumer livechatpersistence to consume this message
    request_url_get = login_data["api_url"] + "/livechat/chats/" + chat_guid
    res_get_chat = send_request(
        request_url_get, None, "GET", None, login_data["common_headers"], None
    )

    # chat_saved = False
    # request_url_get = login_data['api_url'] + '/livechat/chats/' + chat_guid
    # while chat_saved is False:
    #     r = send_request(request_url_get, None, 'GET', None, login_data['common_headers'], None)
    #     if r.status_code != 200:
    #         sleep(5)
    #     else:
    #         chat_saved = True

    yield res_get_chat

    created_id = str(res_get_chat.json()["id"])
    request_url_delete = login_data["api_url"] + "/livechat/chats/" + created_id
    r = send_request(
        request_url_delete, None, "DELETE", None, login_data["common_headers"], None
    )
    assert r.status_code == 204
    logger.info("\n ======= newly-created chat has been deleted =======")


@pytest.fixture(scope="function")
def init_chat(
    login, clean_up_dirty_chats, login_agent_console, init_visitor, init_campaign
):
    login_data = login
    site_id = login_data["site_id"]
    dash_url = login_data["dash_url"]

    agent_session_id = login_agent_console.json()["o"][0]["d"]
    agent_version_offset_guid = login_agent_console.json()["o"][0]["e"]["a"][
        "versionOffset"
    ]["Guid"]

    visitor = init_visitor
    visitor_guid = visitor.json()[0]["payload"][1]["payload"]["visitorGuid"]
    visitor_session_id = visitor.json()[0]["payload"][1]["payload"]["sessionId"]

    campaign = init_campaign
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
    logger.info("\n ======= chat has been accepted =======")

    #  ======= visitor end chat =======

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
            logger.info(
                f"\n ======= chat has been saved to DB at the #{i} check ======="
            )
            break

    yield res_get_chat

    res_get_chat_again = send_request(
        request_url_get, None, "GET", None, login_data["common_headers"], None
    )
    # pdb.set_trace()
    if res_get_chat_again.status_code == 200:
        # the chat has not been deleted
        created_id = str(res_get_chat.json()["id"])
        request_url_delete = login_data["api_url"] + "/livechat/chats/" + created_id
        r = send_request(
            request_url_delete, None, "DELETE", None, login_data["common_headers"], None
        )
        assert r.status_code == 204
        logger.info("\n ======= newly-created chat has been deleted =======")
    else:
        logger.warning(
            "\n ======= The chat does not exist. It either has been deleted by test case or has not been saved yet. ======="
        )


@pytest.fixture(scope="function")
def init_chat_with_all_features_campaign(
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

    visitor = init_visitor_with_all_features_campaign
    visitor_guid = visitor.json()[0]["payload"][1]["payload"]["visitorGuid"]
    visitor_session_id = visitor.json()[0]["payload"][1]["payload"]["sessionId"]

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
    logger.info("\n ======= chat has been accepted =======")

    #  ======= visitor end chat =======

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
            logger.info("\n ======= chat has been saved to DB =======")
            break

    yield res_get_chat

    res_get_chat_again = send_request(
        request_url_get, None, "GET", None, login_data["common_headers"], None
    )
    # pdb.set_trace()
    if res_get_chat_again.status_code == 200:
        # the chat has not been deleted
        created_id = str(res_get_chat.json()["id"])
        request_url_delete = login_data["api_url"] + "/livechat/chats/" + created_id
        r = send_request(
            request_url_delete, None, "DELETE", None, login_data["common_headers"], None
        )
        assert r.status_code == 204
        logger.info("\n ======= newly-created chat has been deleted =======")
    else:
        logger.warning(
            "\n ======= The chat does not exist. It either has been deleted by test case or has not been saved yet. ======="
        )


# create a fixture to refresh livechathistory cache for one site
@pytest.fixture(scope="function")
def refresh_livechathistory_cache(login):
    """this will refresh the livechathistory cache for one site, including campaign, auto invitation, form field, wrapup category, segment, skill, so that the chat can be searched in history page."""

    request_url = login["api_url"] + "/livechathistory/historycache/refresh"
    res = send_request(request_url, None, "GET", None, login["common_headers"], None)

    assert res.status_code == 200
    logger.info("\n ======= livechathistory cache has been refreshed =======")
    yield res


@pytest.fixture(scope="function")
def generate_chat_record(
    login,
    clean_up_dirty_chats,
    generate_visitor_insite,
    visitor_end_chat,
    refresh_livechathistory_cache,
    save_chat,
    delete_chat,
):
    """聊天接起来后，谁也没发消息，然后访客结束聊天，生成一个chat记录"""
    (
        res_end_chat,
        res_accept_chat,
        res_new_visitor,
        res_request_chat,
        visitor_ashx_url,
        livechat_handler3_url,
        visitor_guid,
        visitor_session_id,
        campaign_id,
        chat_guid,
        agent_session_id,
        agent_version_offset_guid,
    ) = visitor_end_chat()

    # pdb.set_trace()
    res_get_chat, chat_id = save_chat(chat_guid)

    # pdb.set_trace()
    yield res_get_chat, chat_id, chat_guid
    # pdb.set_trace()
    delete_chat(chat_id)


@pytest.fixture(scope="function")
def generate_chat_record_with_chat_source_is_manual_invitation(
    login,
    clean_up_dirty_chats,
    generate_visitor_insite,
    visitor_request_chat_from_manual_invitation,
    visitor_end_chat_solo_action,
    save_chat,
    delete_chat,
):
    (
        res_new_visitor,
        res_chat_from_manual_invitation,
        visitor_ashx_url,
        visitor_guid,
        visitor_session_id,
        campaign_id,
        chat_guid,
    ) = visitor_request_chat_from_manual_invitation

    visitor_end_chat_solo_action(chat_guid)
    res_get_chat, chat_id = save_chat(chat_guid)

    # pdb.set_trace()
    yield res_get_chat, chat_id, chat_guid
    # pdb.set_trace()
    delete_chat(chat_id)


@pytest.fixture(scope="function")
def generate_chat_record_with_chat_source_is_auto_invitation(
    login,
    clean_up_dirty_chats,
    generate_visitor_insite,
    visitor_request_chat_from_auto_invitation,
    visitor_end_chat,
    refresh_livechathistory_cache,
    save_chat,
    delete_chat,
):

    (
        res_end_chat,
        res_accept_chat,
        res_new_visitor,
        res_request_chat,
        visitor_ashx_url,
        livechat_handler3_url,
        visitor_guid,
        visitor_session_id,
        campaign_id,
        chat_guid,
        agent_session_id,
        agent_version_offset_guid,
    ) = visitor_end_chat()
    res_get_chat, chat_id = save_chat(chat_guid)

    # pdb.set_trace()
    yield res_get_chat, chat_id, chat_guid
    # pdb.set_trace()
    delete_chat(chat_id)


@pytest.fixture(scope="function")
def generate_chat_record_without_delete(
    login,
    clean_up_dirty_chats,
    generate_visitor_insite,
    visitor_end_chat,
    save_chat,
    delete_chat,
):
    # 调用chatserver那边的fixture, visitor_end_chat生成一个chat
    (
        res_end_chat,
        res_accept_chat,
        res_new_visitor,
        res_request_chat,
        visitor_ashx_url,
        livechat_handler3_url,
        visitor_guid,
        visitor_session_id,
        campaign_id,
        chat_guid,
        agent_session_id,
        agent_version_offset_guid,
    ) = visitor_end_chat()

    # pdb.set_trace()
    res_get_chat, chat_id = save_chat(chat_guid)

    # pdb.set_trace()
    yield chat_id
    # there's no delete_chat here because the test case calling this fixture will delete the chat.


@pytest.fixture(scope="function")
def generate_chat_record_with_pre_chat_fields(
    login,
    clean_up_dirty_chats,
    generate_visitor_insite,
    login_agent_console_new,
    visitor_submit_pre_chat_with_all_fields,
    visitor_end_chat,
    save_chat,
    delete_chat,
):
    """可用于History中Chat Search，对于chat的prechat fields进行搜索"""
    # 调用chatserver那边的fixture, 生成一个chat
    (
        res_end_chat,
        res_accept_chat,
        res_new_visitor,
        res_request_chat,
        visitor_ashx_url,
        livechat_handler3_url,
        visitor_guid,
        visitor_session_id,
        campaign_id,
        chat_guid,
        agent_session_id,
        agent_version_offset_guid,
    ) = visitor_end_chat()

    # pdb.set_trace()
    res_get_chat, chat_id = save_chat(chat_guid)

    # pdb.set_trace()
    yield chat_id, chat_guid
    # pdb.set_trace()
    delete_chat(chat_id)


@pytest.fixture(scope="function")
def generate_chat_record_with_post_chat_fields(
    login,
    clean_up_dirty_chats,
    generate_visitor_insite,
    login_agent_console_new,
    visitor_submit_post_chat_with_all_fields,
    save_chat,
    delete_chat,
):
    """可用于History中Chat Search，对于chat的post chat fields进行搜索"""
    # 调用chatserver那边的fixture, 生成一个chat
    (
        res_submit_post_chat,
        res_end_chat,
        res_accept_chat,
        res_new_visitor,
        res_request_chat,
        visitor_ashx_url,
        livechat_handler3_url,
        visitor_guid,
        visitor_session_id,
        campaign_id,
        chat_guid,
        agent_session_id,
        agent_version_offset_guid,
    ) = visitor_submit_post_chat_with_all_fields

    # pdb.set_trace()
    res_get_chat, chat_id = save_chat(chat_guid)

    # pdb.set_trace()
    yield chat_id, chat_guid
    # pdb.set_trace()
    delete_chat(chat_id)


@pytest.fixture(scope="function")
def generate_chat_record_with_post_chat_only_rating(
    login,
    clean_up_dirty_chats,
    generate_visitor_insite,
    login_agent_console_new,
    visitor_submit_post_chat_with_only_rating,
    save_chat,
    delete_chat,
):
    """可用于History中Chat Search，对于chat的post chat fields进行搜索"""
    # 调用chatserver那边的fixture, 生成一个chat
    (
        res_submit_post_chat,
        res_end_chat,
        res_accept_chat,
        res_new_visitor,
        res_request_chat,
        visitor_ashx_url,
        livechat_handler3_url,
        visitor_guid,
        visitor_session_id,
        campaign_id,
        chat_guid,
        agent_session_id,
        agent_version_offset_guid,
    ) = visitor_submit_post_chat_with_only_rating

    # pdb.set_trace()
    res_get_chat, chat_id = save_chat(chat_guid)

    # pdb.set_trace()
    yield chat_id, chat_guid
    # pdb.set_trace()
    delete_chat(chat_id)


@pytest.fixture(scope="function")
def generate_chat_record_with_attachment(
    login,
    clean_up_dirty_chats,
    generate_visitor_insite,
    visitor_send_file,
    visitor_end_chat,
    save_chat,
    delete_chat,
):
    """聊天接起来后，访客发了一个文件，然后结束聊天，生成一个chat记录"""
    (
        res_end_chat,
        res_accept_chat,
        res_new_visitor,
        res_request_chat,
        visitor_ashx_url,
        livechat_handler3_url,
        visitor_guid,
        visitor_session_id,
        campaign_id,
        chat_guid,
        agent_session_id,
        agent_version_offset_guid,
    ) = visitor_end_chat()

    # pdb.set_trace()
    res_get_chat, chat_id = save_chat(chat_guid)

    # pdb.set_trace()
    yield chat_id, chat_guid
    # pdb.set_trace()
    delete_chat(chat_id)


@pytest.fixture(scope="function")
def generate_chat_record_with_text_message_by_visitor(
    login,
    clean_up_dirty_chats,
    generate_visitor_insite,
    visitor_send_text_message,
    visitor_end_chat,
    refresh_livechathistory_cache,
    save_chat,
    delete_chat,
):
    """聊天接起来后，访客发了一条文字消息，然后访客结束聊天，生成一个chat记录"""
    (
        res_end_chat,
        res_accept_chat,
        res_new_visitor,
        res_request_chat,
        visitor_ashx_url,
        livechat_handler3_url,
        visitor_guid,
        visitor_session_id,
        campaign_id,
        chat_guid,
        agent_session_id,
        agent_version_offset_guid,
    ) = visitor_end_chat()

    # pdb.set_trace()
    res_get_chat, chat_id = save_chat(chat_guid)

    # pdb.set_trace()
    yield res_get_chat, chat_id, chat_guid
    # pdb.set_trace()
    delete_chat(chat_id)


@pytest.fixture(scope="function")
def generate_chat_record_with_very_negative_text_message_by_visitor(
    login,
    clean_up_dirty_chats,
    enable_sentiment_analysis_for_live_chat,
    generate_visitor_insite,
    visitor_send_very_negative_text_message,
    visitor_end_chat,
    refresh_livechathistory_cache,
    save_chat,
    delete_chat,
):
    """聊天接起来后，访客发了一条文字消息，然后访客结束聊天，生成一个chat记录"""
    (
        res_end_chat,
        res_accept_chat,
        res_new_visitor,
        res_request_chat,
        visitor_ashx_url,
        livechat_handler3_url,
        visitor_guid,
        visitor_session_id,
        campaign_id,
        chat_guid,
        agent_session_id,
        agent_version_offset_guid,
    ) = visitor_end_chat()

    # pdb.set_trace()
    res_get_chat, chat_id = save_chat(chat_guid)

    # pdb.set_trace()
    yield res_get_chat, chat_id, chat_guid
    # pdb.set_trace()
    delete_chat(chat_id)


@pytest.fixture(scope="function")
def generate_chat_record_with_negative_text_message_by_visitor(
    login,
    clean_up_dirty_chats,
    enable_sentiment_analysis_for_live_chat,
    generate_visitor_insite,
    visitor_send_negative_text_message,
    visitor_end_chat,
    refresh_livechathistory_cache,
    save_chat,
    delete_chat,
):
    """聊天接起来后，访客发了一条文字消息，然后访客结束聊天，生成一个chat记录"""
    (
        res_end_chat,
        res_accept_chat,
        res_new_visitor,
        res_request_chat,
        visitor_ashx_url,
        livechat_handler3_url,
        visitor_guid,
        visitor_session_id,
        campaign_id,
        chat_guid,
        agent_session_id,
        agent_version_offset_guid,
    ) = visitor_end_chat()

    # pdb.set_trace()
    res_get_chat, chat_id = save_chat(chat_guid)

    # pdb.set_trace()
    yield res_get_chat, chat_id, chat_guid
    # pdb.set_trace()
    delete_chat(chat_id)


@pytest.fixture(scope="function")
def generate_chat_record_with_neutral_text_message_by_visitor(
    login,
    clean_up_dirty_chats,
    enable_sentiment_analysis_for_live_chat,
    generate_visitor_insite,
    visitor_send_neutral_text_message,
    visitor_end_chat,
    refresh_livechathistory_cache,
    save_chat,
    delete_chat,
):
    """聊天接起来后，访客发了一条文字消息，然后访客结束聊天，生成一个chat记录"""
    (
        res_end_chat,
        res_accept_chat,
        res_new_visitor,
        res_request_chat,
        visitor_ashx_url,
        livechat_handler3_url,
        visitor_guid,
        visitor_session_id,
        campaign_id,
        chat_guid,
        agent_session_id,
        agent_version_offset_guid,
    ) = visitor_end_chat()

    # pdb.set_trace()
    res_get_chat, chat_id = save_chat(chat_guid)

    # pdb.set_trace()
    yield res_get_chat, chat_id, chat_guid
    # pdb.set_trace()
    delete_chat(chat_id)


@pytest.fixture(scope="function")
def generate_chat_record_with_positive_text_message_by_visitor(
    login,
    clean_up_dirty_chats,
    enable_sentiment_analysis_for_live_chat,
    generate_visitor_insite,
    visitor_send_positive_text_message,
    visitor_end_chat,
    refresh_livechathistory_cache,
    save_chat,
    delete_chat,
):
    """聊天接起来后，访客发了一条文字消息，然后访客结束聊天，生成一个chat记录"""
    (
        res_end_chat,
        res_accept_chat,
        res_new_visitor,
        res_request_chat,
        visitor_ashx_url,
        livechat_handler3_url,
        visitor_guid,
        visitor_session_id,
        campaign_id,
        chat_guid,
        agent_session_id,
        agent_version_offset_guid,
    ) = visitor_end_chat()

    # pdb.set_trace()
    res_get_chat, chat_id = save_chat(chat_guid)

    # pdb.set_trace()
    yield res_get_chat, chat_id, chat_guid
    # pdb.set_trace()
    delete_chat(chat_id)


@pytest.fixture(scope="function")
def generate_chat_record_with_very_positive_text_message_by_visitor(
    login,
    clean_up_dirty_chats,
    enable_sentiment_analysis_for_live_chat,
    generate_visitor_insite,
    visitor_send_very_positive_text_message,
    visitor_end_chat,
    refresh_livechathistory_cache,
    save_chat,
    delete_chat,
):
    """聊天接起来后，访客发了一条文字消息，然后访客结束聊天，生成一个chat记录"""
    (
        res_end_chat,
        res_accept_chat,
        res_new_visitor,
        res_request_chat,
        visitor_ashx_url,
        livechat_handler3_url,
        visitor_guid,
        visitor_session_id,
        campaign_id,
        chat_guid,
        agent_session_id,
        agent_version_offset_guid,
    ) = visitor_end_chat()

    # pdb.set_trace()
    res_get_chat, chat_id = save_chat(chat_guid)

    # pdb.set_trace()
    yield res_get_chat, chat_id, chat_guid
    # pdb.set_trace()
    delete_chat(chat_id)


@pytest.fixture(scope="function")
def generate_chat_record_with_text_message_by_agent(
    login,
    clean_up_dirty_chats,
    generate_visitor_insite,
    agent_send_text_message,
    visitor_end_chat,
    refresh_livechathistory_cache,
    save_chat,
    delete_chat,
):
    """聊天接起来后，Agent发了一条文字消息，然后访客结束聊天，生成一个chat记录"""
    (
        res_end_chat,
        res_accept_chat,
        res_new_visitor,
        res_request_chat,
        visitor_ashx_url,
        livechat_handler3_url,
        visitor_guid,
        visitor_session_id,
        campaign_id,
        chat_guid,
        agent_session_id,
        agent_version_offset_guid,
    ) = visitor_end_chat()

    # pdb.set_trace()
    res_get_chat, chat_id = save_chat(chat_guid)

    # pdb.set_trace()
    yield res_get_chat, chat_id, chat_guid
    # pdb.set_trace()
    delete_chat(chat_id)


@pytest.fixture(scope="function")
def generate_chat_record_with_custom_variable(
    login,
    clean_up_dirty_chats,
    visitor_set_custom_variable,
    visitor_end_chat,
    save_chat,
    delete_chat,
):
    """可用于History中Chat Search，对于chat的custom variable进行搜索"""
    # 调用chatserver那边的fixture, 生成一个chat
    (
        res_end_chat,
        res_accept_chat,
        res_new_visitor,
        res_request_chat,
        visitor_ashx_url,
        livechat_handler3_url,
        visitor_guid,
        visitor_session_id,
        campaign_id,
        chat_guid,
        agent_session_id,
        agent_version_offset_guid,
    ) = visitor_end_chat()

    # pdb.set_trace()
    res_get_chat, chat_id = save_chat(chat_guid)

    # pdb.set_trace()
    yield chat_id, chat_guid
    # pdb.set_trace()
    delete_chat(chat_id)


@pytest.fixture(scope="function")
def generate_chat_record_with_segment(
    login,
    clean_up_dirty_chats,
    init_segment,
    generate_visitor_insite,
    visitor_end_chat,
    save_chat,
    delete_chat,
):
    # 调用chatserver那边的fixture, 生成一个chat
    (
        res_end_chat,
        res_accept_chat,
        res_new_visitor,
        res_request_chat,
        visitor_ashx_url,
        livechat_handler3_url,
        visitor_guid,
        visitor_session_id,
        campaign_id,
        chat_guid,
        agent_session_id,
        agent_version_offset_guid,
    ) = visitor_end_chat()

    # pdb.set_trace()
    res_get_chat, chat_id = save_chat(chat_guid)

    # pdb.set_trace()
    yield chat_id, chat_guid
    # pdb.set_trace()
    delete_chat(chat_id)


@pytest.fixture(scope="function")
def generate_chat_record_with_transfer_log(
    login,
    clean_up_dirty_chats,
    generate_visitor_insite,
    agent_transfer_chat,
    visitor_end_chat,
    save_chat,
    delete_chat,
):
    # 调用chatserver那边的fixture, agent_transfer_chat生成一个有transfer log的chat
    (
        res_end_chat,
        res_accept_chat,
        res_new_visitor,
        res_request_chat,
        visitor_ashx_url,
        livechat_handler3_url,
        visitor_guid,
        visitor_session_id,
        campaign_id,
        chat_guid,
        agent_session_id,
        agent_version_offset_guid,
    ) = visitor_end_chat()

    # pdb.set_trace()
    res_get_chat, chat_id = save_chat(chat_guid)

    # pdb.set_trace()
    yield chat_id
    # pdb.set_trace()
    delete_chat(chat_id)


@pytest.fixture(scope="function")
def generate_chat_record_with_transfer_in_department_log(
    login,
    clean_up_dirty_chats,
    generate_visitor_insite,
    enable_auto_distribution,
    agent_transfer_chat_to_department,
    visitor_end_chat,
    save_chat,
    delete_chat,
):
    (
        res_end_chat,
        res_accept_chat,
        res_new_visitor,
        res_request_chat,
        visitor_ashx_url,
        livechat_handler3_url,
        visitor_guid,
        visitor_session_id,
        campaign_id,
        chat_guid,
        agent_session_id,
        agent_version_offset_guid,
    ) = visitor_end_chat()

    # pdb.set_trace()
    res_get_chat, chat_id = save_chat(chat_guid)

    # pdb.set_trace()
    yield chat_id
    # pdb.set_trace()
    delete_chat(chat_id)


@pytest.fixture(scope="function")
def generate_chat_record_with_wrapup_category_and_comment_during_chat(
    login,
    clean_up_dirty_chats,
    generate_visitor_insite,
    agent_submit_wrapup_category_and_comment_during_chat,
    visitor_end_chat,
    refresh_livechathistory_cache,
    save_chat,
    delete_chat,
):
    """
    调用chatserver那边的fixture, agent_submit_wrapup_category_and_comment, 生成一个有wrapup cateogry & comment的chat
    """

    (
        res_end_chat,
        res_accept_chat,
        res_new_visitor,
        res_request_chat,
        visitor_ashx_url,
        livechat_handler3_url,
        visitor_guid,
        visitor_session_id,
        campaign_id,
        chat_guid,
        agent_session_id,
        agent_version_offset_guid,
    ) = visitor_end_chat()

    # pdb.set_trace()
    res_get_chat, chat_id = save_chat(chat_guid)

    # pdb.set_trace()
    yield chat_id
    # pdb.set_trace()
    delete_chat(chat_id)


@pytest.fixture(scope="function")
def generate_chat_record_with_transfer_out_department_log(
    login,
    clean_up_dirty_chats,
    generate_visitor_with_pre_chat_chatting_contain_department,
    enable_auto_distribution,
    agent_transfer_chat_to_department,
    visitor_end_chat,
    save_chat,
    delete_chat,
):
    (
        res_end_chat,
        res_accept_chat,
        res_new_visitor,
        res_request_chat,
        visitor_ashx_url,
        livechat_handler3_url,
        visitor_guid,
        visitor_session_id,
        campaign_id,
        chat_guid,
        agent_session_id,
        agent_version_offset_guid,
    ) = visitor_end_chat()

    # pdb.set_trace()
    res_get_chat, chat_id = save_chat(chat_guid)

    # pdb.set_trace()
    yield chat_id
    # pdb.set_trace()
    delete_chat(chat_id)


@pytest.fixture(scope="function")
def generate_chat_record_with_wrapup_category_and_comment_in_history(
    generate_chat_record, update_wrapup_comment, update_wrapup_category
):
    res_get_chat, chat_id, chat_guid = generate_chat_record

    logger.info(
        "\n ======= now we have a chat record with wrapup category & comment submitted in history. ======="
    )
    yield res_get_chat, chat_id, chat_guid


@pytest.fixture(scope="function")
def generate_chat_record_with_wrapup_all_fields_in_history(
    generate_chat_record,
    update_wrapup_comment,
    update_wrapup_category,
    update_wrapup_custom_fields,
):
    res_get_chat, chat_id, chat_guid = generate_chat_record

    logger.info(
        "\n ======= now we have a chat record with all fields submitted in history. ======="
    )
    yield res_get_chat, chat_id, chat_guid


@pytest.fixture(scope="function")
def generate_chat_record_with_conversion_log(
    clean_up_dirty_chats,
    init_conversion_action_api_type,
    generate_visitor_insite,
    visitor_end_chat,
    save_chat,
    conversion_achieved,
    save_conversion,
    delete_chat,
):
    # 1. 先生成 api type的conversion action
    conversion_action_name = init_conversion_action_api_type.json()["name"]

    # 2. 生成访客，进行聊天，结束聊天，
    (
        res_end_chat,
        res_accept_chat,
        res_new_visitor,
        res_request_chat,
        visitor_ashx_url,
        livechat_handler3_url,
        visitor_guid,
        visitor_session_id,
        campaign_id,
        chat_guid,
        agent_session_id,
        agent_version_offset_guid,
    ) = visitor_end_chat()

    # pdb.set_trace()
    res_get_chat, chat_id = save_chat(chat_guid)

    # 3. 在聊天结束之后，调用conversion archieved: mark as successful api，这个conversion会和聊天相关联
    conversion_achieved(conversion_action_name, visitor_guid)
    # CAUTION: need to wait for consumer livechatpersistence to consume this conversion log
    # sleep(5)

    save_conversion(chat_guid)
    # pdb.set_trace()
    yield chat_id, chat_guid
    # pdb.set_trace()
    delete_chat(chat_id)


@pytest.fixture(scope="function")
def generate_refused_chat_record(
    login,
    clean_up_dirty_missed_refused_chats,
    generate_visitor_insite,
    agent_refuse_chat,
    save_chat,
    delete_chat,
):
    # 调用chatserver那边的fixture, agent_refuse_chat生成一个 refused chat
    (
        res_refuse_chat,
        res_new_visitor,
        res_request_chat,
        visitor_ashx_url,
        livechat_handler3_url,
        visitor_guid,
        visitor_session_id,
        campaign_id,
        chat_guid,
        agent_session_id,
        agent_version_offset_guid,
    ) = agent_refuse_chat()

    # pdb.set_trace()
    res_get_chat, chat_id = save_chat(chat_guid)

    # pdb.set_trace()
    yield chat_id
    # pdb.set_trace()
    delete_chat(chat_id)


@pytest.fixture(scope="function")
def generate_missed_chat_record(
    login,
    clean_up_dirty_missed_refused_chats,
    login_agent_console_new,
    generate_visitor_insite,
    visitor_end_waiting_chat,
    save_chat,
    delete_chat,
):
    # 调用chatserver那边的fixture, visitor_end_waiting_chat 生成一个 missed chat
    (
        res_end_chat,
        res_new_visitor,
        res_request_chat,
        visitor_ashx_url,
        visitor_guid,
        visitor_session_id,
        campaign_id,
        chat_guid,
    ) = visitor_end_waiting_chat()

    # pdb.set_trace()
    res_get_chat, chat_id = save_chat(chat_guid)

    # pdb.set_trace()
    yield chat_id
    # pdb.set_trace()
    delete_chat(chat_id)


@pytest.fixture(scope="function")
def generate_refused_chat_record_without_delete(
    login,
    clean_up_dirty_missed_refused_chats,
    generate_visitor_insite,
    agent_refuse_chat,
    save_chat,
    delete_chat,
):
    # 调用chatserver那边的fixture, agent_refuse_chat生成一个 refused chat
    (
        res_refuse_chat,
        res_new_visitor,
        res_request_chat,
        visitor_ashx_url,
        livechat_handler3_url,
        visitor_guid,
        visitor_session_id,
        campaign_id,
        chat_guid,
        agent_session_id,
        agent_version_offset_guid,
    ) = agent_refuse_chat()

    # pdb.set_trace()
    res_get_chat, chat_id = save_chat(chat_guid)

    # pdb.set_trace()
    yield chat_id
    # there's no delete_chat here because the test case calling this fixture will delete the chat.


@pytest.fixture(scope="function")
def search_chat_record(login, refresh_livechathistory_cache):

    def _search_chat_record(chat_id):
        request_url_get = login["api_url"] + "/livechat/chats/" + chat_id
        res_get_chat = send_request(
            request_url_get, None, "GET", None, login["common_headers"], None
        )

        return res_get_chat.json()

    # pdb.set_trace()
    yield _search_chat_record
    # pdb.set_trace()


@pytest.fixture(scope="function")
def generate_offline_message_record(
    login,
    clean_up_dirty_offline_messages,
    generate_visitor_insite,
    visitor_submit_offline_message,
    save_offline_message,
    delete_offline_message,
):
    (
        res_submit_offline_message,
        res_new_visitor,
        visitor_guid,
        visitor_session_id,
        campaign_id,
        visitor_ashx_url,
    ) = visitor_submit_offline_message

    # pdb.set_trace()
    (offline_message_id, offline_message_guid) = save_offline_message(campaign_id)
    # pdb.set_trace()

    yield offline_message_id, offline_message_guid

    # pdb.set_trace()
    delete_offline_message(offline_message_id)


@pytest.fixture(scope="function")
def generate_offline_message_record_with_segment(
    login,
    clean_up_dirty_offline_messages,
    init_segment,
    generate_visitor_insite,
    visitor_submit_offline_message,
    save_offline_message,
    delete_offline_message,
):
    """There's a bug54635: in livechathistory - the segment is saved to DB but not displayed in History page and API. So don't use this fixture yet."""
    (
        res_submit_offline_message,
        res_new_visitor,
        visitor_guid,
        visitor_session_id,
        campaign_id,
        visitor_ashx_url,
    ) = visitor_submit_offline_message

    # pdb.set_trace()
    (offline_message_id, offline_message_guid) = save_offline_message(campaign_id)
    # pdb.set_trace()

    yield offline_message_id

    # pdb.set_trace()
    delete_offline_message(offline_message_id)


@pytest.fixture(scope="function")
def generate_offline_message_record_without_delete(
    login,
    clean_up_dirty_offline_messages,
    generate_visitor_insite,
    visitor_submit_offline_message,
    save_offline_message,
    delete_offline_message,
):
    (
        res_submit_offline_message,
        res_new_visitor,
        visitor_guid,
        visitor_session_id,
        campaign_id,
        visitor_ashx_url,
    ) = visitor_submit_offline_message

    # pdb.set_trace()
    (offline_message_id, offline_message_guid) = save_offline_message(campaign_id)
    # pdb.set_trace()

    yield offline_message_id
    # there's no delete_offline_message here because the test case calling this fixture will delete the offline message.


@pytest.fixture(scope="function")
def init_offline_message(
    login, clean_up_dirty_offline_messages, init_visitor, init_campaign
):
    login_data = login
    site_id = login_data["site_id"]

    visitor = init_visitor
    visitor_guid = visitor.json()[0]["payload"][1]["payload"]["visitorGuid"]
    visitor_session_id = visitor.json()[0]["payload"][1]["payload"]["sessionId"]

    campaign = init_campaign
    campaign_id = campaign.json()["id"]

    request_url = (
        login_data["chat_server_url"]
        + f"/visitor.ashx?siteId={site_id}&visitorGuid={visitor_guid}"
    )

    request_body = [
        {
            "type": "submitOfflineMessage",
            "campaignId": campaign_id,
            "form": {
                "name": "temp visitor",
                "email": "tempvisitor@mail.com",
                "phone": "13900000000",
                "company": "",
                "department": "",
                "subject": "Hello subject",
                "content": "Hello offline message content.",
                "attachment": {},
            },
            "source": {"type": "button", "page": {}},
            "sessionId": visitor_session_id,
            "ssoSessionToken": "",
            "id": 64,
        }
    ]

    res = send_request(
        request_url, None, "POST", None, login_data["common_headers"], request_body
    )

    # pdb.set_trace()
    assert res.status_code == 200
    assert res.json()[0]["type"] == "submitOfflineMessage"
    logger.info(
        "\n ======= a new offline message has been created successfully in chatserver ======="
    )

    # loop for 5 seconds x 6 times to check if the offline message has been saved to DB
    for i in range(6):
        sleep(5)
        request_url_search = login_data["api_url"] + "/livechat/offlineMessages:search"
        request_body = {
            "filters": [
                {"name": "campaignId", "operator": "is", "value": [campaign_id]}
            ]
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
        if res_get_offline_message.status_code == 200:
            break

    # pdb.set_trace()
    yield res_get_offline_message

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


@pytest.fixture(scope="session")
def clean_up_dirty_chats(login):
    """在测试用例执行之前，删除既有的chat脏数据，以免影响测试用例运行"""
    login_data = login

    request_url_search = login_data["api_url"] + "/livechat/chats:search"
    request_body = {
        "filters": [{"name": "departmentId", "operator": "ignored", "value": [""]}]
    }  # 这个条件会将所有duration>0的chat都找出来，接口会做分页，默认50条一页。
    res_get_chats = send_request(
        request_url_search,
        None,
        "POST",
        None,
        login_data["common_headers"],
        request_body,
    )
    # pdb.set_trace()

    if res_get_chats.status_code == 200 and len(res_get_chats.json()["list"]) > 0:
        request_url_delete = login_data["api_url"] + "/livechat/chats/"
        batch_delete_chat_list = []
        for item in res_get_chats.json()["list"]:
            chat_id = str(item["id"])
            batch_delete_chat_list.append(chat_id)

        res_batch_delete = send_request(
            request_url_delete,
            None,
            "DELETE",
            None,
            login_data["common_headers"],
            batch_delete_chat_list,
        )
        # pdb.set_trace()
        assert res_batch_delete.status_code == 204, (
            "Failed with status code: "
            + str(res_batch_delete.status_code)
            + " and response: "
            + str(res_batch_delete.json())
        )
        logger.info("\n ======= all existing dirty chats have been cleaned up. =======")


@pytest.fixture(scope="session")
def clean_up_dirty_offline_messages(login):
    """在测试用例执行之前，删除既有的offline_messages脏数据，以免影响测试用例运行"""
    login_data = login

    request_url_search = login_data["api_url"] + "/livechat/offlineMessages:search"
    request_body = {
        "filters": [{"name": "departmentId", "operator": "ignored", "value": [""]}]
    }  # 这个条件会将所有duration>0的chat都找出来，接口会做分页，默认50条一页。
    res_get_messages = send_request(
        request_url_search,
        None,
        "POST",
        None,
        login_data["common_headers"],
        request_body,
    )
    # pdb.set_trace()

    if res_get_messages.status_code == 200 and len(res_get_messages.json()["list"]) > 0:
        request_url_delete = login_data["api_url"] + "/livechat/offlineMessages/"
        batch_delete_list = []
        for item in res_get_messages.json()["list"]:
            message_id = str(item["id"])
            batch_delete_list.append(message_id)

        # pdb.set_trace()
        res_batch_delete = send_request(
            request_url_delete,
            None,
            "DELETE",
            None,
            login_data["common_headers"],
            batch_delete_list,
        )
        # pdb.set_trace()
        assert res_batch_delete.status_code == 204, (
            "Failed with status code: "
            + str(res_batch_delete.status_code)
            + " and response: "
            + str(res_batch_delete.json())
        )
        logger.info(
            "\n ======= all existing dirty offline messages have been cleaned up. ======="
        )


@pytest.fixture(scope="session")
def clean_up_dirty_missed_refused_chats(login):
    """在测试用例执行之前，删除既有的missed & refused chat脏数据，以免影响测试用例运行"""
    login_data = login

    request_url_search = (
        login_data["api_url"] + "/livechat/missedAndRefusedChats:search"
    )
    request_body = {
        "filters": [{"name": "departmentId", "operator": "ignored", "value": [""]}]
    }  # 这个条件会将所有duration>0的chat都找出来，接口会做分页，默认50条一页。
    res_get_chats = send_request(
        request_url_search,
        None,
        "POST",
        None,
        login_data["common_headers"],
        request_body,
    )
    # pdb.set_trace()

    if res_get_chats.status_code == 200 and len(res_get_chats.json()["list"]) > 0:
        request_url_delete = login_data["api_url"] + "/livechat/missedAndRefusedChats/"
        batch_delete_chat_list = []
        for item in res_get_chats.json()["list"]:
            chat_id = str(item["id"])
            batch_delete_chat_list.append(chat_id)

        # pdb.set_trace()
        res_batch_delete = send_request(
            request_url_delete,
            None,
            "DELETE",
            None,
            login_data["common_headers"],
            batch_delete_chat_list,
        )
        # pdb.set_trace()
        assert res_batch_delete.status_code == 204, (
            "Failed with status code: "
            + str(res_batch_delete.status_code)
            + " and response: "
            + str(res_batch_delete.json())
        )
        logger.info(
            "\n ======= all existing dirty missed & refused chats have been cleaned up. ======="
        )


@pytest.fixture(scope="function")
def save_and_delete_chat(login, delete_chat):
    """这个方法会用来检查和删除 normal chat, missed chat, refused chat"""
    login_data = login

    def _save_and_delete_chat(chat_guid):
        # loop for 5 seconds x 6 times to check if the chat has been saved to DB
        for i in range(6):
            sleep(5)
            request_url_get = login_data["api_url"] + "/livechat/chats/" + chat_guid
            res_get_chat = send_request(
                request_url_get, None, "GET", None, login_data["common_headers"], None
            )
            # pdb.set_trace()
            if res_get_chat.status_code == 200:
                logger.info(
                    f"\n ======= chat has been saved to DB at the #{i} check ======="
                )
                chat_id = str(res_get_chat.json()["id"])
                delete_chat(chat_id)
                break

    yield _save_and_delete_chat


@pytest.fixture(scope="function")
def save_chat(login):
    """这个方法会用来检查normal chat, missed chat, refused chat. 检查chat是否已经保存到DB，如果已经保存，则返回chat_id"""
    login_data = login

    def _save_chat(chat_guid):
        # loop for 5 seconds x 6 times to check if the chat has been saved to DB
        for i in range(6):
            sleep(5)
            request_url_get = login_data["api_url"] + "/livechat/chats/" + chat_guid
            res_get_chat = send_request(
                request_url_get, None, "GET", None, login_data["common_headers"], None
            )
            # pdb.set_trace()
            if res_get_chat.status_code == 200:
                logger.info(
                    f"\n ======= chat has been saved to DB at the #{i} check ======="
                )
                chat_id = str(res_get_chat.json()["id"])
                return res_get_chat, chat_id

    yield _save_chat


@pytest.fixture(scope="function")
def save_conversion(login):
    """这个方法会用来检查conversionaction是否同步到reporting,conversionlog数据是否已经消费成功"""
    login_data = login

    def _save_conversion(chat_guid):
        # loop for 5 seconds x 60 times to check if the conversion has been saved to DB
        for i in range(120):
            sleep(5)
            site_id = login_data["site_id"]
            request_url_get = (
                login_data["api_url"]
                + "/LiveChat/conversionLogs?include=conversionAction"
            )
            params = {"chatGuid": chat_guid, "siteId": site_id}
            res_get_conversion_log = send_request(
                request_url_get, params, "GET", None, login_data["common_headers"], None
            )
            # pdb.set_trace()
            if (
                res_get_conversion_log.status_code == 200
                and len(res_get_conversion_log.json()) > 0
                and "conversionAction" in res_get_conversion_log.json()[0]
            ):
                logger.info(
                    f"\n ======= conversion has been saved to DB at the #{i} check ======="
                )
                break
            else:
                logger.info(
                    f"\n ======= conversion has not been saved to DB at the #{i} check ======="
                )

    yield _save_conversion


@pytest.fixture(scope="function")
def delete_chat(login):
    """统一使用chats接口，来删除 normal chat, missed chat, refused chat"""
    login_data = login

    def _delete_chat(chat_id):
        request_url_delete = login_data["api_url"] + "/livechat/chats/" + chat_id
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

    yield _delete_chat


@pytest.fixture(scope="function")
def delete_missed_refused_chat(login):
    """暂时不需要这个方案，使用上面delete_chat fixture来删除missed和refused chat"""
    login_data = login

    # chat_id = str(res_get_chat.json()["id"])

    def _delete_missed_refused_chat(chat_id):
        request_url_delete = (
            login_data["api_url"] + "/livechat/missedAndRefusedChats/" + chat_id
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
        logger.info(
            "\n ======= newly-created missed or refused chat has been deleted ======="
        )

    yield _delete_missed_refused_chat


@pytest.fixture(scope="function")
def save_and_delete_offline_message(login, delete_offline_message):
    """这个方法会用来检查和删除 normal chat, missed chat, refused chat"""
    login_data = login

    def _save_and_delete_offline_message(campaign_id):
        # loop for 5 seconds x 6 times to check if the offline message has been saved to DB
        for i in range(6):
            sleep(5)
            request_url_search = (
                login_data["api_url"] + "/livechat/offlineMessages:search"
            )
            request_body = {
                "filters": [
                    {"name": "campaignId", "operator": "is", "value": [campaign_id]}
                ]
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

            if (
                res_get_offline_message.status_code == 200
                and len(res_get_offline_message.json()["list"]) > 0
            ):
                logger.info(
                    f"\n ======= Offline Message has been saved to DB at the #{i} check ======="
                )
                for item in res_get_offline_message.json()["list"]:
                    offline_message_id = str(item["id"])
                    delete_offline_message(offline_message_id)
                break

    yield _save_and_delete_offline_message


@pytest.fixture(scope="function")
def save_offline_message(login):
    login_data = login

    def _save_offline_message(campaign_id):
        # loop for 5 seconds x 6 times to check if the offline message has been saved to DB
        for i in range(6):
            sleep(5)
            request_url_search = (
                login_data["api_url"]
                + "/livechat/offlineMessages:search?pageIndex=1&pageSize=50&sortBy=createdTime&sortOrder=desc"
            )
            request_body = {
                "filters": [
                    {"name": "campaignId", "operator": "is", "value": [campaign_id]}
                ]
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
            if (
                res_get_offline_message.status_code == 200
                and len(res_get_offline_message.json()["list"]) > 0
            ):
                logger.info(
                    f"\n ======= Offline Message has been saved to DB at the #{i} check ======="
                )
                offline_message_id = str(
                    res_get_offline_message.json()["list"][0]["id"]
                )
                offline_message_guid = str(
                    res_get_offline_message.json()["list"][0]["guid"]
                )
                return offline_message_id, offline_message_guid

    yield _save_offline_message


@pytest.fixture(scope="function")
def delete_offline_message(login):
    login_data = login

    def _delete_offline_message(offline_message_id):
        request_url_delete = (
            login_data["api_url"] + "/livechat/offlineMessages/" + offline_message_id
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

    yield _delete_offline_message


@pytest.fixture(scope="function")
def update_wrapup_comment(login, generate_chat_record):
    req_url = login["api_url"] + "/livechat/chatWrapups/"
    res_get_chat, chat_id, chat_guid = generate_chat_record
    req_body = {"chatId": chat_id, "comment": "temp comment submitted in history"}

    res = send_request(req_url, None, "POST", None, login["common_headers"], req_body)

    # pdb.set_trace()
    assert res.status_code == 201, (
        "Failed with status code: "
        + str(res.status_code)
        + " and response: "
        + str(res.json())
    )
    logger.info("\n ======= chat wrapup comment is submitted in history. =======")


@pytest.fixture(scope="function")
def update_wrapup_category(login, generate_chat_record, get_wrapup_category_option):
    res_get_chat, chat_id, chat_guid = generate_chat_record
    res_get_wrapup_category_option, first_option_id, second_option_id = (
        get_wrapup_category_option
    )

    req_url = login["api_url"] + f"/livechat/chats/{chat_guid}/chatWrapupCategories"
    req_body = [{"chatId": chat_id, "categoryOptionId": first_option_id}]

    res = send_request(req_url, None, "POST", None, login["common_headers"], req_body)

    # pdb.set_trace()
    assert res.status_code == 200, (
        "Failed with status code: "
        + str(res.status_code)
        + " and response: "
        + str(res.json())
    )
    logger.info("\n ======= chat wrapup category is submitted in history. =======")


@pytest.fixture(scope="function")
def update_wrapup_custom_fields(
    login, update_campaign_wrapup_add_all_fields, generate_chat_record
):
    req_url = login["api_url"] + "/livechat/chatFieldResults/"
    res_get_chat, chat_id, chat_guid = generate_chat_record
    campaign_id, custom_fields_list = update_campaign_wrapup_add_all_fields

    req_body = [
        {
            "fieldName": custom_fields_list[0]["name"],
            "value": "temp text field value",
            "chatId": chat_id,
            "formType": "wrapup",
            "fieldId": custom_fields_list[0]["id"],
        },
        {
            "fieldName": custom_fields_list[1]["name"],
            "value": "temp textArea field value\nmultiple lines",
            "chatId": chat_id,
            "formType": "wrapup",
            "fieldId": custom_fields_list[1]["id"],
        },
        {
            "fieldName": custom_fields_list[2]["name"],
            "value": "rb1",
            "chatId": chat_id,
            "formType": "wrapup",
            "fieldId": custom_fields_list[2]["id"],
        },
        {
            "fieldName": custom_fields_list[3]["name"],
            "value": "true",
            "chatId": chat_id,
            "formType": "wrapup",
            "fieldId": custom_fields_list[3]["id"],
        },
        {
            "fieldName": custom_fields_list[4]["name"],
            "value": "ddl1",
            "chatId": chat_id,
            "formType": "wrapup",
            "fieldId": custom_fields_list[4]["id"],
        },
        {
            "fieldName": custom_fields_list[5]["name"],
            "value": ["cbl1", "cbl2"],
            "chatId": chat_id,
            "formType": "wrapup",
            "fieldId": custom_fields_list[5]["id"],
        },
    ]

    res = send_request(req_url, None, "POST", None, login["common_headers"], req_body)

    # pdb.set_trace()
    assert res.status_code == 200, (
        "Failed with status code: "
        + str(res.status_code)
        + " and response: "
        + str(res.json())
    )
    logger.info(
        "\n ======= chat wrapup custom fields are submitted in history. ======="
    )

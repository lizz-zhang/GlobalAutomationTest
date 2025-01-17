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
def create_keyword_chatbot(login, clean_up_chatbot):
    req_url = login["api_url"] + "/chatbot/chatbots"
    req_body = {
        "isCustomAnswersEnabled": True,
        "isGenerativeAnswersEnabled": False,
        "engineId": "266b567c-c716-43c4-84e1-5723f5badfaf",
        "thirdPartyWebhookUrl": "https://",
        "isManual": True,
        "systemAvatarId": "00000000-0000-0000-0000-000000000001",
        "paymentStatus": "paid",
        "name": "temp keyword bot",
        "languageId": "en",
        "channelIds": ["Live Chat"],
    }

    res = send_request(
        req_url,
        None,
        "POST",
        None,
        login["common_headers"],
        req_body,
    )
    # pdb.set_trace()
    assert res.status_code == 201, (
        "Failed with status code: "
        + str(res.status_code)
        + " and response: "
        + str(res.json())
    )
    logger.info("\n ======= keyword chatbot has been created =======")
    yield res

    created_id = res.json()["id"]
    req_url_delete = login["api_url"] + "/chatbot/chatbots/" + created_id
    res_delete = send_request(
        req_url_delete,
        None,
        "DELETE",
        None,
        login["common_headers"],
        None,
    )

    # pdb.set_trace()
    assert res_delete.status_code == 204, (
        "Failed with status code: "
        + str(res_delete.status_code)
        + " and response: "
        + str(res_delete.json())
    )
    logger.info("\n ======= newly-created keyword chatbot has been deleted =======")


# create a fixture that will search and delete all chatbot
@pytest.fixture(scope="session")
def clean_up_chatbot(login):
    login_data = login
    request_url_get = login_data["api_url"] + "/Bot/chatbots"
    res_get = send_request(
        request_url_get,
        None,
        "GET",
        None,
        login_data["common_headers"],
        None,
    )
    # pdb.set_trace()
    assert res_get.status_code == 200, (
        "Failed with status code: "
        + str(res_get.status_code)
        + " and response: "
        + str(res_get.json())
    )

    res_get_data = res_get.json()["chatbots"]

    if len(res_get_data) > 0:
        for chatbot in res_get_data:
            bot_id = chatbot["id"]
            request_url_delete = login_data["api_url"] + "/chatbot/chatbots/" + bot_id
            res_delete = send_request(
                request_url_delete,
                None,
                "DELETE",
                None,
                login_data["common_headers"],
                None,
            )
            # pdb.set_trace()
            assert res_delete.status_code == 204, (
                "Failed with status code: "
                + str(res_delete.status_code)
                + " and response: "
                + str(res_delete.json())
            )
        logger.info("\n ======= all existing chat bots have been cleaned up =======")


@pytest.fixture(scope="session")
def create_task_bot(login):
    req_url = login["api_url"] + "/taskbot/taskbots"
    req_body = {
        "name": "temp task bot",
        "ifCustomizeAvatar": False,
        "systemAvatarId": "00000000-0000-0000-0000-000000000001",
        "latestVersionId": "00000000-0000-0000-0000-000000000000",
        "avatar": "",
    }

    res = send_request(
        req_url,
        None,
        "POST",
        None,
        login["common_headers"],
        req_body,
    )
    # pdb.set_trace()
    assert res.status_code == 201, (
        "Failed with status code: "
        + str(res.status_code)
        + " and response: "
        + str(res.json())
    )
    logger.info(
        "\n ======= task bot has been created, but it is not ready to use yet. We need to initialize it. ======="
    )
    yield res

    created_id = res.json()["id"]
    req_url_delete = login["api_url"] + "/taskbot/taskbots/" + created_id
    res_delete = send_request(
        req_url_delete,
        None,
        "DELETE",
        None,
        login["common_headers"],
        None,
    )

    # pdb.set_trace()
    assert res_delete.status_code == 204, (
        "Failed with status code: "
        + str(res_delete.status_code)
        + " and response: "
        + str(res_delete.json())
    )
    logger.info("\n ======= newly-created task bot has been deleted =======")


@pytest.fixture(scope="session")
def init_task_bot(login, create_task_bot):
    task_bot_id = create_task_bot.json()["id"]

    req_url = login["api_url"] + "/taskbot/taskbotversions:save"

    # currently I'm using the FAQ taskbot template.
    req_body = {
        "taskbotActions": [
            {
                "id": "84a392eb-d408-41b8-9e11-0a1f1f353003",
                "taskbotVersionId": "20beec90-744c-4c76-961a-0917006760d7",
                "xPosition": 1211,
                "yPosition": 859,
                "type": "taskbotSendMessage",
                "taskbotSendMessage": {
                    "taskbotActionId": "84a392eb-d408-41b8-9e11-0a1f1f353003",
                    "typingDelay": 1,
                    "message": "data:text/plain;base64,WiBpcyBoYW5kbGVkIGJ5IG91ciBjdXN0b21lciBzZXJ2aWNlIHRlYW0gZGlyZWN0bHksIGxldCBtZSB0cmFuc2ZlciB5b3UuIPCfmIo=",
                    "nextActionId": "f983c94b-a58e-44d9-8155-cb6102d69e8f",
                    "taskbotSendMessageButtons": [],
                },
            },
            {
                "id": "c7a14b7f-ce45-4624-94c3-2b8261ec2409",
                "taskbotVersionId": "20beec90-744c-4c76-961a-0917006760d7",
                "xPosition": 2670,
                "yPosition": 290,
                "type": "taskbotCollectName",
                "taskbotCollectName": {
                    "taskbotActionId": "c7a14b7f-ce45-4624-94c3-2b8261ec2409",
                    "typingDelay": 1,
                    "message": "data:text/plain;base64,T2theSBJIGp1c3QgbmVlZCBzb21lIGluZm8gZnJvbSB5b3UuIFdoYXQncyB5b3VyIG5hbWU/",
                    "nextActionId": "93b23087-275c-4549-b974-59ee93a6899c",
                },
            },
            {
                "id": "aaee606d-9d9e-443b-b91a-4734b2c004f4",
                "taskbotVersionId": "20beec90-744c-4c76-961a-0917006760d7",
                "xPosition": 2310,
                "yPosition": 290,
                "type": "taskbotQuickReply",
                "taskbotQuickReply": {
                    "taskbotActionId": "aaee606d-9d9e-443b-b91a-4734b2c004f4",
                    "typingDelay": 1,
                    "message": "data:text/plain;base64,SSdtIHNvcnJ5IPCfmJQsIG5vIG9uZSBpcyBvbmxpbmUgcmlnaHQgbm93LCB3b3VsZCB5b3UgbGlrZSB0byBsZWF2ZSBhIG1lc3NhZ2UgZm9yIG91ciBzYWxlcyB0ZWFtPw==",
                    "otherResponseToActionId": "00000000-0000-0000-0000-000000000000",
                    "taskbotQuickReplyOptions": [
                        {
                            "id": "ce49a3ae-a964-4617-b473-d1865d44bc14",
                            "taskbotActionId": "aaee606d-9d9e-443b-b91a-4734b2c004f4",
                            "text": "Yes",
                            "order": 0,
                            "nextActionId": "c7a14b7f-ce45-4624-94c3-2b8261ec2409",
                        },
                        {
                            "id": "84204193-60ce-4306-a092-5abb3b9d1336",
                            "taskbotActionId": "aaee606d-9d9e-443b-b91a-4734b2c004f4",
                            "text": "No",
                            "order": 1,
                            "nextActionId": "695bb7be-0293-42b7-b68b-74b129ac67b5",
                        },
                    ],
                },
            },
            {
                "id": "4097561c-ed9b-4ef6-873d-486734557adf",
                "taskbotVersionId": "20beec90-744c-4c76-961a-0917006760d7",
                "xPosition": 1211,
                "yPosition": 630,
                "type": "taskbotSendMessage",
                "taskbotSendMessage": {
                    "taskbotActionId": "4097561c-ed9b-4ef6-873d-486734557adf",
                    "typingDelay": 1,
                    "message": "data:text/plain;base64,WW91IGNhbiBsZWFybiBtb3JlIGFib3V0IFkgYnkgY2xpY2tpbmcgdGhlIGxpbmsgYmVsb3c6",
                    "nextActionId": "22730214-883d-41e2-834b-9d83f808c9fd",
                    "taskbotSendMessageButtons": [
                        {
                            "id": "ce1fd375-eeb4-475b-b842-d85c358afa9f",
                            "taskbotActionId": "4097561c-ed9b-4ef6-873d-486734557adf",
                            "buttonText": "Learn more",
                            "type": "link",
                            "url": "https://www.comm100.com",
                            "openIn": "sideWindow",
                            "openStyle": "tall",
                            "order": 0,
                        }
                    ],
                },
            },
            {
                "id": "1400373d-4ddd-48ea-918c-50c0c19c6f0f",
                "taskbotVersionId": "20beec90-744c-4c76-961a-0917006760d7",
                "xPosition": 871,
                "yPosition": 294,
                "type": "taskbotSendVideo",
                "taskbotSendVideo": {
                    "taskbotActionId": "1400373d-4ddd-48ea-918c-50c0c19c6f0f",
                    "typingDelay": 1,
                    "message": "data:text/plain;base64,SGVyZSBpcyBhIGhvdyB0byB2aWRlbyBvbiBob3cgdG8gZG8gWDo=",
                    "videoUrl": "https://www.youtube.com/watch?v=wMaST-4dPMs",
                    "nextActionId": "22730214-883d-41e2-834b-9d83f808c9fd",
                },
            },
            {
                "id": "fedc9158-8cb7-4055-8eea-5130a160e8c5",
                "taskbotVersionId": "20beec90-744c-4c76-961a-0917006760d7",
                "xPosition": 510,
                "yPosition": 50,
                "type": "taskbotQuickReply",
                "taskbotQuickReply": {
                    "taskbotActionId": "fedc9158-8cb7-4055-8eea-5130a160e8c5",
                    "typingDelay": 1,
                    "message": "data:text/plain;base64,UGxlYXNlIHNlbGVjdCBvbmUgb2YgdGhlIG9wdGlvbnMgYmVsb3cgdG8gZ2V0IHN0YXJ0ZWQ6",
                    "otherResponseToActionId": "00000000-0000-0000-0000-000000000000",
                    "taskbotQuickReplyOptions": [
                        {
                            "id": "ac8d55e2-9fb3-4178-996b-8c8d824599e5",
                            "taskbotActionId": "fedc9158-8cb7-4055-8eea-5130a160e8c5",
                            "text": "#1 FAQ - What is your policy on X?",
                            "order": 0,
                            "nextActionId": "9817e8c5-b09e-4fad-88c5-5c4dabac0d13",
                        },
                        {
                            "id": "32aa1b10-f58d-43cc-9d3e-7269c0c1a054",
                            "taskbotActionId": "fedc9158-8cb7-4055-8eea-5130a160e8c5",
                            "text": "#2 FAQ - How do I do X?",
                            "order": 1,
                            "nextActionId": "1400373d-4ddd-48ea-918c-50c0c19c6f0f",
                        },
                        {
                            "id": "18846521-012e-4f78-93c2-ea82d4f89838",
                            "taskbotActionId": "fedc9158-8cb7-4055-8eea-5130a160e8c5",
                            "text": "#3 FAQ - My X isn't working, how do I fix it?",
                            "order": 2,
                            "nextActionId": "a90f544c-00eb-4904-bcea-dfd918af63a2",
                        },
                        {
                            "id": "10f00167-dc32-49fb-aea1-dcb09af119be",
                            "taskbotActionId": "fedc9158-8cb7-4055-8eea-5130a160e8c5",
                            "text": "Talk to an Agent",
                            "order": 3,
                            "nextActionId": "f983c94b-a58e-44d9-8155-cb6102d69e8f",
                        },
                    ],
                },
            },
            {
                "id": "5adf4c43-2857-4a4e-a5b4-5137e62da235",
                "taskbotVersionId": "20beec90-744c-4c76-961a-0917006760d7",
                "xPosition": 1590,
                "yPosition": 50,
                "type": "taskbotSendMessage",
                "taskbotSendMessage": {
                    "taskbotActionId": "5adf4c43-2857-4a4e-a5b4-5137e62da235",
                    "typingDelay": 1,
                    "message": "data:text/plain;base64,VGhhdCdzIGdyZWF0LiBDb21lIGJhY2sgYW5kIGNoYXQgd2l0aCBtZSBhbnl0aW1lIHlvdSBsaWtlISDwn5iK",
                    "nextActionId": "00000000-0000-0000-0000-000000000000",
                    "taskbotSendMessageButtons": [],
                },
            },
            {
                "id": "93b23087-275c-4549-b974-59ee93a6899c",
                "taskbotVersionId": "20beec90-744c-4c76-961a-0917006760d7",
                "xPosition": 3030,
                "yPosition": 290,
                "type": "taskbotCollectEmail",
                "taskbotCollectEmail": {
                    "taskbotActionId": "93b23087-275c-4549-b974-59ee93a6899c",
                    "typingDelay": 1,
                    "message": "data:text/plain;base64,SGkgeyFOYW1lfSEgV2hhdCdzIHlvdXIgZW1haWw/",
                    "nextActionId": "f43fa9ce-8f93-4095-b178-c1c44698e907",
                },
            },
            {
                "id": "9817e8c5-b09e-4fad-88c5-5c4dabac0d13",
                "taskbotVersionId": "20beec90-744c-4c76-961a-0917006760d7",
                "xPosition": 870,
                "yPosition": 50,
                "type": "taskbotSendMessage",
                "taskbotSendMessage": {
                    "taskbotActionId": "9817e8c5-b09e-4fad-88c5-5c4dabac0d13",
                    "typingDelay": 1,
                    "message": "data:text/plain;base64,WW91IGNhbiBsZWFybiBhYm91dCBvdXIgWCBwb2xpY3kgYnkgY2xpY2tpbmcgdGhlIGJ1dHRvbiBiZWxvdzo=",
                    "nextActionId": "22730214-883d-41e2-834b-9d83f808c9fd",
                    "taskbotSendMessageButtons": [
                        {
                            "id": "91a909c4-351e-496e-b4d0-bd8d228cc97e",
                            "taskbotActionId": "9817e8c5-b09e-4fad-88c5-5c4dabac0d13",
                            "buttonText": "Learn more",
                            "type": "link",
                            "url": "https://www.comm100.com",
                            "openIn": "sideWindow",
                            "openStyle": "tall",
                            "order": 0,
                        }
                    ],
                },
            },
            {
                "id": "9e894631-6e39-4f64-b9a0-69958a1eca59",
                "taskbotVersionId": "20beec90-744c-4c76-961a-0917006760d7",
                "xPosition": 150,
                "yPosition": 50,
                "type": "taskbotSendMessage",
                "taskbotSendMessage": {
                    "taskbotActionId": "9e894631-6e39-4f64-b9a0-69958a1eca59",
                    "typingDelay": 1,
                    "message": "data:text/plain;base64,8J+RiyBIaSB0aGVyZSwgSSBhbSBhbiBGQVEgYm90IGRlc2lnbmVkIHRvIHJlc29sdmUgY29tbW9uIGN1c3RvbWVyIHF1ZXN0aW9ucy4g8J+klg==",
                    "nextActionId": "fedc9158-8cb7-4055-8eea-5130a160e8c5",
                    "taskbotSendMessageButtons": [],
                },
            },
            {
                "id": "695bb7be-0293-42b7-b68b-74b129ac67b5",
                "taskbotVersionId": "20beec90-744c-4c76-961a-0917006760d7",
                "xPosition": 2670,
                "yPosition": 544,
                "type": "taskbotSendMessage",
                "taskbotSendMessage": {
                    "taskbotActionId": "695bb7be-0293-42b7-b68b-74b129ac67b5",
                    "typingDelay": 1,
                    "message": "data:text/plain;base64,T2theSwgbGV0IG1lIGtub3cgaWYgeW91IG5lZWQgYW55IGhlbHAhIEknbSBhbHdheXMgaGVyZSB0byBoZWxwIPCfmIo=",
                    "nextActionId": "00000000-0000-0000-0000-000000000000",
                    "taskbotSendMessageButtons": [],
                },
            },
            {
                "id": "ec146dfb-fb76-4ac8-b98f-8f66da175c50",
                "taskbotVersionId": "20beec90-744c-4c76-961a-0917006760d7",
                "xPosition": 3750,
                "yPosition": 290,
                "type": "taskbotSendMessage",
                "taskbotSendMessage": {
                    "taskbotActionId": "ec146dfb-fb76-4ac8-b98f-8f66da175c50",
                    "typingDelay": 1,
                    "message": "data:text/plain;base64,T2theSwgb3VyIGN1c3RvbWVyIHNlcnZpY2UgdGVhbSB3aWxsIGdldCBiYWNrIHRvIHlvdSBpbiB0aGUgbmV4dCAyNCBob3Vycy4gVGhhbmtzIGZvciB0aGUgY2hhdCE=",
                    "nextActionId": "00000000-0000-0000-0000-000000000000",
                    "taskbotSendMessageButtons": [],
                },
            },
            {
                "id": "22730214-883d-41e2-834b-9d83f808c9fd",
                "taskbotVersionId": "20beec90-744c-4c76-961a-0917006760d7",
                "xPosition": 1230,
                "yPosition": 50,
                "type": "taskbotQuickReply",
                "taskbotQuickReply": {
                    "taskbotActionId": "22730214-883d-41e2-834b-9d83f808c9fd",
                    "typingDelay": 1,
                    "message": "data:text/plain;base64,V2FzIHRoYXQgaGVscGZ1bD8=",
                    "otherResponseToActionId": "00000000-0000-0000-0000-000000000000",
                    "taskbotQuickReplyOptions": [
                        {
                            "id": "7f3da2b4-c79d-4d1e-acf0-2c6ce60b252e",
                            "taskbotActionId": "22730214-883d-41e2-834b-9d83f808c9fd",
                            "text": "Yes",
                            "order": 0,
                            "nextActionId": "5adf4c43-2857-4a4e-a5b4-5137e62da235",
                        },
                        {
                            "id": "5f3367eb-a497-4357-b644-cfc6c4342286",
                            "taskbotActionId": "22730214-883d-41e2-834b-9d83f808c9fd",
                            "text": "No",
                            "order": 1,
                            "nextActionId": "8701ddb7-ef5a-4308-937f-f06cd155ac1c",
                        },
                    ],
                },
            },
            {
                "id": "f43fa9ce-8f93-4095-b178-c1c44698e907",
                "taskbotVersionId": "20beec90-744c-4c76-961a-0917006760d7",
                "xPosition": 3390,
                "yPosition": 290,
                "type": "taskbotCollectComment",
                "taskbotCollectComment": {
                    "taskbotActionId": "f43fa9ce-8f93-4095-b178-c1c44698e907",
                    "typingDelay": 1,
                    "message": "data:text/plain;base64,SXMgdGhlcmUgYSBtZXNzYWdlIHlvdSdkIGxpa2UgdG8gcGFzcyBvbiB0byBvdXIgdGVhbT8=",
                    "nextActionId": "ec146dfb-fb76-4ac8-b98f-8f66da175c50",
                },
            },
            {
                "id": "f983c94b-a58e-44d9-8155-cb6102d69e8f",
                "taskbotVersionId": "20beec90-744c-4c76-961a-0917006760d7",
                "xPosition": 1964,
                "yPosition": 281,
                "type": "taskbotTransferChat",
                "taskbotTransferChat": {
                    "taskbotActionId": "f983c94b-a58e-44d9-8155-cb6102d69e8f",
                    "type": "transferToAgent",
                    "transferTo": "6467a021-a043-4c13-85af-ce6ee3919ba3",
                    "whenAgentOfflineToActionId": "aaee606d-9d9e-443b-b91a-4734b2c004f4",
                },
            },
            {
                "id": "4e8b99bb-2b58-44b6-9622-d626a4c7ca72",
                "taskbotVersionId": "20beec90-744c-4c76-961a-0917006760d7",
                "xPosition": 24,
                "yPosition": 50,
                "type": "taskbotStart",
                "taskbotStart": {
                    "taskbotActionId": "4e8b99bb-2b58-44b6-9622-d626a4c7ca72",
                    "nextActionId": "9e894631-6e39-4f64-b9a0-69958a1eca59",
                },
            },
            {
                "id": "a90f544c-00eb-4904-bcea-dfd918af63a2",
                "taskbotVersionId": "20beec90-744c-4c76-961a-0917006760d7",
                "xPosition": 873,
                "yPosition": 658,
                "type": "taskbotQuickReply",
                "taskbotQuickReply": {
                    "taskbotActionId": "a90f544c-00eb-4904-bcea-dfd918af63a2",
                    "typingDelay": 1,
                    "message": "data:text/plain;base64,V2hhdCB0eXBlIG9mIFggZG8geW91IGhhdmU/",
                    "otherResponseToActionId": "00000000-0000-0000-0000-000000000000",
                    "taskbotQuickReplyOptions": [
                        {
                            "id": "7d0f1d75-2f40-4747-9513-9f23ae3fc93f",
                            "taskbotActionId": "a90f544c-00eb-4904-bcea-dfd918af63a2",
                            "text": "I have Y type",
                            "order": 0,
                            "nextActionId": "4097561c-ed9b-4ef6-873d-486734557adf",
                        },
                        {
                            "id": "41e01207-85d8-4f91-9e05-c94a7c09ecb0",
                            "taskbotActionId": "a90f544c-00eb-4904-bcea-dfd918af63a2",
                            "text": "I have Z type",
                            "order": 1,
                            "nextActionId": "84a392eb-d408-41b8-9e11-0a1f1f353003",
                        },
                    ],
                },
            },
            {
                "id": "8701ddb7-ef5a-4308-937f-f06cd155ac1c",
                "taskbotVersionId": "20beec90-744c-4c76-961a-0917006760d7",
                "xPosition": 1590,
                "yPosition": 290,
                "type": "taskbotSendMessage",
                "taskbotSendMessage": {
                    "taskbotActionId": "8701ddb7-ef5a-4308-937f-f06cd155ac1c",
                    "typingDelay": 1,
                    "message": "data:text/plain;base64,VGhhdCdzIGEgc2hhbWUg8J+YlCwgbGV0IG1lIHRyYW5zZmVyIHlvdSB0byBhIG1lbWJlciBvZiBvdXIgY3VzdG9tZXIgc2VydmljZSB0ZWFtLg==",
                    "nextActionId": "f983c94b-a58e-44d9-8155-cb6102d69e8f",
                    "taskbotSendMessageButtons": [],
                },
            },
        ],
        "taskbotId": task_bot_id,
        "createdTime": "2024/03/08 16:05:55",
    }

    res = send_request(
        req_url,
        None,
        "POST",
        None,
        login["common_headers"],
        req_body,
    )
    # pdb.set_trace()
    assert res.status_code == 200, (
        "Failed with status code: "
        + str(res.status_code)
        + " and response: "
        + str(res.json())
    )
    logger.info("\n ======= task bot has been initialized and ready to use. =======")
    yield res


@pytest.fixture(scope="session")
def get_root_intent_category(login, create_keyword_chatbot):
    chatbot_id = create_keyword_chatbot.json()["id"]

    req_url = login["api_url"] + "/bot/chatbotIntentCategories"

    res = send_request(
        req_url,
        {"chatbotId": chatbot_id},
        "GET",
        None,
        login["common_headers"],
        None,
    )
    # pdb.set_trace()
    assert res.status_code == 200, (
        "Failed with status code: "
        + str(res.status_code)
        + " and response: "
        + str(res.json())
    )
    logger.info("\n ======= intent root category has been retrieved =======")
    yield res


@pytest.fixture(scope="session")
def create_intent_pizza_order(login, get_root_intent_category):
    category_id = get_root_intent_category.json()[0]["id"]

    chatbot_action_start_id = str(uuid.uuid4())
    chatbot_action_send_message_id = str(uuid.uuid4())

    req_url = login["api_url"] + "/chatbot/chatbotIntents"
    req_body = {
        "name": "temp pizza order intent",
        "chatbotIntentCategoryId": category_id,
        "chatbotIntentAnswers": [
            {
                "channelId": "Live Chat",
                "chatbotResponse": {
                    "chatbotActions": [
                        {
                            "id": chatbot_action_start_id,
                            "xPosition": 24,
                            "yPosition": 50,
                            "type": "chatbotActionStart",
                            "chatbotActionStart": {
                                "nextActionId": chatbot_action_send_message_id
                            },
                        },
                        {
                            "id": chatbot_action_send_message_id,
                            "xPosition": 154,
                            "yPosition": 62,
                            "type": "chatbotActionSendMessage",
                            "chatbotActionSendMessage": {
                                "typingDelay": 0,  # change this to no delay
                                "message": "what kind of pizza - flavor, size, toppings?",
                                "nextActionId": "00000000-0000-0000-0000-000000000000",
                                "variants": None,
                                "chatbotActionSendMessageLinks": [],
                            },
                            "isError": False,
                            "extendData": {
                                "actionTitle": True,
                                "links": True,
                                "linkTo": True,
                                "defaultOpenIn": "sideWindow",
                                "defaultLinkToType": "webview",
                                "htmlInput": {"dynamicInfo": True},
                                "maxLinkCount": 10,
                            },
                        },
                    ]
                },
            }
        ],
        "chatbotIntentPrompts": [],
        "chatbotIntentQuestions": [
            {
                "key": 1,
                "content": "I want to buy a pizza",
                "order": 0,
                "chatbotIntentQuestionKeywords": [],
            }
        ],
    }

    res = send_request(
        req_url,
        None,
        "POST",
        None,
        login["common_headers"],
        req_body,
    )

    # pdb.set_trace()
    assert res.status_code == 201, (
        "Failed with status code: "
        + str(res.status_code)
        + " and response: "
        + str(res.json())
    )
    logger.info("\n ======= intent pizza order has been created =======")
    yield res

    created_id = res.json()["id"]
    req_url_delete = login["api_url"] + "/chatbot/chatbotIntents/" + created_id
    res_delete = send_request(
        req_url_delete,
        None,
        "DELETE",
        None,
        login["common_headers"],
        None,
    )
    assert res_delete.status_code == 204, (
        "Failed with status code: "
        + str(res_delete.status_code)
        + " and response: "
        + str(res_delete.json())
    )
    logger.info("\n ======= newly-created intent pizza order has been deleted =======")


@pytest.fixture(scope="session")
def create_intent_send_form(login, get_root_intent_category):
    category_id = get_root_intent_category.json()[0]["id"]

    chatbot_action_start_id = str(uuid.uuid4())
    chatbot_action_send_form_id = str(uuid.uuid4())

    req_url = login["api_url"] + "/chatbot/chatbotIntents"
    req_body = {
        "name": "temp send form intent",
        "chatbotIntentCategoryId": category_id,
        "chatbotIntentAnswers": [
            {
                "channelId": "Live Chat",
                "chatbotResponse": {
                    "chatbotActions": [
                        {
                            "id": chatbot_action_start_id,
                            "xPosition": 24,
                            "yPosition": 50,
                            "type": "chatbotActionStart",
                            "chatbotActionStart": {
                                "nextActionId": chatbot_action_send_form_id
                            },
                        },
                        {
                            "id": chatbot_action_send_form_id,
                            "xPosition": 154,
                            "yPosition": 62,
                            "type": "chatbotActionSendForm",
                            "chatbotActionSendForm": {
                                "typingDelay": 0,
                                "title": "temp form",
                                "message": "Can you please submit this form?",
                                "isConfirmationRequired": False,
                                "isInputAreaEnabled": False,
                                "nextActionId": "00000000-0000-0000-0000-000000000000",
                                "submitButtonText": "Submit",
                                "cancelButtonText": "Cancel",
                                "confirmButtonText": "Confirm",
                                "chatbotActionSendFormFields": [
                                    {
                                        "name": "Name",
                                        "isRequired": True,
                                        "isMasked": False,
                                        "type": "text",
                                        "variableName": "Name",
                                        "order": 0,
                                        "options": [],
                                    },
                                    {
                                        "name": "Email",
                                        "isRequired": True,
                                        "isMasked": False,
                                        "type": "email",
                                        "variableName": "Email",
                                        "order": 1,
                                        "options": [],
                                    },
                                ],
                                "successedActionId": "00000000-0000-0000-0000-000000000000",
                                "failedActionId": "00000000-0000-0000-0000-000000000000",
                                "formSource": "setUpAForm",
                                "formPageUrl": "",
                            },
                            "extendData": "",
                        },
                    ]
                },
            }
        ],
        "chatbotIntentPrompts": [],
        "chatbotIntentQuestions": [
            {
                "key": 1,
                "content": "send form",
                "order": 0,
                "chatbotIntentQuestionKeywords": [],
            }
        ],
    }

    res = send_request(
        req_url,
        None,
        "POST",
        None,
        login["common_headers"],
        req_body,
    )

    # pdb.set_trace()
    assert res.status_code == 201, (
        "Failed with status code: "
        + str(res.status_code)
        + " and response: "
        + str(res.json())
    )
    logger.info("\n ======= intent send form has been created =======")
    yield res

    created_id = res.json()["id"]
    req_url_delete = login["api_url"] + "/chatbot/chatbotIntents/" + created_id
    res_delete = send_request(
        req_url_delete,
        None,
        "DELETE",
        None,
        login["common_headers"],
        None,
    )

    # pdb.set_trace()
    assert res_delete.status_code == 204, (
        "Failed with status code: "
        + str(res_delete.status_code)
        + " and response: "
        + str(res_delete.json())
    )
    logger.info("\n ======= newly-created intent send form has been deleted =======")


@pytest.fixture(scope="session")
def get_event_message_when_visitor_starts_chat(login, create_keyword_chatbot):
    chatbot_id = create_keyword_chatbot.json()["id"]

    req_url = login["api_url"] + "/bot/chatbotMessagesWhenAVisitorStartAChat"

    res = send_request(
        req_url,
        {"chatbotId": chatbot_id},
        "GET",
        None,
        login["common_headers"],
        None,
    )

    # pdb.set_trace()
    assert res.status_code == 200, (
        "Failed with status code: "
        + str(res.status_code)
        + " and response: "
        + str(res.json())
    )
    logger.info(
        "\n ======= event_message_when_visitor_starts_chat has been retrieved ======="
    )
    yield res


@pytest.fixture(scope="module")
def update_event_message_when_visitor_starts_chat_add_link_to_intent_pizza_order(
    login,
    create_keyword_chatbot,
    create_intent_pizza_order,
    get_event_message_when_visitor_starts_chat,
):
    """update the event message when visitor starts chat by adding a link to the pizza order intent. When visitor clicks the buy pizza link, action 'chatBotSelectQuestion' is generated."""

    # prepare the data
    chatbot_id = create_keyword_chatbot.json()["id"]
    intent_id = create_intent_pizza_order.json()["id"]
    event_message = get_event_message_when_visitor_starts_chat.json()[0]
    event_message_id = event_message["id"]
    chatbot_response_id = event_message["chatbotResponseId"]
    chatbot_action_send_message_id = event_message["chatbotResponse"]["chatbotActions"][
        0
    ]["id"]
    chatbot_action_start_id = event_message["chatbotResponse"]["chatbotActions"][1][
        "id"
    ]

    # update the event message
    req_url = (
        login["api_url"]
        + "/bot/chatbotMessagesWhenAVisitorStartAChat/"
        + event_message_id
    )
    req_body = {
        "id": event_message_id,
        "chatbotId": chatbot_id,
        "chatbotResponseId": chatbot_response_id,
        "channelId": "Live Chat",
        "chatbotResponse": {
            "id": chatbot_response_id,
            "chatbotActions": [
                {
                    "id": chatbot_action_send_message_id,
                    "xPosition": 150,
                    "yPosition": 50,
                    "type": "chatbotActionSendMessage",
                    "chatbotActionSendMessage": {
                        "nextActionId": "00000000-0000-0000-0000-000000000000",
                        "typingDelay": 0,  # change this to no delay
                        "message": "Hi there! I'm a chatbot, here to help answer your questions.",
                        "variants": None,
                        "chatbotActionId": chatbot_action_send_message_id,
                        "chatbotActionSendMessageLinks": [
                            {
                                "buttonText": "buy pizza",
                                "type": "intent",
                                "url": "",
                                "openIn": "sideWindow",
                                "openStyle": "full",
                                "order": 0,
                                "intentId": intent_id,
                                "id": str(uuid.uuid4()),
                            }
                        ],
                    },
                    "isError": False,
                    "extendData": {
                        "actionTitle": True,
                        "links": True,
                        "linkTo": True,
                        "defaultOpenIn": "sideWindow",
                        "defaultLinkToType": "webview",
                        "htmlInput": {"dynamicInfo": True},
                        "maxLinkCount": 10,
                    },
                },
                {
                    "id": chatbot_action_start_id,
                    "xPosition": 24,
                    "yPosition": 50,
                    "type": "chatbotActionStart",
                    "chatbotActionStart": {
                        "nextActionId": chatbot_action_send_message_id,
                        "chatbotActionId": chatbot_action_start_id,
                    },
                    "extendData": None,
                },
            ],
        },
    }

    res = send_request(
        req_url,
        None,
        "PUT",
        None,
        login["common_headers"],
        req_body,
    )

    # pdb.set_trace()
    assert res.status_code == 200, (
        "Failed with status code: "
        + str(res.status_code)
        + " and response: "
        + str(res.json())
    )
    logger.info(
        "\n ======= update event_message_when_visitor_starts_chat with adding link to intent buy pizza succeeded. ======="
    )
    yield res


@pytest.fixture(scope="module")
def update_event_message_when_visitor_starts_chat_add_link_to_intent_send_form(
    login,
    create_keyword_chatbot,
    create_intent_send_form,
    get_event_message_when_visitor_starts_chat,
):
    """update the event message when visitor starts chat by adding a link to the send form intent. Then visitor can trigger visitorHandleBotForm action."""

    # prepare the data
    chatbot_id = create_keyword_chatbot.json()["id"]
    intent_id = create_intent_send_form.json()["id"]
    event_message = get_event_message_when_visitor_starts_chat.json()[0]
    event_message_id = event_message["id"]
    chatbot_response_id = event_message["chatbotResponseId"]
    chatbot_action_send_form_id = event_message["chatbotResponse"]["chatbotActions"][0][
        "id"
    ]
    chatbot_action_start_id = event_message["chatbotResponse"]["chatbotActions"][1][
        "id"
    ]

    # update the event message
    req_url = (
        login["api_url"]
        + "/bot/chatbotMessagesWhenAVisitorStartAChat/"
        + event_message_id
    )
    req_body = {
        "id": event_message_id,
        "chatbotId": chatbot_id,
        "chatbotResponseId": chatbot_response_id,
        "channelId": "Live Chat",
        "chatbotResponse": {
            "id": chatbot_response_id,
            "chatbotActions": [
                {
                    "id": chatbot_action_send_form_id,
                    "xPosition": 150,
                    "yPosition": 50,
                    "type": "chatbotActionSendMessage",
                    "chatbotActionSendMessage": {
                        "nextActionId": "00000000-0000-0000-0000-000000000000",
                        "typingDelay": 0,  # change this to no delay
                        "message": "Hi there! I'm a chatbot, here to help answer your questions.",
                        "variants": None,
                        "chatbotActionId": chatbot_action_send_form_id,
                        "chatbotActionSendMessageLinks": [
                            {
                                "buttonText": "send form",
                                "type": "intent",
                                "url": "",
                                "openIn": "sideWindow",
                                "openStyle": "full",
                                "order": 0,
                                "intentId": intent_id,
                                "id": str(uuid.uuid4()),
                            }
                        ],
                    },
                    "isError": False,
                    "extendData": {
                        "actionTitle": True,
                        "links": True,
                        "linkTo": True,
                        "defaultOpenIn": "sideWindow",
                        "defaultLinkToType": "webview",
                        "htmlInput": {"dynamicInfo": True},
                        "maxLinkCount": 10,
                    },
                },
                {
                    "id": chatbot_action_start_id,
                    "xPosition": 24,
                    "yPosition": 50,
                    "type": "chatbotActionStart",
                    "chatbotActionStart": {
                        "nextActionId": chatbot_action_send_form_id,
                        "chatbotActionId": chatbot_action_start_id,
                    },
                    "extendData": None,
                },
            ],
        },
    }

    res = send_request(
        req_url,
        None,
        "PUT",
        None,
        login["common_headers"],
        req_body,
    )

    # pdb.set_trace()
    assert res.status_code == 200, (
        "Failed with status code: "
        + str(res.status_code)
        + " and response: "
        + str(res.json())
    )
    logger.info(
        "\n ======= update event_message_when_visitor_starts_chat with adding link to intent send form succeeded. ======="
    )
    yield res

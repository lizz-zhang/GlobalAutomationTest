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
def generate_visitor_chatting_with_chatbot(
    update_campaign_enable_chatbot,  # need to make sure chatbot is enabled
    generate_visitor_no_pre_chat_system_processing,
    visitor_request_chat,
    visitor_end_chat_solo_action,
    save_and_delete_chat,
):
    (
        res_new_visitor,
        res_request_chat,
        visitor_ashx_url,
        visitor_guid,
        visitor_session_id,
        campaign_id,
        chat_guid,
    ) = visitor_request_chat

    logger.info("\n ======= Now we have a visitor chatting with chatbot. =======")

    # pdb.set_trace()
    yield (
        res_new_visitor,
        res_request_chat,
        visitor_ashx_url,
        visitor_guid,
        visitor_session_id,
        campaign_id,
        chat_guid,
    )

    # teardown part: 需要结束聊天，并确保聊天最后被删除

    visitor_end_chat_solo_action(chat_guid)
    # pdb.set_trace()
    save_and_delete_chat(chat_guid)


@pytest.fixture(scope="function")
def generate_visitor_got_initial_messages_with_chatbot(
    generate_visitor_chatting_with_chatbot,
    visitor_get_initial_messages_solo_action,
    visitor_end_chat_solo_action,
    save_and_delete_chat,
):
    (
        res_get_initial_messages,
        res_new_visitor,
        visitor_ashx_url,
        visitor_guid,
        visitor_session_id,
        campaign_id,
        chat_guid,
        visitor_chat_version,
        visitor_chat_version_from_id,
    ) = visitor_get_initial_messages_solo_action

    # pdb.set_trace()
    logger.info(
        "\n ======= Now we have a visitor who has got initial messages with chatbot. ======="
    )

    yield (
        res_get_initial_messages,
        res_new_visitor,
        visitor_ashx_url,
        visitor_guid,
        visitor_session_id,
        campaign_id,
        chat_guid,
        visitor_chat_version,
        visitor_chat_version_from_id,
    )

    # teardown part: 需要结束聊天，并确保聊天最后被删除

    visitor_end_chat_solo_action(chat_guid)
    # pdb.set_trace()
    save_and_delete_chat(chat_guid)


@pytest.fixture(scope="function")
def generate_visitor_got_chatbot_select_question_pizza_order_message(
    create_intent_pizza_order,
    update_event_message_when_visitor_starts_chat_add_link_to_intent_pizza_order,
    generate_visitor_got_initial_messages_with_chatbot,
):
    """在访客选择了chatbot发出来的buy pizza问题之后，访客发了一次getChatMessages请求，把选择的buy pizza这条消息已经拿下来了。如果后续用例来调用这个fixture，然后再getChatMessages的时候，应该要收到chatbot发过来pizza order这个intent发的消息。"""

    intent_id = create_intent_pizza_order.json()["id"]

    (
        res_get_initial_messages,
        res_new_visitor,
        visitor_ashx_url,
        visitor_guid,
        visitor_session_id,
        campaign_id,
        chat_guid,
        visitor_chat_version,
        visitor_chat_version_from_id,
    ) = generate_visitor_got_initial_messages_with_chatbot

    req_body = [
        {
            "type": "batchAction",
            "actions": [
                {
                    "type": "chatBotSelectQuestion",
                    "chatGuid": chat_guid,
                    "question": {
                        "questionId": intent_id,
                        "questionName": "buy pizza",
                    },
                    "clickType": 1,
                    "botId": "00000000-0000-0000-0000-000000000000",
                    "senderType": 3,
                    "chatVersion": visitor_chat_version,
                    "sessionId": visitor_session_id,
                },
                {
                    "type": "getChatMessages",
                    "chatGuid": chat_guid,
                    "fromId": visitor_chat_version_from_id,
                    "chatVersion": visitor_chat_version,
                    "sessionId": visitor_session_id,
                },
                {
                    "type": "visitorGetLatestMsgSeen",
                    "chatGuid": chat_guid,
                    "chatVersion": visitor_chat_version,
                    "sessionId": visitor_session_id,
                },
            ],
            "ssoSessionToken": "",
            "id": 31,
        },
    ]

    # pdb.set_trace()
    res = send_request(
        visitor_ashx_url,
        None,
        "POST",
        None,
        None,
        req_body,
    )

    # pdb.set_trace()
    assert res.status_code == 200, (
        "Failed with status code: "
        + str(res.status_code)
        + " and response: "
        + str(res.json())
    )
    assert (
        res.json()[0]["payload"][0]["type"] == "chatBotSelectQuestion"
    ), "Failed with response: " + str(res.json())
    assert (
        res.json()[0]["payload"][1]["payload"][-1]["type"] == "visitorAddTextMessage"
    ), "Failed with response: " + str(res.json())
    logger.info(
        "\n ======= Now we have a visitor who has got the 'buy pizza' message. ======="
    )

    visitor_chat_version = res.json()[0]["payload"][1]["payload"][-1]["guid"]
    visitor_chat_version_from_id = res.json()[0]["payload"][1]["payload"][-1]["id"]
    res_got_chatbot_select_question_message = res
    sleep(
        2
    )  # make sure the chatbot has enough time to respond to the visitor's message
    yield (
        res_got_chatbot_select_question_message,
        res_new_visitor,
        visitor_ashx_url,
        visitor_guid,
        visitor_session_id,
        campaign_id,
        chat_guid,
        visitor_chat_version,
        visitor_chat_version_from_id,
        intent_id,
    )


@pytest.fixture(scope="function")
def generate_visitor_got_chatbot_select_question_send_form_message(
    create_intent_send_form,
    update_event_message_when_visitor_starts_chat_add_link_to_intent_send_form,
    generate_visitor_got_initial_messages_with_chatbot,
):
    """在访客选择了chatbot发出来的send form问题之后，访客发了一次getChatMessages请求，把选择的send form这条消息已经拿下来了。如果后续用例来调用这个fixture，然后再getChatMessages的时候，应该要收到chatbot发过来send form这个intent发的消息。"""

    intent_id = create_intent_send_form.json()["id"]

    (
        res_get_initial_messages,
        res_new_visitor,
        visitor_ashx_url,
        visitor_guid,
        visitor_session_id,
        campaign_id,
        chat_guid,
        visitor_chat_version,
        visitor_chat_version_from_id,
    ) = generate_visitor_got_initial_messages_with_chatbot

    req_body = [
        {
            "type": "batchAction",
            "actions": [
                {
                    "type": "chatBotSelectQuestion",
                    "chatGuid": chat_guid,
                    "question": {
                        "questionId": intent_id,
                        "questionName": "send form",
                    },
                    "clickType": 1,
                    "botId": "00000000-0000-0000-0000-000000000000",
                    "senderType": 3,
                    "chatVersion": visitor_chat_version,
                    "sessionId": visitor_session_id,
                },
                {
                    "type": "getChatMessages",
                    "chatGuid": chat_guid,
                    "fromId": visitor_chat_version_from_id,
                    "chatVersion": visitor_chat_version,
                    "sessionId": visitor_session_id,
                },
                {
                    "type": "visitorGetLatestMsgSeen",
                    "chatGuid": chat_guid,
                    "chatVersion": visitor_chat_version,
                    "sessionId": visitor_session_id,
                },
            ],
            "ssoSessionToken": "",
            "id": 31,
        },
    ]

    # pdb.set_trace()
    res = send_request(
        visitor_ashx_url,
        None,
        "POST",
        None,
        None,
        req_body,
    )

    # pdb.set_trace()
    assert res.status_code == 200, (
        "Failed with status code: "
        + str(res.status_code)
        + " and response: "
        + str(res.json())
    )
    assert (
        res.json()[0]["payload"][0]["type"] == "chatBotSelectQuestion"
    ), "Failed with response: " + str(res.json())
    assert (
        res.json()[0]["payload"][1]["payload"][-1]["type"] == "visitorAddTextMessage"
    ), "Failed with response: " + str(res.json())
    logger.info(
        "\n ======= Now we have a visitor who has got the 'send form' message. ======="
    )

    visitor_chat_version = res.json()[0]["payload"][1]["payload"][-1]["guid"]
    visitor_chat_version_from_id = res.json()[0]["payload"][1]["payload"][-1]["id"]
    res_got_chatbot_select_question_message = res

    yield (
        res_got_chatbot_select_question_message,
        res_new_visitor,
        visitor_ashx_url,
        visitor_guid,
        visitor_session_id,
        campaign_id,
        chat_guid,
        visitor_chat_version,
        visitor_chat_version_from_id,
        intent_id,
    )


@pytest.fixture(scope="function")
def generate_visitor_got_chatbot_intent_pizza_order_response_message(
    generate_visitor_got_chatbot_select_question_pizza_order_message,
    visitor_get_latest_messages_solo_action,
):
    """在访客收到了chatBotSelectQuestion动作产生的buy pizza消息之后，再次去getMessages,会把intent的回复消息拿下来。
    然后从拿到的消息中取到如下数据，为后续的对这个消息做helpful/not helpful操作做准备：
    chatGuid - 已有
    actionGuid
    intentId - 已有
    botId
    chatbotMessageId
    visitor sessionId - 已有
    """

    (
        res_got_chatbot_select_question_message,
        res_new_visitor,
        visitor_ashx_url,
        visitor_guid,
        visitor_session_id,
        campaign_id,
        chat_guid,
        visitor_chat_version,
        visitor_chat_version_from_id,
        intent_id,
    ) = generate_visitor_got_chatbot_select_question_pizza_order_message
    # pdb.set_trace()

    # make sure the chatbot has enough time to respond to the visitor's message
    sleep(2)

    (
        res_visitor_get_latest_messages,
        res_new_visitor,
        visitor_ashx_url,
        visitor_guid,
        visitor_session_id,
        campaign_id,
        chat_guid,
        visitor_chat_version,
        visitor_chat_version_from_id,
    ) = visitor_get_latest_messages_solo_action(
        chat_guid, visitor_chat_version, visitor_chat_version_from_id
    )

    # pdb.set_trace()
    # 需要把getMessages取回来的消息中的originalMessage取出来，然后取里面的actionGuid, botId, chatbotMessageId
    assert (
        len(res_visitor_get_latest_messages.json()[0]["payload"]) > 0
    ), "Latest message is null. Failed with response: " + str(
        res_visitor_get_latest_messages.json()
    )
    bot_original_message = json.loads(
        res_visitor_get_latest_messages.json()[0]["payload"][0]["originalMessage"]
    )
    action_guid = bot_original_message["messageGuid"]
    intent_id = bot_original_message["intentId"]
    bot_id = bot_original_message["botId"]
    chatbot_message_id = bot_original_message["id"]

    # pdb.set_trace()
    yield (
        res_visitor_get_latest_messages,
        res_new_visitor,
        visitor_ashx_url,
        visitor_guid,
        visitor_session_id,
        campaign_id,
        chat_guid,
        visitor_chat_version,
        visitor_chat_version_from_id,
        intent_id,
        action_guid,
        bot_id,
        chatbot_message_id,
    )


@pytest.fixture(scope="function")
def generate_visitor_got_chatbot_intent_send_form_response_message(
    generate_visitor_got_chatbot_select_question_send_form_message,
    visitor_get_latest_messages_solo_action,
):
    """在访客收到了chatBotSelectQuestion动作产生的send form消息之后，再次去getMessages,会把intent的回复消息拿下来。"""

    (
        res_got_chatbot_select_question_message,
        res_new_visitor,
        visitor_ashx_url,
        visitor_guid,
        visitor_session_id,
        campaign_id,
        chat_guid,
        visitor_chat_version,
        visitor_chat_version_from_id,
        intent_id,
    ) = generate_visitor_got_chatbot_select_question_send_form_message
    # pdb.set_trace()

    # make sure the chatbot has enough time to respond to the visitor's message
    sleep(2)

    (
        res_visitor_get_latest_messages,
        res_new_visitor,
        visitor_ashx_url,
        visitor_guid,
        visitor_session_id,
        campaign_id,
        chat_guid,
        visitor_chat_version,
        visitor_chat_version_from_id,
    ) = visitor_get_latest_messages_solo_action(
        chat_guid, visitor_chat_version, visitor_chat_version_from_id
    )

    # pdb.set_trace()
    # 需要把getMessages取回来的消息中的originalMessage取出来，然后取里面的actionGuid, botId, chatbotMessageId
    assert (
        len(res_visitor_get_latest_messages.json()[0]["payload"]) > 0
    ), "Latest message is null. Failed with response: " + str(
        res_visitor_get_latest_messages.json()
    )
    bot_original_message = json.loads(
        res_visitor_get_latest_messages.json()[0]["payload"][0]["originalMessage"]
    )
    action_guid = bot_original_message["messageGuid"]
    intent_id = bot_original_message["intentId"]
    bot_id = bot_original_message["botId"]
    chatbot_message_id = bot_original_message["id"]

    # pdb.set_trace()
    yield (
        res_visitor_get_latest_messages,
        res_new_visitor,
        visitor_ashx_url,
        visitor_guid,
        visitor_session_id,
        campaign_id,
        chat_guid,
        visitor_chat_version,
        visitor_chat_version_from_id,
        intent_id,
        action_guid,
        bot_id,
        chatbot_message_id,
    )


@pytest.fixture(scope="function")
def enable_sentiment_analysis_for_live_chat(login):
    login_data = login
    request_url_enable = (
        login_data["api_url"] + "/bot/agentAssistSentimentAnalysisConfig"
    )
    request_body_enable = {"isEnabledForLiveChat": True}
    res_enable = send_request(
        request_url_enable,
        None,
        "PUT",
        None,
        login_data["common_headers"],
        request_body_enable,
    )

    # pdb.set_trace()
    assert res_enable.status_code == 200, (
        "Failed with status code: "
        + str(res_enable.status_code)
        + " and response: "
        + str(res_enable.json())
    )
    logger.info("\n ======= sentiment analysis for live chat has been enabled =======")
    yield res_enable

    request_url_disable = (
        login_data["api_url"] + "/bot/agentAssistSentimentAnalysisConfig"
    )
    request_body_disable = {"isEnabledForLiveChat": False}
    res_disable = send_request(
        request_url_disable,
        None,
        "PUT",
        None,
        login_data["common_headers"],
        request_body_disable,
    )

    # pdb.set_trace()
    assert res_disable.status_code == 200, (
        "Failed with status code: "
        + str(res_disable.status_code)
        + " and response: "
        + str(res_disable.json())
    )
    logger.info("\n ======= sentiment analysis for live chat has been disabled =======")

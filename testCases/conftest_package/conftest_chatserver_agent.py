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
def generate_agent_got_initial_messages(
    generate_visitor_insite,
    agent_get_initial_messages,
    visitor_end_chat_with_teardown,
):
    (
        res_agent_get_initial_messages,
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
        agent_latest_message_int_id,
        agent_latest_message_guid,
    ) = agent_get_initial_messages

    logger.info("\n ======= Now we have an agent who has got initial messages. =======")

    yield (
        res_agent_get_initial_messages,
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
        agent_latest_message_int_id,
        agent_latest_message_guid,
    )

    # teardown part: 需要结束聊天，并确保聊天最后被删除
    visitor_end_chat_with_teardown()


@pytest.fixture(scope="function")
def generate_agent_recalled_message(
    generate_visitor_insite,
    agent_recall_text_message,
    visitor_end_chat_with_teardown,
):
    (
        res_agent_recall_message,
        res_agent_send_message,
        res_agent_get_initial_messages,
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
        agent_latest_message_int_id,
        agent_latest_message_guid,
        agent_send_message_guid,
    ) = agent_recall_text_message

    logger.info(
        "\n ======= Now we have an agent who has recalled a text message in a chat. ======="
    )

    yield (
        res_agent_recall_message,
        res_agent_send_message,
        res_agent_get_initial_messages,
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
        agent_latest_message_int_id,
        agent_latest_message_guid,
        agent_send_message_guid,
    )

    # teardown part: 需要结束聊天，并确保聊天最后被删除
    visitor_end_chat_with_teardown()


@pytest.fixture(scope="function")
def generate_agent_sent_message(
    generate_visitor_insite,
    agent_send_text_message,
    visitor_end_chat_with_teardown,
):
    (
        res_agent_send_message,
        res_agent_get_initial_messages,
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
        agent_latest_message_int_id,
        agent_latest_message_guid,
        agent_send_message_guid,
    ) = agent_send_text_message

    logger.info(
        "\n ======= Now we have an agent who has sent a message in a chat. ======="
    )

    yield (
        res_agent_send_message,
        res_agent_get_initial_messages,
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
        agent_latest_message_int_id,
        agent_latest_message_guid,
        agent_send_message_guid,
    )

    # teardown part: 需要结束聊天，并确保聊天最后被删除
    visitor_end_chat_with_teardown()


@pytest.fixture(scope="function")
def generate_agent_requested_video_chat(
    generate_visitor_insite,
    agent_request_video_chat,
    visitor_end_chat_with_teardown,
):
    (
        res_agent_request_video_chat,
        res_agent_get_initial_messages,
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
        agent_latest_message_int_id,
        agent_latest_message_guid,
        agent_send_message_guid,
    ) = agent_request_video_chat

    logger.info(
        "\n ======= Now we have an agent who has requested video chat in a chat. ======="
    )

    yield (
        res_agent_request_video_chat,
        res_agent_get_initial_messages,
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
        agent_latest_message_int_id,
        agent_latest_message_guid,
        agent_send_message_guid,
    )

    # teardown part: 需要结束聊天，并确保聊天最后被删除
    visitor_end_chat_with_teardown()


@pytest.fixture(scope="function")
def generate_agent_requested_audio_chat(
    generate_visitor_insite,
    agent_request_audio_chat,
    visitor_end_chat_with_teardown,
):
    (
        res_agent_request_audio_chat,
        res_agent_get_initial_messages,
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
        agent_latest_message_int_id,
        agent_latest_message_guid,
        agent_send_message_guid,
    ) = agent_request_audio_chat

    logger.info(
        "\n ======= Now we have an agent who has requested audio chat in a chat. ======="
    )

    yield (
        res_agent_request_audio_chat,
        res_agent_get_initial_messages,
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
        agent_latest_message_int_id,
        agent_latest_message_guid,
        agent_send_message_guid,
    )

    # teardown part: 需要结束聊天，并确保聊天最后被删除
    visitor_end_chat_with_teardown()


@pytest.fixture(scope="function")
def generate_agent_with_visitor_requested_video(
    generate_visitor_insite,
    agent_get_initial_messages,
    visitor_request_video_chat,
    visitor_end_chat_with_teardown,
):
    (
        res_agent_get_initial_messages,
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
        agent_latest_message_int_id,
        agent_latest_message_guid,
    ) = agent_get_initial_messages

    (
        res_visitor_request_video_chat,
        res_get_initial_messages,
        res_new_visitor,
        visitor_ashx_url,
        livechat_handler3_url,
        visitor_guid,
        visitor_session_id,
        campaign_id,
        chat_guid,
        agent_session_id,
        agent_version_offset_guid,
        visitor_chat_version,
        visitor_chat_version_from_id,
    ) = visitor_request_video_chat

    logger.info(
        "\n ======= Now we have an agent with visitor requested video chat. ======="
    )

    yield (
        res_agent_get_initial_messages,
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
        agent_latest_message_int_id,
        agent_latest_message_guid,
    )

    # teardown part: 需要结束聊天，并确保聊天最后被删除
    visitor_end_chat_with_teardown()


@pytest.fixture(scope="function")
def generate_agent_with_visitor_requested_audio(
    generate_visitor_insite,
    agent_get_initial_messages,
    visitor_request_audio_chat,
    visitor_end_chat_with_teardown,
):
    (
        res_agent_get_initial_messages,
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
        agent_latest_message_int_id,
        agent_latest_message_guid,
    ) = agent_get_initial_messages

    (
        res_visitor_request_audio_chat,
        res_get_initial_messages,
        res_new_visitor,
        visitor_ashx_url,
        livechat_handler3_url,
        visitor_guid,
        visitor_session_id,
        campaign_id,
        chat_guid,
        agent_session_id,
        agent_version_offset_guid,
        visitor_chat_version,
        visitor_chat_version_from_id,
    ) = visitor_request_audio_chat

    logger.info(
        "\n ======= Now we have an agent with visitor requested audio chat. ======="
    )

    yield (
        res_agent_get_initial_messages,
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
        agent_latest_message_int_id,
        agent_latest_message_guid,
    )

    # teardown part: 需要结束聊天，并确保聊天最后被删除
    visitor_end_chat_with_teardown()


@pytest.fixture(scope="function")
def generate_agent_accepted_video_chat(
    generate_visitor_insite,
    agent_accept_video_chat_request,
    visitor_end_chat_with_teardown,
):
    (
        res_agent_accept_video_chat_request,
        res_agent_get_initial_messages,
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
        agent_latest_message_int_id,
        agent_latest_message_guid,
    ) = agent_accept_video_chat_request

    sleep(2)  # 让视频聊天持续一段时间，方便后续的测试
    logger.info("\n ======= Now we have an agent in video-chatting. =======")

    yield (
        res_agent_accept_video_chat_request,
        res_agent_get_initial_messages,
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
        agent_latest_message_int_id,
        agent_latest_message_guid,
    )

    # teardown part: 需要结束聊天，并确保聊天最后被删除
    visitor_end_chat_with_teardown()


@pytest.fixture(scope="function")
def generate_agent_accepted_audio_chat(
    generate_visitor_insite,
    agent_accept_audio_chat_request,
    visitor_end_chat_with_teardown,
):
    (
        res_agent_accept_audio_chat_request,
        res_agent_get_initial_messages,
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
        agent_latest_message_int_id,
        agent_latest_message_guid,
    ) = agent_accept_audio_chat_request

    sleep(2)  # 让音频聊天持续一段时间，方便后续的测试
    logger.info("\n ======= Now we have an agent in audio-chatting. =======")

    yield (
        res_agent_accept_audio_chat_request,
        res_agent_get_initial_messages,
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
        agent_latest_message_int_id,
        agent_latest_message_guid,
    )

    # teardown part: 需要结束聊天，并确保聊天最后被删除
    visitor_end_chat_with_teardown()


@pytest.fixture(scope="function")
def generate_agent_requested_to_transfer_chat_to_department(
    generate_visitor_insite,
    agent_transfer_chat_to_department,
    visitor_end_chat_with_teardown,
):
    (
        res_transfer_chat_to_department,
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
        agent2_login_data,
        agent2_res_login_ac,
        agent2_session_id,
        agent2_version_offset_guid,
    ) = agent_transfer_chat_to_department

    logger.info(
        "\n ======= Now we have an agent who has requested to transfer the chat to department2. ======="
    )

    yield (
        res_transfer_chat_to_department,
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
        agent2_login_data,
        agent2_res_login_ac,
        agent2_session_id,
        agent2_version_offset_guid,
    )

    # teardown part: 需要结束聊天，并确保聊天最后被删除
    visitor_end_chat_with_teardown()


@pytest.fixture(scope="function")
def generate_agent_enabled_translation_with_previous_visitor_messages(
    generate_visitor_insite,
    agent_enable_auto_translation_in_chat,
    visitor_end_chat_with_teardown,
):
    (
        res_agent_enable_auto_translation_in_chat,
        res_agent_get_initial_messages,
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
        agent_latest_message_int_id,
        agent_latest_message_guid,
        visitor_previous_message_guid,
    ) = agent_enable_auto_translation_in_chat

    logger.info(
        "\n ======= Now we have an agent who has enabled auto translation in chat with previous visitor messages. ======="
    )
    sleep(2)  # wait for translation to be done

    yield (
        res_agent_enable_auto_translation_in_chat,
        res_agent_get_initial_messages,
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
        agent_latest_message_int_id,
        agent_latest_message_guid,
        visitor_previous_message_guid,
    )

    # teardown part: 需要结束聊天，并确保聊天最后被删除
    visitor_end_chat_with_teardown()


@pytest.fixture(scope="function")
def agent_manually_invite(login, login_agent_console_new, generate_visitor_insite):
    login_data = login
    site_id = login_data["site_id"]

    (
        res_login_ac,
        livechat_handler3_url,
        agent_session_id,
        agent_version_offset_guid,
    ) = login_agent_console_new

    (
        res_new_visitor,
        visitor_guid,
        visitor_session_id,
        campaign_id,
        visitor_ashx_url,
    ) = generate_visitor_insite

    #  ======= Agent manually invite =======
    req_body = {
        "m": [
            {
                "d": 224,
                "a": visitor_guid,
                "b": "Hello, how may I help you? - from pytest",
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
    res = send_request(
        livechat_handler3_url,
        None,
        "POST",
        None,
        login_data["common_headers"],
        req_body,
    )
    # pdb.set_trace()
    assert res.status_code == 200, (
        "Failed with status code: "
        + str(res.status_code)
        + " and response: "
        + str(res.json())
    )
    assert res.json()["c"] == 0, "Failed with response: " + str(res.json())

    logger.info("\n ======= Agent has manually invited the visitor. =======")

    res_agent_manual_invite = res

    yield (
        res_agent_manual_invite,
        res_new_visitor,
        livechat_handler3_url,
        visitor_guid,
        visitor_session_id,
        campaign_id,
        agent_session_id,
        agent_version_offset_guid,
    )


@pytest.fixture(scope="function")
def agent_accept_chat(login, login_agent_console_new, visitor_request_chat):
    def _agent_accept_chat():
        login_data = login
        site_id = login_data["site_id"]

        (
            res_login_ac,
            livechat_handler3_url,
            agent_session_id,
            agent_version_offset_guid,
        ) = login_agent_console_new

        (
            res_new_visitor,
            res_request_chat,
            visitor_ashx_url,
            visitor_guid,
            visitor_session_id,
            campaign_id,
            chat_guid,
        ) = visitor_request_chat

        sleep(1)  # 等待1s,使得waiting time>0
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
        assert res_accept_chat.status_code == 200, (
            "Failed with status code: "
            + str(res_accept_chat.status_code)
            + " and response: "
            + str(res_accept_chat.json())
        )
        assert res_accept_chat.json()["c"] == 0, "Failed with response: " + str(
            res_accept_chat.json()
        )

        logger.info("\n ======= Agent has accepted chat. =======")

        return (
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
        )

    yield _agent_accept_chat


@pytest.fixture(scope="function")
def agent_accept_chat_solo_action(
    login, login_agent_console_new, generate_visitor_insite
):
    def _agent_accept_chat_solo_action():
        login_data = login
        site_id = login_data["site_id"]

        (
            res_login_ac,
            livechat_handler3_url,
            agent_session_id,
            agent_version_offset_guid,
        ) = login_agent_console_new
        (
            res_new_visitor,
            visitor_guid,
            visitor_session_id,
            campaign_id,
            visitor_ashx_url,
        ) = generate_visitor_insite

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
        assert res_accept_chat.status_code == 200, (
            "Failed with status code: "
            + str(res_accept_chat.status_code)
            + " and response: "
            + str(res_accept_chat.json())
        )
        assert res_accept_chat.json()["c"] == 0, "Failed with response: " + str(
            res_accept_chat.json()
        )

        logger.info("\n ======= Agent has accepted chat. =======")

        return (
            res_accept_chat,
            res_new_visitor,
            livechat_handler3_url,
            visitor_guid,
            visitor_session_id,
            campaign_id,
            agent_session_id,
            agent_version_offset_guid,
        )

    yield _agent_accept_chat_solo_action


@pytest.fixture(scope="function")
def agent_refuse_chat(login, login_agent_console_new, visitor_request_chat):
    def _agent_refuse_chat():
        login_data = login
        site_id = login_data["site_id"]

        (
            res_login_ac,
            livechat_handler3_url,
            agent_session_id,
            agent_version_offset_guid,
        ) = login_agent_console_new

        (
            res_new_visitor,
            res_request_chat,
            visitor_ashx_url,
            visitor_guid,
            visitor_session_id,
            campaign_id,
            chat_guid,
        ) = visitor_request_chat

        #  ======= Agent refuse chat =======
        req_body_refuse_chat = {
            "m": [
                {
                    "d": 105,
                    "a": visitor_guid,
                    "messageGuid": "3C7D2925-B0EF-360A-035C-73F4589ECA9C",
                    "e": 5042,
                },
            ],
            "s": agent_session_id,
            "l": [],
            "operatorOffset": {"Guid": agent_version_offset_guid, "OffSet": 0},
        }

        # pdb.set_trace()
        res_refuse_chat = send_request(
            livechat_handler3_url,
            None,
            "POST",
            None,
            login_data["common_headers"],
            req_body_refuse_chat,
        )
        # pdb.set_trace()
        assert res_refuse_chat.status_code == 200, (
            "Failed with status code: "
            + str(res_refuse_chat.status_code)
            + " and response: "
            + str(res_refuse_chat.json())
        )
        assert res_refuse_chat.json()["c"] == 0, "Failed with response: " + str(
            res_refuse_chat.json()
        )

        logger.info("\n ======= Agent has refused chat. =======")

        return (
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
        )

    yield _agent_refuse_chat


@pytest.fixture(scope="function")
def agent_get_initial_messages(login, agent_accept_chat):
    login_data = login
    (
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
    ) = agent_accept_chat()

    #  ======= agent get initial messages =======

    request_body = {
        "m": [{"d": 131, "e": 1045}],
        "s": agent_session_id,
        "l": [{"a": visitor_guid, "b": -1, "latestChatMessageGuid": ""}],
        "operatorOffset": {"Guid": agent_version_offset_guid, "OffSet": 0},
    }

    # pdb.set_trace()
    res_agent_get_initial_messages = send_request(
        livechat_handler3_url,
        None,
        "POST",
        None,
        login_data["common_headers"],
        request_body,
    )
    # pdb.set_trace()
    assert res_agent_get_initial_messages.status_code == 200, (
        "Failed with status code: "
        + str(res_agent_get_initial_messages.status_code)
        + " and response: "
        + str(res_agent_get_initial_messages.json())
    )
    assert res_agent_get_initial_messages.json()["c"] == 0, " with response: " + str(
        res_agent_get_initial_messages.json()
    )
    logger.info("\n ======= agent has got first few messages =======")

    # update agent latest chat version
    agent_latest_message_int_id = res_agent_get_initial_messages.json()["m"][-1]["e"]
    agent_latest_message_guid = res_agent_get_initial_messages.json()["m"][-1][
        "messageGuid"
    ]

    yield (
        res_agent_get_initial_messages,
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
        agent_latest_message_int_id,
        agent_latest_message_guid,
    )


@pytest.fixture(scope="function")
def agent_transfer_chat(
    login,
    agent_accept_chat,
    agent2_login_agent_console,
):
    login_data = login
    agent2_id = login_data["agent2_id"]

    (
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
    ) = agent_accept_chat()

    #  ======= agent transfer chat to agent2 =======

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
    yield (
        res_transfer_chat,
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
    )


@pytest.fixture(scope="function")
def agent_transfer_chat_to_department(
    login,
    agent2_login,
    init_2departments,
    agent_accept_chat,
    agent2_login_agent_console_new,
):
    login_data = login
    agent2_login_data = agent2_login
    agent2_id = login_data["agent2_id"]
    (
        create_department,
        create_2nd_department,
        department1_id,
        department2_id,
    ) = init_2departments

    (
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
    ) = agent_accept_chat()
    (
        agent2_res_login_ac,
        livechat_handler3_url,
        agent2_session_id,
        agent2_version_offset_guid,
    ) = agent2_login_agent_console_new

    #  ======= agent transfer chat to department2 =======

    request_body = {
        "m": [
            {
                "d": 218,
                "a": visitor_guid,
                "b": department2_id,
                "c": "false",
                "messageGuid": str(uuid.uuid4()),
                "e": 78,
            }
        ],
        "s": agent_session_id,
        "l": [],
        "operatorOffset": {"Guid": agent_version_offset_guid, "OffSet": 0},
    }

    # pdb.set_trace()
    res = send_request(
        livechat_handler3_url,
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
    assert res.json()["c"] == 0, " with response: " + str(res.json())
    res_transfer_chat_to_department = res

    logger.info(
        "\n ======= agent has requested to transfer the chat to department2 ======="
    )
    yield (
        res_transfer_chat_to_department,
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
        agent2_login_data,
        agent2_res_login_ac,
        agent2_session_id,
        agent2_version_offset_guid,
    )


@pytest.fixture(scope="function")
def agent_send_text_message(login, agent_get_initial_messages):
    login_data = login
    (
        res_agent_get_initial_messages,
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
        agent_latest_message_int_id,
        agent_latest_message_guid,
    ) = agent_get_initial_messages

    agent_send_message_guid = str(uuid.uuid4())

    #  ======= Agent send message =======

    request_body = {
        "m": [
            {
                "d": 102,
                "a": visitor_guid,
                "messageGuid": agent_send_message_guid,
                "e": 73,
                "b": "aGVsbG8gdmlzaXRvcg==",  # hello visitor
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
    yield (
        res_agent_send_message,
        res_agent_get_initial_messages,
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
        agent_latest_message_int_id,
        agent_latest_message_guid,
        agent_send_message_guid,
    )


@pytest.fixture(scope="function")
def agent_recall_text_message(login, agent_send_text_message):
    login_data = login
    (
        res_agent_send_message,
        res_agent_get_initial_messages,
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
        agent_latest_message_int_id,
        agent_latest_message_guid,
        agent_send_message_guid,
    ) = agent_send_text_message

    #  ======= Agent recall message =======

    request_body = {
        "m": [
            {
                "d": 760,
                "a": visitor_guid,
                "b": agent_send_message_guid,
            },
        ],
        "s": agent_session_id,
        "operatorOffset": {"Guid": agent_version_offset_guid, "OffSet": 0},
    }

    # pdb.set_trace()
    res = send_request(
        livechat_handler3_url,
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
    assert res.json()["c"] == 0, " with response: " + str(res.json())

    logger.info("\n ======= agent has recalled a text message =======")

    res_agent_recall_message = res

    yield (
        res_agent_recall_message,
        res_agent_send_message,
        res_agent_get_initial_messages,
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
        agent_latest_message_int_id,
        agent_latest_message_guid,
        agent_send_message_guid,
    )


@pytest.fixture(scope="function")
def agent_submit_wrapup_category_and_comment_during_chat(
    login, agent_get_initial_messages, get_wrapup_category_option
):
    login_data = login
    res_get_wrapup_category_option, first_option_id, second_option_id = (
        get_wrapup_category_option
    )

    (
        res_agent_get_initial_messages,
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
        agent_latest_message_int_id,
        agent_latest_message_guid,
    ) = agent_get_initial_messages

    #  ======= Agent submit wrapup during chatting =======

    request_body = {
        "m": [
            {
                "d": 215,
                "a": visitor_guid,
                "b": f'{{"c": {first_option_id},"e":"temp comment - nice customer - submitted by pytest","d":[],"b": {chat_guid},"a": {visitor_guid}}}',
            },
        ],
        "s": agent_session_id,
        "operatorOffset": {"Guid": agent_version_offset_guid, "OffSet": 0},
    }

    # pdb.set_trace()
    res = send_request(
        livechat_handler3_url,
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
    assert res.json()["c"] == 0, " with response: " + str(res.json())

    logger.info(
        "\n ======= agent has submitted wrapup category and comment during chatting. ======="
    )
    res_agent_submit_wrapup = res

    yield (
        res_agent_submit_wrapup,
        res_agent_get_initial_messages,
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
        agent_latest_message_int_id,
        agent_latest_message_guid,
    )


@pytest.fixture(scope="function")
def agent_request_video_chat(login, agent_get_initial_messages):
    login_data = login
    (
        res_agent_get_initial_messages,
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
        agent_latest_message_int_id,
        agent_latest_message_guid,
    ) = agent_get_initial_messages

    agent_send_message_guid = str(uuid.uuid4())

    #  ======= Agent requests video chat =======

    request_body = {
        "m": [
            {
                "d": 320,
                "a": visitor_guid,
                "messageGuid": agent_send_message_guid,
                "e": 66,
            },
            {"d": 131, "e": 67},
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
    res = send_request(
        livechat_handler3_url,
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
    assert res.json()["c"] == 0, "Failed with response: " + str(res.json())

    logger.info("\n ======= agent has requested video chat =======")

    agent_latest_message_int_id = res.json()["m"][-1]["e"]
    agent_latest_message_guid = res.json()["m"][-1]["messageGuid"]
    res_agent_request_video_chat = res

    yield (
        res_agent_request_video_chat,
        res_agent_get_initial_messages,
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
        agent_latest_message_int_id,
        agent_latest_message_guid,
        agent_send_message_guid,
    )


@pytest.fixture(scope="function")
def agent_request_audio_chat(login, agent_get_initial_messages):
    login_data = login
    (
        res_agent_get_initial_messages,
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
        agent_latest_message_int_id,
        agent_latest_message_guid,
    ) = agent_get_initial_messages

    agent_send_message_guid = str(uuid.uuid4())

    #  ======= Agent requests audio chat =======

    request_body = {
        "m": [
            {
                "d": 332,
                "a": visitor_guid,
                "messageGuid": agent_send_message_guid,
                "e": 66,
            },
            {"d": 131, "e": 67},
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
    res = send_request(
        livechat_handler3_url,
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
    assert res.json()["c"] == 0, "Failed with response: " + str(res.json())

    logger.info("\n ======= agent has requested audio chat =======")

    agent_latest_message_int_id = res.json()["m"][-1]["e"]
    agent_latest_message_guid = res.json()["m"][-1]["messageGuid"]
    res_agent_request_audio_chat = res

    yield (
        res_agent_request_audio_chat,
        res_agent_get_initial_messages,
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
        agent_latest_message_int_id,
        agent_latest_message_guid,
        agent_send_message_guid,
    )


@pytest.fixture(scope="function")
def agent_accept_video_chat_request(
    login, agent_get_initial_messages, visitor_request_video_chat
):
    login_data = login
    (
        res_agent_get_initial_messages,
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
        agent_latest_message_int_id,
        agent_latest_message_guid,
    ) = agent_get_initial_messages

    #  ======= Agent accept video chat =======

    request_body = {
        "m": [
            {
                "d": 322,
                "a": visitor_guid,
                "messageGuid": str(uuid.uuid4()),
                "e": 66,
            },
            {"d": 131, "e": 67},
        ],
        "s": agent_session_id,
        "l": [
            {
                "a": visitor_guid,
                "b": agent_latest_message_int_id,
                "latestChatMessageGuid": agent_latest_message_guid,
            },
        ],
        "operatorOffset": {"Guid": agent_version_offset_guid, "OffSet": 0},
    }

    # pdb.set_trace()
    res = send_request(
        livechat_handler3_url,
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
    assert res.json()["c"] == 0, " with response: " + str(res.json())

    logger.info("\n ======= agent has accepted video chat request. =======")

    # update agent latest chat version
    agent_latest_message_int_id = res.json()["m"][-1]["e"]
    agent_latest_message_guid = res.json()["m"][-1]["messageGuid"]

    res_agent_accept_video_chat_request = res

    yield (
        res_agent_accept_video_chat_request,
        res_agent_get_initial_messages,
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
        agent_latest_message_int_id,
        agent_latest_message_guid,
    )


@pytest.fixture(scope="function")
def agent_accept_audio_chat_request(
    login, agent_get_initial_messages, visitor_request_audio_chat
):
    login_data = login
    (
        res_agent_get_initial_messages,
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
        agent_latest_message_int_id,
        agent_latest_message_guid,
    ) = agent_get_initial_messages

    #  ======= Agent accept audio chat =======

    request_body = {
        "m": [
            {
                "d": 334,
                "a": visitor_guid,
                "messageGuid": str(uuid.uuid4()),
                "e": 66,
            },
            {"d": 131, "e": 67},
        ],
        "s": agent_session_id,
        "l": [
            {
                "a": visitor_guid,
                "b": agent_latest_message_int_id,
                "latestChatMessageGuid": agent_latest_message_guid,
            },
        ],
        "operatorOffset": {"Guid": agent_version_offset_guid, "OffSet": 0},
    }

    # pdb.set_trace()
    res = send_request(
        livechat_handler3_url,
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
    assert res.json()["c"] == 0, " with response: " + str(res.json())

    logger.info("\n ======= agent has accepted audio chat request. =======")

    # update agent latest chat version
    agent_latest_message_int_id = res.json()["m"][-1]["e"]
    agent_latest_message_guid = res.json()["m"][-1]["messageGuid"]

    res_agent_accept_audio_chat_request = res

    yield (
        res_agent_accept_audio_chat_request,
        res_agent_get_initial_messages,
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
        agent_latest_message_int_id,
        agent_latest_message_guid,
    )


@pytest.fixture(scope="function")
def agent_set_preference_enable_auto_translation(
    login,
    enable_auto_translation,
    login_agent_console_new,
):
    login_data = login
    (
        res_login_ac,
        livechat_handler3_url,
        agent_session_id,
        agent_version_offset_guid,
    ) = login_agent_console_new

    #  ======= agent set preference to enable auto translation and set language as English =======
    agent_preference = res_login_ac.json()["o"][0]["e"]["a"]
    agent_preference["bk"] = True

    request_body = {
        "m": [{"d": 126, "b": json.dumps(agent_preference), "e": 3}],
        "s": agent_session_id,
        "l": [],
        "operatorOffset": {"Guid": agent_version_offset_guid, "OffSet": 0},
    }

    # pdb.set_trace()
    res = send_request(
        livechat_handler3_url,
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
    assert res.json()["c"] == 0, " with response: " + str(res.json())

    logger.info(
        "\n ======= auto translation for agent in AC has been enabled and the Language is set as English. ======="
    )
    yield res

    # teardown: restore to disable auto translation
    agent_preference["bk"] = False

    req_body_disable = {
        "m": [{"d": 126, "b": json.dumps(agent_preference), "e": 3}],
        "s": agent_session_id,
        "l": [],
        "operatorOffset": {"Guid": agent_version_offset_guid, "OffSet": 0},
    }

    # pdb.set_trace()
    res_disable = send_request(
        livechat_handler3_url,
        None,
        "POST",
        None,
        login_data["common_headers"],
        req_body_disable,
    )
    # pdb.set_trace()
    assert res_disable.status_code == 200, (
        "Failed with status code: "
        + str(res_disable.status_code)
        + " and response: "
        + str(res_disable.json())
    )
    assert res_disable.json()["c"] == 0, " with response: " + str(res_disable.json())

    logger.info(
        "\n ======= auto translation for agent in AC has been restored to be disabled. ======="
    )


@pytest.fixture(scope="function")
def agent2_set_preference_enable_auto_monitor(
    agent2_login,
    agent2_login_agent_console_new,
):
    login_data = agent2_login
    (
        res_login_ac,
        livechat_handler3_url,
        agent_session_id,
        agent_version_offset_guid,
    ) = agent2_login_agent_console_new

    agent_preference = res_login_ac.json()["o"][0]["e"]["a"]
    agent_preference["bi"] = agent_preference["bi"].replace('"f":false', '"f":true')

    request_body = {
        "m": [{"d": 126, "b": json.dumps(agent_preference), "e": 0}],
        "s": agent_session_id,
        "l": [],
        "operatorOffset": {"Guid": agent_version_offset_guid, "OffSet": 0},
    }

    # pdb.set_trace()
    res = send_request(
        livechat_handler3_url,
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
    assert res.json()["c"] == 0, " with response: " + str(res.json())
    # wait for 5 seconds to make sure the setting is effective
    sleep(5)
    logger.info("\n ======= agent2 auto monitor in AC has been enabled. =======")
    yield res

    agent_preference["bi"] = agent_preference["bi"].replace('"f":true', '"f":false')

    req_body_disable = {
        "m": [{"d": 126, "b": json.dumps(agent_preference), "e": 0}],
        "s": agent_session_id,
        "l": [],
        "operatorOffset": {"Guid": agent_version_offset_guid, "OffSet": 0},
    }

    # pdb.set_trace()
    res_disable = send_request(
        livechat_handler3_url,
        None,
        "POST",
        None,
        login_data["common_headers"],
        req_body_disable,
    )
    # pdb.set_trace()
    assert res_disable.status_code == 200, (
        "Failed with status code: "
        + str(res_disable.status_code)
        + " and response: "
        + str(res_disable.json())
    )
    assert res_disable.json()["c"] == 0, " with response: " + str(res_disable.json())

    logger.info(
        "\n ======= agent2 auto monitor in AC has been restored to be disabled. ======="
    )


@pytest.fixture(scope="function")
def agent_enable_auto_translation_in_chat(
    login,
    agent_set_preference_enable_auto_translation,
    agent_get_initial_messages,
    visitor_send_text_message,
):
    login_data = login

    (
        res_agent_get_initial_messages,
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
        agent_latest_message_int_id,
        agent_latest_message_guid,
    ) = agent_get_initial_messages

    request_body = {
        "m": [
            {
                "d": 208,
                "a": visitor_guid,
                "b": "14",
                "messageGuid": str(uuid.uuid4()),
                "e": 66,
            },
            {"d": 131, "e": 70},
        ],
        "s": agent_session_id,
        "l": [
            {
                "a": visitor_guid,
                "b": agent_latest_message_int_id,
                "latestChatMessageGuid": agent_latest_message_guid,
            },
        ],
        "operatorOffset": {"Guid": agent_version_offset_guid, "OffSet": 0},
    }

    # pdb.set_trace()
    res = send_request(
        livechat_handler3_url,
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
    assert res.json()["c"] == 0, " with response: " + str(res.json())

    logger.info(
        "\n ======= Agent has enabled Auto Translation for this chat and got latest messages. ======="
    )

    visitor_previous_message_guid = res.json()["m"][0][
        "messageGuid"
    ]  # this message will be translated after agent enabled auto translation
    agent_latest_message_int_id = res.json()["m"][-1]["e"]
    agent_latest_message_guid = res.json()["m"][-1]["messageGuid"]

    res_agent_enable_auto_translation_in_chat = res

    yield (
        res_agent_enable_auto_translation_in_chat,
        res_agent_get_initial_messages,
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
        agent_latest_message_int_id,
        agent_latest_message_guid,
        visitor_previous_message_guid,
    )


@pytest.fixture(scope="function")
def agent_enable_gotomeeting_in_ac(
    login,
    enable_gotomeeting_integration,
    login_agent_console_new,
):
    login_data = login

    (
        res_login_ac,
        livechat_handler3_url,
        agent_session_id,
        agent_version_offset_guid,
    ) = login_agent_console_new

    request_body = {
        "m": [
            {"d": 213, "b": "jamesdd@163.com⊙Aa000000"},
        ],
        "s": agent_session_id,
        "operatorOffset": {"Guid": agent_version_offset_guid, "OffSet": 0},
    }

    # pdb.set_trace()
    res = send_request(
        livechat_handler3_url,
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
    assert res.json()["c"] == 0, " with response: " + str(res.json())
    assert res.json()["o"][0]["c"] == 0, " with response: " + str(res.json())
    assert res.json()["o"][0]["d"] == "true", " with response: " + str(res.json())

    logger.info("\n ======= Agent has enabled Gotomeeting integration in AC. =======")

    res_agent_enable_gotomeeting_in_ac = res

    yield (
        res_agent_enable_gotomeeting_in_ac,
        res_login_ac,
        livechat_handler3_url,
        agent_session_id,
        agent_version_offset_guid,
    )

    req_body_reset = {
        "m": [
            {"d": 213, "b": "⊙"},
        ],
        "s": agent_session_id,
        "operatorOffset": {"Guid": agent_version_offset_guid, "OffSet": 0},
    }

    # pdb.set_trace()
    res_reset = send_request(
        livechat_handler3_url,
        None,
        "POST",
        None,
        login_data["common_headers"],
        req_body_reset,
    )
    # pdb.set_trace()
    assert res_reset.status_code == 200, (
        "Failed with status code: "
        + str(res_reset.status_code)
        + " and response: "
        + str(res_reset.json())
    )
    assert res_reset.json()["c"] == 0, " with response: " + str(res_reset.json())
    assert res_reset.json()["o"][0]["c"] == 0, " with response: " + str(
        res_reset.json()
    )
    assert res_reset.json()["o"][0]["d"] == "false", " with response: " + str(
        res_reset.json()
    )

    logger.info(
        "\n ======= Agent has reset/disabled Gotomeeting integration in AC. ======="
    )

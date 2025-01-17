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
def generate_visitor_insite(visitor_new_visitor, ban_visitor):
    (
        res_new_visitor,
        visitor_guid,
        visitor_session_id,
        campaign_id,
        visitor_ashx_url,
    ) = visitor_new_visitor

    yield (
        res_new_visitor,
        visitor_guid,
        visitor_session_id,
        campaign_id,
        visitor_ashx_url,
    )

    # teardown part: 需要通过ban visitor的方式将visitor从chatserver中删除
    ban_visitor(visitor_guid)


@pytest.fixture(scope="function")
def generate_multi_visitors_insite(visitor_new_multi_visitors, ban_visitor):
    visitors = []

    def _generate_multi_visitors_insite(visitor_count=1):
        nonlocal visitors
        visitors = visitor_new_multi_visitors(visitor_count)
        return visitors

    yield _generate_multi_visitors_insite

    # teardown part: 需要通过ban visitor的方式将所有visitor从chatserver中删除
    for visitor in visitors:
        ban_visitor(visitor["visitor_guid"])


@pytest.fixture(scope="function")
def generate_visitor_manual_invited_then_request_chat(
    generate_visitor_insite,
    login_agent_console_new,
    visitor_check_manual_invitation_after_agent_invite,
    visitor_end_chat_solo_action,
    save_and_delete_chat,
):
    """这个fixture调用的时候，需要调用visitor_end_chat_solo_action这个Fixture。不能直接调用visitor_end_chat fixture，因为visitor_end_chat fixture中调用的agent_accept_chat中调用的visitor_request_chat会提前执行，本来想要的manual invited状态，就会变成waitingforchat的状态"""
    (
        res_check_manual_invitation,
        res_new_visitor,
        visitor_ashx_url,
        visitor_guid,
        visitor_session_id,
        campaign_id,
        chat_guid,
    ) = visitor_check_manual_invitation_after_agent_invite

    # pdb.set_trace()
    logger.info(
        "\n ======= Now we have a visitor who is in manual invited status and will then request chat to start a chat. ======="
    )

    yield (
        res_check_manual_invitation,
        res_new_visitor,
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
def generate_visitor_pre_chat(
    login_agent_console_new,
    generate_visitor_insite,
    visitor_request_chat_go_to_pre_chat,
):
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
    ) = visitor_request_chat_go_to_pre_chat

    logger.info("\n ======= Now we have a visitor in pre-chat status. =======")
    # pdb.set_trace()

    yield (
        res_login_ac,
        livechat_handler3_url,
        agent_session_id,
        agent_version_offset_guid,
        res_new_visitor,
        res_request_chat,
        visitor_ashx_url,
        visitor_guid,
        visitor_session_id,
        campaign_id,
    )


@pytest.fixture(scope="function")
def generate_visitor_no_pre_chat_system_processing(
    login_agent_console_new,
    generate_visitor_insite,
    visitor_request_chat_no_pre_chat_go_to_system_processing,
):
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
    ) = visitor_request_chat_no_pre_chat_go_to_system_processing

    logger.info(
        "\n ======= Now we have a visitor who doesn't have pre-chat and now is in system processing status. ======="
    )
    # pdb.set_trace()

    sleep(5)  # 等待一段时间，确保System Processing heartbeat已经结束
    yield (
        res_login_ac,
        livechat_handler3_url,
        agent_session_id,
        agent_version_offset_guid,
        res_new_visitor,
        res_request_chat,
        visitor_ashx_url,
        visitor_guid,
        visitor_session_id,
        campaign_id,
    )


@pytest.fixture(scope="function")
def generate_visitor_with_pre_chat_system_processing(
    login_agent_console_new,
    generate_visitor_insite,
    visitor_request_chat_go_to_pre_chat,
    visitor_submit_pre_chat,
    visitor_request_chat_with_pre_chat_go_to_system_processing,
):
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
    ) = visitor_request_chat_with_pre_chat_go_to_system_processing

    logger.info(
        "\n ======= Now we have a visitor who has done pre-chat and now is in system processing status. ======="
    )
    # pdb.set_trace()

    sleep(5)  # 等待一段时间，确保System Processing heartbeat已经结束
    yield (
        res_login_ac,
        livechat_handler3_url,
        agent_session_id,
        agent_version_offset_guid,
        res_new_visitor,
        res_request_chat,
        visitor_ashx_url,
        visitor_guid,
        visitor_session_id,
        campaign_id,
    )


@pytest.fixture(scope="function")
def generate_visitor_with_pre_chat_chatting_contain_department(
    login_agent_console_new,
    generate_visitor_insite,
    visitor_submit_pre_chat_with_department,
    visitor_request_chat_with_pre_chat_go_to_chat,
):
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
    ) = visitor_request_chat_with_pre_chat_go_to_chat

    logger.info(
        "\n ======= Now we have a visitor who has done pre-chat and now is in chat status. ======="
    )
    # pdb.set_trace()

    # sleep(5)  # 等待一段时间，确保System Processing heartbeat已经结束
    yield (
        res_login_ac,
        livechat_handler3_url,
        agent_session_id,
        agent_version_offset_guid,
        res_new_visitor,
        res_request_chat,
        visitor_ashx_url,
        visitor_guid,
        visitor_session_id,
        campaign_id,
    )


@pytest.fixture(scope="function")
def generate_visitor_waiting_for_accept(
    login_agent_console_new,
    generate_visitor_insite,
    visitor_request_chat,
    visitor_end_chat_with_teardown,
):
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

    logger.info("\n ======= Now we have a visitor waiting for accept. =======")

    yield (
        res_login_ac,
        livechat_handler3_url,
        agent_session_id,
        agent_version_offset_guid,
        res_new_visitor,
        res_request_chat,
        visitor_ashx_url,
        visitor_guid,
        visitor_session_id,
        campaign_id,
        chat_guid,
    )

    # teardown part: 需要结束聊天，并确保聊天最后被删除
    visitor_end_chat_with_teardown()


@pytest.fixture(scope="function")
def generate_visitor_waiting_for_refuse(
    login_agent_console_new,
    generate_visitor_insite,
    visitor_request_chat,
    save_and_delete_chat,
):
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

    logger.info("\n ======= Now we have a visitor waiting for refuse. =======")

    yield (
        res_login_ac,
        livechat_handler3_url,
        agent_session_id,
        agent_version_offset_guid,
        res_new_visitor,
        res_request_chat,
        visitor_ashx_url,
        visitor_guid,
        visitor_session_id,
        campaign_id,
        chat_guid,
    )

    # teardown part: 需要结束聊天，并确保聊天最后被删除
    save_and_delete_chat(chat_guid)


@pytest.fixture(scope="function")
def generate_visitor_chatting(
    generate_visitor_insite, agent_accept_chat, visitor_end_chat_with_teardown
):
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

    logger.info("\n ======= Now we have a chatting visitor. =======")

    yield (
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

    # teardown part: 需要结束聊天，并确保聊天最后被删除
    visitor_end_chat_with_teardown()


@pytest.fixture(scope="function")
def generate_visitor_got_initial_messages(
    generate_visitor_insite,
    visitor_get_initial_messages,
    visitor_end_chat_with_teardown,
):
    (
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
    ) = visitor_get_initial_messages

    logger.info(
        "\n ======= Now we have a visitor who has got initial messages. ======="
    )

    yield (
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
    )

    # teardown part: 需要结束聊天，并确保聊天最后被删除
    visitor_end_chat_with_teardown()


@pytest.fixture(scope="function")
def generate_visitor_sent_message(
    generate_visitor_insite,
    visitor_send_text_message,
    visitor_end_chat_with_teardown,
):
    (
        res_visitor_send_text_message,
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
    ) = visitor_send_text_message

    logger.info("\n ======= Now we have a visitor who has sent a text message. =======")

    yield (
        res_visitor_send_text_message,
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
    )

    # teardown part: 需要结束聊天，并确保聊天最后被删除
    visitor_end_chat_with_teardown()


@pytest.fixture(scope="function")
def generate_visitor_sent_very_positive_message(
    generate_visitor_insite,
    visitor_send_very_positive_text_message,
    visitor_end_chat_with_teardown,
):
    (
        res_visitor_send_text_message,
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
        message_guid,
        very_positive_text_message,
        visitor_chat_version,
        visitor_chat_version_from_id,
    ) = visitor_send_very_positive_text_message

    logger.info(
        "\n ======= Now we have a visitor who has sent a very positive message. ======="
    )

    yield (
        res_visitor_send_text_message,
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
        message_guid,
        very_positive_text_message,
        visitor_chat_version,
        visitor_chat_version_from_id,
    )

    # teardown part: 需要结束聊天，并确保聊天最后被删除
    visitor_end_chat_with_teardown()


@pytest.fixture(scope="function")
def generate_visitor_requested_video_chat(
    generate_visitor_insite,
    visitor_request_video_chat,
    visitor_end_chat_with_teardown,
):
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
        "\n ======= Now we have a visitor who has requested video chat. ======="
    )

    yield (
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
    )

    # teardown part: 需要结束聊天，并确保聊天最后被删除
    visitor_end_chat_with_teardown()


@pytest.fixture(scope="function")
def generate_visitor_requested_audio_chat(
    generate_visitor_insite,
    visitor_request_audio_chat,
    visitor_end_chat_with_teardown,
):
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
        "\n ======= Now we have a visitor who has requested audio chat. ======="
    )

    yield (
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
    )

    # teardown part: 需要结束聊天，并确保聊天最后被删除
    visitor_end_chat_with_teardown()


@pytest.fixture(scope="function")
def generate_visitor_with_agent_requested_video(
    generate_visitor_insite,
    agent_request_video_chat,
    visitor_get_initial_messages,
    visitor_end_chat_with_teardown,
):
    """先做agent_request_video_chat，再做visitor_get_initial_messages，这样可以把agent_request_video_chat的消息给拿下来。"""
    (
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
    ) = visitor_get_initial_messages

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
        "\n ======= Now we have a visitor with agent requested video chat. ======="
    )

    yield (
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
    )

    # teardown part: 需要结束聊天，并确保聊天最后被删除
    visitor_end_chat_with_teardown()


@pytest.fixture(scope="function")
def generate_visitor_with_agent_requested_audio(
    generate_visitor_insite,
    agent_request_audio_chat,
    visitor_get_initial_messages,
    visitor_end_chat_with_teardown,
):
    """先做agent_request_audio_chat，再做visitor_get_initial_messages，这样可以把agent_request_audio_chat的消息给拿下来。"""
    (
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
    ) = visitor_get_initial_messages

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
        "\n ======= Now we have a visitor with agent requested audio chat. ======="
    )

    yield (
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
    )

    # teardown part: 需要结束聊天，并确保聊天最后被删除
    visitor_end_chat_with_teardown()


@pytest.fixture(scope="function")
def generate_visitor_video_chatting(
    generate_visitor_insite,
    agent_accept_video_chat_request,
    visitor_get_latest_messages,
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

    (
        res_visitor_get_latest_messages,
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
    ) = visitor_get_latest_messages

    sleep(2)  # 让视频聊天持续一段时间，方便后续的测试
    logger.info("\n ======= Now we have a visitor in video-chatting. =======")

    yield (
        res_visitor_get_latest_messages,
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
    )

    # teardown part: 需要结束聊天，并确保聊天最后被删除
    visitor_end_chat_with_teardown()


@pytest.fixture(scope="function")
def generate_visitor_audio_chatting(
    generate_visitor_insite,
    agent_accept_audio_chat_request,
    visitor_get_latest_messages,
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

    (
        res_visitor_get_latest_messages,
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
    ) = visitor_get_latest_messages

    sleep(2)  # 让音频聊天持续一段时间，方便后续的测试
    logger.info("\n ======= Now we have a visitor in audio-chatting. =======")

    yield (
        res_visitor_get_latest_messages,
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
    )

    # teardown part: 需要结束聊天，并确保聊天最后被删除
    visitor_end_chat_with_teardown()


@pytest.fixture(scope="function")
def generate_visitor_chat_ended(
    generate_visitor_insite,
    login_agent_console_new,
    visitor_end_chat_with_teardown,
):
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
    ) = visitor_end_chat_with_teardown()

    yield (
        res_new_visitor,
        res_request_chat,
        visitor_ashx_url,
        visitor_guid,
        visitor_session_id,
        campaign_id,
        chat_guid,
        res_login_ac,
        livechat_handler3_url,
        agent_session_id,
        agent_version_offset_guid,
    )


@pytest.fixture(scope="function")
def generate_visitor_offline_message_no_submit(
    generate_visitor_insite, visitor_enter_offline_message
):
    (
        res_enter_offline_message,
        res_new_visitor,
        visitor_guid,
        visitor_session_id,
        campaign_id,
        visitor_ashx_url,
    ) = visitor_enter_offline_message

    logger.info(
        "\n ======= Now we have a visitor who has entered offline message window but will not submit. ======="
    )

    yield visitor_enter_offline_message


@pytest.fixture(scope="function")
def generate_visitor_offline_message_with_submit(
    generate_visitor_insite,
    visitor_enter_offline_message,
    save_and_delete_offline_message,
):
    (
        res_enter_offline_message,
        res_new_visitor,
        visitor_guid,
        visitor_session_id,
        campaign_id,
        visitor_ashx_url,
    ) = visitor_enter_offline_message

    logger.info(
        "\n ======= Now we have a visitor who has entered offline message window and ready to submit. ======="
    )
    yield visitor_enter_offline_message
    # teardown part: 需要删除生成的offline message
    save_and_delete_offline_message(campaign_id)


@pytest.fixture(scope="function")
def visitor_new_visitor(login, init_campaign):
    login_data = login
    campaign_id = init_campaign.json()["id"]
    site_id = login_data["site_id"]

    request_url = login_data["chat_server_url"] + f"/visitor.ashx?siteId={site_id}"
    # wait for new campaign added to chat server cache as interval is 5s
    time.sleep(6)
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
                {
                    "type": "checkIfOnline",
                    "campaignId": campaign_id,
                    "chatVersion": "",
                },
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

    res_new_visitor = send_request(
        request_url, None, "POST", None, login_data["common_headers"], request_body
    )

    # pdb.set_trace()
    assert res_new_visitor.status_code == 200, "Failed with response: " + str(
        res_new_visitor.json()
    )
    assert (
        res_new_visitor.json()[0]["payload"][1]["payload"]["ifNewVisitor"] == True
    ), "Failed with response: " + str(res_new_visitor.json())

    visitor_guid = res_new_visitor.json()[0]["payload"][1]["payload"]["visitorGuid"]
    visitor_session_id = res_new_visitor.json()[0]["payload"][1]["payload"]["sessionId"]

    visitor_ashx_url = (
        login_data["chat_server_url"]
        + f"/visitor.ashx?siteId={site_id}&visitorGuid={visitor_guid}"
    )

    logger.info(
        f"\n ======= new visitor with id: {visitor_guid} has been generated successfully ======="
    )
    yield res_new_visitor, visitor_guid, visitor_session_id, campaign_id, visitor_ashx_url


@pytest.fixture(scope="function")
def visitor_new_multi_visitors(login, init_campaign):
    login_data = login
    campaign_id = init_campaign.json()["id"]
    site_id = login_data["site_id"]

    request_url = login_data["chat_server_url"] + f"/visitor.ashx?siteId={site_id}"
    # wait for new campaign added to chat server cache as interval is 5s
    time.sleep(6)

    def _visitor_new_multi_visitors(visitor_count):
        visitors_info = []

        for i in range(visitor_count):
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
                            "name": f"temp visitor {i}",
                            "email": f"tempvisitor{i}@mail.com",
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
                        {
                            "type": "checkIfOnline",
                            "campaignId": campaign_id,
                            "chatVersion": "",
                        },
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

            res_new_visitor = send_request(
                request_url,
                None,
                "POST",
                None,
                login_data["common_headers"],
                request_body,
            )

            assert res_new_visitor.status_code == 200, "Failed with response: " + str(
                res_new_visitor.json()
            )
            assert (
                res_new_visitor.json()[0]["payload"][1]["payload"]["ifNewVisitor"]
                == True
            ), "Failed with response: " + str(res_new_visitor.json())

            visitor_guid = res_new_visitor.json()[0]["payload"][1]["payload"][
                "visitorGuid"
            ]
            visitor_session_id = res_new_visitor.json()[0]["payload"][1]["payload"][
                "sessionId"
            ]

            visitor_ashx_url = (
                login_data["chat_server_url"]
                + f"/visitor.ashx?siteId={site_id}&visitorGuid={visitor_guid}"
            )

            visitors_info.append(
                {
                    "res_new_visitor": res_new_visitor,
                    "visitor_guid": visitor_guid,
                    "visitor_session_id": visitor_session_id,
                    "campaign_id": campaign_id,
                    "visitor_ashx_url": visitor_ashx_url,
                }
            )

        logger.info(
            f"\n ======= {visitor_count} new visitor(s) has been generated successfully ======="
        )
        return visitors_info

    return _visitor_new_multi_visitors


@pytest.fixture(scope="function")
def visitor_check_manual_invitation_after_agent_invite(
    login, generate_visitor_insite, agent_manually_invite
):
    login_data = login
    site_id = login_data["site_id"]

    (
        res_new_visitor,
        visitor_guid,
        visitor_session_id,
        campaign_id,
        visitor_ashx_url,
    ) = generate_visitor_insite

    #  ======= visitor submit pre-chat =======

    req_body = [
        {
            "type": "checkManualInvitation",
            "campaignId": campaign_id,
            "chatVersion": "",
            "sessionId": visitor_session_id,
            "ssoSessionToken": "",
            "id": 15,
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
        res.json()[0]["type"] == "checkManualInvitation"
    ), "Failed with response: " + str(res.json())
    logger.info(
        "\n ======= Visitor has checked manual invitation and got the invitation & chatguid ======="
    )
    res_check_manual_invitation = res
    chat_guid = res_check_manual_invitation.json()[0]["payload"]["chat"]["guid"]

    # pdb.set_trace()
    yield (
        res_check_manual_invitation,
        res_new_visitor,
        visitor_ashx_url,
        visitor_guid,
        visitor_session_id,
        campaign_id,
        chat_guid,
    )


@pytest.fixture(scope="function")
def visitor_check_auto_invitation(
    login,
    update_campaign_add_auto_invitation,
    generate_visitor_insite,
):
    login_data = login
    site_id = login_data["site_id"]

    (
        res_new_visitor,
        visitor_guid,
        visitor_session_id,
        campaign_id,
        visitor_ashx_url,
    ) = generate_visitor_insite

    #  ======= visitor checks auto invitation and makes sure it's invited =======

    req_body = [
        {
            "type": "checkAutoInvitation",
            "campaignId": campaign_id,
            "chatVersion": "",
            "sessionId": visitor_session_id,
            "ssoSessionToken": "",
            "id": 15,
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
        res.json()[0]["type"] == "checkAutoInvitation"
    ), "Failed with response: " + str(res.json())
    assert res.json()[0]["payload"][0]["delay"] == 0, "Failed with response: " + str(
        res.json()
    )
    logger.info(
        "\n ======= Visitor has checked auto invitation and made sure it's invited and got the auto_invitation_id  ======="
    )
    res_visitor_check_auto_invitation = res
    auto_invitation_id = update_campaign_add_auto_invitation.json()["id"]

    # pdb.set_trace()
    yield (
        res_visitor_check_auto_invitation,
        res_new_visitor,
        visitor_ashx_url,
        visitor_guid,
        visitor_session_id,
        campaign_id,
        auto_invitation_id,
    )


@pytest.fixture(scope="function")
def visitor_confirm_auto_invitation(
    login, login_agent_console_new, visitor_check_auto_invitation
):
    (
        res_visitor_check_auto_invitation,
        res_new_visitor,
        visitor_ashx_url,
        visitor_guid,
        visitor_session_id,
        campaign_id,
        auto_invitation_id,
    ) = visitor_check_auto_invitation

    request_body = [
        {
            "type": "confirmAutoInvitation",
            "chatVersion": "",
            "invitationId": auto_invitation_id,
            "sessionId": visitor_session_id,
            "id": 5,
        },
    ]

    # pdb.set_trace()
    res = send_request(
        visitor_ashx_url,
        None,
        "POST",
        None,
        None,
        request_body,
    )

    assert res.status_code == 200, (
        "Failed with status code: "
        + str(res.status_code)
        + " and response: "
        + str(res.json())
    )
    assert (
        res.json()[0]["type"] == "confirmAutoInvitation"
    ), "Failed with response: " + str(res.json())
    logger.info(
        "\n ======= Visitor side has poped up the autoinvitation window ======="
    )

    invitation_type = res.json()[0]["payload"]["type"]
    invitation_id = res.json()[0]["payload"]["id"]

    res_confirm_auto_invitation = res

    yield (
        res_new_visitor,
        res_confirm_auto_invitation,
        visitor_ashx_url,
        visitor_guid,
        visitor_session_id,
        campaign_id,
        invitation_type,
        invitation_id,
    )


@pytest.fixture(scope="function")
def visitor_set_custom_variable(
    login,
    init_custom_variable,
    generate_visitor_insite,
):
    login_data = login
    site_id = login_data["site_id"]
    custom_variable_name = init_custom_variable.json()["name"]

    (
        res_new_visitor,
        visitor_guid,
        visitor_session_id,
        campaign_id,
        visitor_ashx_url,
    ) = generate_visitor_insite

    #  ======= visitor set custom variable =======

    req_body = [
        {
            "type": "setCustomVariables",
            "customVariables": {custom_variable_name: "temp cv value, sanity test"},
            "campaignId": campaign_id,
            "chatVersion": "",
            "sessionId": visitor_session_id,
            "ssoSessionToken": "",
            "id": 15,
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
        res.json()[0]["type"] == "setCustomVariables"
    ), "Failed with response: " + str(res.json())
    logger.info("\n ======= Visitor has set custom variable.  =======")
    res_visitor_set_custom_variable = res

    # pdb.set_trace()
    yield (
        res_visitor_set_custom_variable,
        res_new_visitor,
        visitor_ashx_url,
        visitor_guid,
        visitor_session_id,
        campaign_id,
    )


@pytest.fixture(scope="function")
def visitor_submit_pre_chat(
    login, update_campaign_enable_pre_chat, visitor_new_visitor
):
    login_data = login
    site_id = login_data["site_id"]

    (
        res_new_visitor,
        visitor_guid,
        visitor_session_id,
        campaign_id,
        visitor_ashx_url,
    ) = visitor_new_visitor

    #  ======= visitor submit pre-chat =======

    req_body = [
        {
            "type": "submitPrechat",
            "form": {
                "name": "temp visitor",
                "email": "tempvisitor@mail.com",
                "department": "",
                "phone": "13900000000",
                "company": "temp company",
                "product": "Knowledge Base",
            },
            "campaignId": campaign_id,
            "sessionId": visitor_session_id,
            "ssoSessionToken": "",
            "id": 55,
        }
    ]

    # pdb.set_trace()
    res_submit_pre_chat = send_request(
        visitor_ashx_url,
        None,
        "POST",
        None,
        None,
        req_body,
    )
    # pdb.set_trace()
    assert res_submit_pre_chat.status_code == 200, (
        "Failed with status code: "
        + str(res_submit_pre_chat.status_code)
        + " and response: "
        + str(res_submit_pre_chat.json())
    )
    assert (
        res_submit_pre_chat.json()[0]["type"] == "submitPrechat"
    ), "Failed with response: " + str(res_submit_pre_chat.json())
    logger.info("\n ======= Visitor has submitted pre-chat =======")

    yield (
        res_submit_pre_chat,
        res_new_visitor,
        visitor_ashx_url,
        visitor_guid,
        visitor_session_id,
        campaign_id,
    )


@pytest.fixture(scope="function")
def visitor_submit_pre_chat_with_department(
    login,
    init_2departments,
    update_campaign_pre_chat_enable_all_fields,
    visitor_new_visitor,
):
    login_data = login
    site_id = login_data["site_id"]
    (create_department, create_2nd_department, department1_id, department2_id) = (
        init_2departments
    )
    # pdb.set_trace()
    (
        res_new_visitor,
        visitor_guid,
        visitor_session_id,
        campaign_id,
        visitor_ashx_url,
    ) = visitor_new_visitor

    #  ======= visitor submit pre-chat with department =======

    req_body = [
        {
            "type": "submitPrechat",
            "form": {
                "name": "temp visitor",
                "email": "tempvisitor@mail.com",
                "department": department1_id,
                "phone": "13900000000",
                "company": "temp company",
                "product": "Knowledge Base",
            },
            "campaignId": campaign_id,
            "sessionId": visitor_session_id,
            "ssoSessionToken": "",
            "id": 55,
        }
    ]

    # pdb.set_trace()
    res_submit_pre_chat = send_request(
        visitor_ashx_url,
        None,
        "POST",
        None,
        None,
        req_body,
    )
    # pdb.set_trace()
    assert res_submit_pre_chat.status_code == 200, (
        "Failed with status code: "
        + str(res_submit_pre_chat.status_code)
        + " and response: "
        + str(res_submit_pre_chat.json())
    )
    assert (
        res_submit_pre_chat.json()[0]["type"] == "submitPrechat"
    ), "Failed with response: " + str(res_submit_pre_chat.json())
    logger.info("\n ======= Visitor has submitted pre-chat with department =======")

    yield (
        res_submit_pre_chat,
        res_new_visitor,
        visitor_ashx_url,
        visitor_guid,
        visitor_session_id,
        campaign_id,
    )


@pytest.fixture(scope="function")
def visitor_submit_pre_chat_with_all_fields(
    login, update_campaign_pre_chat_enable_all_fields, visitor_new_visitor
):
    login_data = login
    site_id = login_data["site_id"]
    pre_chat_form_fields = update_campaign_pre_chat_enable_all_fields.json()[
        "preChatFormFields"
    ]
    # pdb.set_trace()

    (
        res_new_visitor,
        visitor_guid,
        visitor_session_id,
        campaign_id,
        visitor_ashx_url,
    ) = visitor_new_visitor

    #  ======= visitor submit pre-chat =======

    req_body = [
        {
            "type": "submitPrechat",
            "form": {
                "name": "temp visitor",
                "email": "tempvisitor@mail.com",
                "department": "",
                "phone": "123456",
                "company": "temp Inc.",
                "product": "KnowledgeBase",
                "custom": {
                    pre_chat_form_fields[6]["id"]: "temp text field value",
                    pre_chat_form_fields[7][
                        "id"
                    ]: "temp textArea field value\nmultiple lines",
                    pre_chat_form_fields[8]["id"]: "rb1",
                    pre_chat_form_fields[9]["id"]: "true",
                    pre_chat_form_fields[10]["id"]: "ddl1",
                    pre_chat_form_fields[11]["id"]: "cbl1⊙cbl2",
                },
            },
            "campaignId": campaign_id,
            "sessionId": visitor_session_id,
            "ssoSessionToken": "",
            "id": 55,
        }
    ]

    # pdb.set_trace()

    # wait for updates made to campaign reflected in chat server cache as interval is 5s, before sending submit_pre_chat request
    time.sleep(6)
    res_submit_pre_chat = send_request(
        visitor_ashx_url,
        None,
        "POST",
        None,
        None,
        req_body,
    )
    # pdb.set_trace()
    assert res_submit_pre_chat.status_code == 200, (
        "Failed with status code: "
        + str(res_submit_pre_chat.status_code)
        + " and response: "
        + str(res_submit_pre_chat.json())
    )
    assert (
        res_submit_pre_chat.json()[0]["type"] == "submitPrechat"
    ), "Failed with response: " + str(res_submit_pre_chat.json())
    logger.info("\n ======= Visitor has submitted pre-chat with all fields =======")

    yield (
        res_submit_pre_chat,
        res_new_visitor,
        visitor_ashx_url,
        visitor_guid,
        visitor_session_id,
        campaign_id,
    )


@pytest.fixture(scope="function")
def visitor_submit_pre_chat_with_all_fields_left_emtpy(
    login, update_campaign_pre_chat_enable_all_fields, visitor_new_visitor
):
    """所有字段都为空, 提交了prechat。可以用于chat_search测试 rabiobox, dropdownlist为空，checkbox、checkboxlist为false的场景。"""
    # teamtodo - 需要补充这种场景
    pass


@pytest.fixture(scope="function")
def visitor_submit_post_chat_with_all_fields(
    login, update_campaign_post_chat_enable_all_fields, visitor_end_chat
):
    login_data = login
    site_id = login_data["site_id"]
    post_chat_form_fields = update_campaign_post_chat_enable_all_fields.json()[
        "postChatFormFields"
    ]
    # pdb.set_trace()

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

    #  ======= visitor submit post-chat =======

    req_body = [
        {
            "type": "submitPostChat",
            "chatGuid": chat_guid,
            "form": {
                "rating": "0",
                "comment": "0 star service",
                "custom": {
                    post_chat_form_fields[2]["id"]: "temp text field value",
                    post_chat_form_fields[3][
                        "id"
                    ]: "temp textArea field value\nmultiple lines",
                    post_chat_form_fields[4]["id"]: "rb1",
                    post_chat_form_fields[5]["id"]: "true",
                    post_chat_form_fields[6]["id"]: "ddl1",
                    post_chat_form_fields[7]["id"]: "cbl1⊙cbl2",
                },
            },
            "sessionId": visitor_session_id,
            "ssoSessionToken": "",
            "id": 55,
        }
    ]

    # pdb.set_trace()

    # wait for updates made to campaign reflected in chat server cache as interval is 5s, before sending submit_post_chat request
    time.sleep(6)
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
    assert res.json()[0]["type"] == "submitPostChat", "Failed with response: " + str(
        res.json()
    )
    logger.info("\n ======= Visitor has submitted post-chat with all fields =======")

    res_submit_post_chat = res
    yield (
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
    )


@pytest.fixture(scope="function")
def visitor_submit_post_chat_with_only_rating(
    login, update_campaign_enable_post_chat, visitor_end_chat
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

    #  ======= visitor submit post-chat with only rating =======

    req_body = [
        {
            "type": "submitPostChat",
            "chatGuid": chat_guid,
            "form": {
                "rating": "3",
                "comment": "3 star service",
                "custom": {},
            },
            "sessionId": visitor_session_id,
            "ssoSessionToken": "",
            "id": 55,
        }
    ]

    # pdb.set_trace()

    # wait for updates made to campaign reflected in chat server cache as interval is 5s, before sending submit_post_chat request
    time.sleep(6)
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
    assert res.json()[0]["type"] == "submitPostChat", "Failed with response: " + str(
        res.json()
    )
    logger.info("\n ======= Visitor has submitted post-chat with only rating. =======")

    res_submit_post_chat = res
    yield (
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
    )


@pytest.fixture(scope="function")
def visitor_request_chat_go_to_pre_chat(
    login, update_campaign_enable_pre_chat, visitor_new_visitor
):
    login_data = login
    site_id = login_data["site_id"]

    (
        res_new_visitor,
        visitor_guid,
        visitor_session_id,
        campaign_id,
        visitor_ashx_url,
    ) = visitor_new_visitor

    #  ======= visitor request chat =======

    request_body_request_chat = [
        {
            "type": "requestChat",
            "campaignId": campaign_id,
            "source": {
                "type": "button",
                "page": {
                    "url": f"https://www.baidu.com/",
                    "title": "Baidu",
                },
            },
            "isPrechatDone": False,
            "isSupportWebrtc": True,
            "isProcessingDone": False,
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
    logger.info(
        "\n ======= Visitor has requested to chat and now in pre-chat status. ======="
    )

    yield (
        res_new_visitor,
        res_request_chat,
        visitor_ashx_url,
        visitor_guid,
        visitor_session_id,
        campaign_id,
    )


@pytest.fixture(scope="function")
def visitor_request_chat_no_pre_chat_go_to_system_processing(
    login, visitor_new_visitor
):
    login_data = login
    site_id = login_data["site_id"]

    (
        res_new_visitor,
        visitor_guid,
        visitor_session_id,
        campaign_id,
        visitor_ashx_url,
    ) = visitor_new_visitor

    #  ======= visitor request chat with isProcessingDone=False =======

    request_body_request_chat = [
        {
            "type": "requestChat",
            "campaignId": campaign_id,
            "source": {
                "type": "button",
                "page": {
                    "url": f"https://www.baidu.com/",
                    "title": "Baidu",
                },
            },
            "isPrechatDone": False,
            "isSupportWebrtc": True,
            "isProcessingDone": False,
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
    assert (
        res_request_chat.json()[0]["payload"]["next"] == "systemProcessing"
    ), "Failed with response: " + str(res_request_chat.json())
    logger.info(
        "\n ======= Visitor has requested to chat and now is in systemProcessing status. ======="
    )

    yield (
        res_new_visitor,
        res_request_chat,
        visitor_ashx_url,
        visitor_guid,
        visitor_session_id,
        campaign_id,
    )


@pytest.fixture(scope="function")
def visitor_request_chat_with_pre_chat_go_to_system_processing(
    login, visitor_new_visitor
):
    """这个fixture用在集成了salesforce,bot,taskbot,dynamic365的请求下的聊天请求"""
    login_data = login
    site_id = login_data["site_id"]

    (
        res_new_visitor,
        visitor_guid,
        visitor_session_id,
        campaign_id,
        visitor_ashx_url,
    ) = visitor_new_visitor

    #  ======= visitor request chat with isProcessingDone=False =======

    request_body_request_chat = [
        {
            "type": "requestChat",
            "campaignId": campaign_id,
            "source": {
                "type": "button",
                "page": {
                    "url": f"https://www.baidu.com/",
                    "title": "Baidu",
                },
            },
            "isPrechatDone": True,
            "isSupportWebrtc": True,
            "isProcessingDone": False,
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
    assert (
        res_request_chat.json()[0]["payload"]["next"] == "systemProcessing"
    ), "Failed with response: " + str(res_request_chat.json())
    logger.info(
        "\n ======= Visitor has requested to chat and now is in systemProcessing status. ======="
    )

    yield (
        res_new_visitor,
        res_request_chat,
        visitor_ashx_url,
        visitor_guid,
        visitor_session_id,
        campaign_id,
    )


@pytest.fixture(scope="function")
def visitor_request_chat_with_pre_chat_go_to_chat(login, visitor_new_visitor):
    """这个fixture用在未集成salesforce,bot,taskbot,dynamic365的请求下的聊天请求"""
    login_data = login
    site_id = login_data["site_id"]

    (
        res_new_visitor,
        visitor_guid,
        visitor_session_id,
        campaign_id,
        visitor_ashx_url,
    ) = visitor_new_visitor

    #  ======= visitor request chat with isProcessingDone=False =======

    request_body_request_chat = [
        {
            "type": "requestChat",
            "campaignId": campaign_id,
            "source": {
                "type": "button",
                "page": {
                    "url": f"https://www.baidu.com/",
                    "title": "Baidu",
                },
            },
            "isPrechatDone": True,
            "isSupportWebrtc": True,
            "isProcessingDone": False,
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
    assert (
        res_request_chat.json()[0]["payload"]["next"] == "chat"
    ), "Failed with response: " + str(res_request_chat.json())
    logger.info(
        "\n ======= Visitor has requested to chat and now is in chat status. ======="
    )

    yield (
        res_new_visitor,
        res_request_chat,
        visitor_ashx_url,
        visitor_guid,
        visitor_session_id,
        campaign_id,
    )


@pytest.fixture(scope="function")
def visitor_request_chat(login, visitor_new_visitor):
    login_data = login
    site_id = login_data["site_id"]

    (
        res_new_visitor,
        visitor_guid,
        visitor_session_id,
        campaign_id,
        visitor_ashx_url,
    ) = visitor_new_visitor

    #  ======= visitor request chat =======

    request_body_request_chat = [
        {
            "type": "requestChat",
            "campaignId": campaign_id,
            "source": {
                "type": "button",
                "page": {
                    "url": f"https://www.baidu.com/",
                    "title": "Baidu",
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
    logger.info("\n ======= Visitor has requested to chat =======")

    chat_guid = res_request_chat.json()[0]["payload"]["chatGuid"]

    yield (
        res_new_visitor,
        res_request_chat,
        visitor_ashx_url,
        visitor_guid,
        visitor_session_id,
        campaign_id,
        chat_guid,
    )


@pytest.fixture(scope="function")
def visitor_request_chat_from_manual_invitation(
    login, visitor_check_manual_invitation_after_agent_invite
):
    (
        res_check_manual_invitation,
        res_new_visitor,
        visitor_ashx_url,
        visitor_guid,
        visitor_session_id,
        campaign_id,
        chat_guid,
    ) = visitor_check_manual_invitation_after_agent_invite

    message_guid = str(uuid.uuid4())

    #  ======= visitor request chat =======

    request_body = [
        {
            "type": "batchAction",
            "actions": [
                {
                    "type": "requestChat",
                    "campaignId": campaign_id,
                    "source": {
                        "invitationType": "bubble",
                        "type": "manualInvitation",
                        "page": {
                            "url": f"https://www.baidu.com/",
                            "title": "Baidu",
                        },
                    },
                    "isPrechatDone": False,
                    "isSupportWebrtc": True,
                    "lastChattedAgents": [],
                    "chatVersion": "",
                    "sessionId": visitor_session_id,
                },
                {
                    "type": "sendChatMessages",
                    "chatGuid": chat_guid,
                    "messages": [
                        {
                            "content": "5oiR5pyJ5LiA5Liq5b6I5Lil6YeN55qE6Zeu6aKY",  # 消息是：我有一个很严重的问题
                            "encoding": "base64",
                            "type": "visitorAddTextMessage",
                            "guid": message_guid,
                            "sender": {"type": "visitor"},
                            "isPassword": False,
                            "quickReplyNextActionId": "00000000-0000-0000-0000-000000000000",
                        }
                    ],
                    "chatVersion": "",
                    "sessionId": visitor_session_id,
                },
                {
                    "type": "getChatMessages",
                    "chatGuid": chat_guid,
                    "fromId": 0,
                    "chatVersion": "",
                    "sessionId": visitor_session_id,
                },
            ],
            "ssoSessionToken": "",
            "id": 66,
        }
    ]

    # pdb.set_trace()
    res = send_request(
        visitor_ashx_url,
        None,
        "POST",
        None,
        None,
        request_body,
    )
    # pdb.set_trace()
    assert res.status_code == 200, (
        "Failed with status code: "
        + str(res.status_code)
        + " and response: "
        + str(res.json())
    )

    assert (
        res.json()[0]["payload"][0]["type"] == "requestChat"
    ), "Failed with response: " + str(res.json())
    logger.info(
        "\n ======= Visitor has requested to chat and chat will auto started from manual invitation ======="
    )

    res_chat_from_manual_invitation = res

    yield (
        res_new_visitor,
        res_chat_from_manual_invitation,
        visitor_ashx_url,
        visitor_guid,
        visitor_session_id,
        campaign_id,
        chat_guid,
    )


@pytest.fixture(scope="function")
def visitor_request_chat_from_auto_invitation(login, visitor_confirm_auto_invitation):
    (
        res_new_visitor,
        res_confirm_auto_invitation,
        visitor_ashx_url,
        visitor_guid,
        visitor_session_id,
        campaign_id,
        invitation_type,
        invitation_id,
    ) = visitor_confirm_auto_invitation

    #  ======= visitor request chat from auto invitation =======

    request_body = [
        {
            "type": "requestChat",
            "campaignId": campaign_id,
            "source": {
                "invitationId": invitation_id,
                "invitationType": invitation_type,
                "page": {
                    "url": f"https://www.baidu.com/",
                    "title": "Baidu",
                },
                "type": "autoInvitation",
            },
            "isPrechatDone": False,
            "isSupportWebrtc": True,
            "lastChattedAgents": [],
            "chatVersion": "",
            "sessionId": visitor_session_id,
        },
    ]

    # pdb.set_trace()
    res = send_request(
        visitor_ashx_url,
        None,
        "POST",
        None,
        None,
        request_body,
    )
    # pdb.set_trace()
    assert res.status_code == 200, (
        "Failed with status code: "
        + str(res.status_code)
        + " and response: "
        + str(res.json())
    )
    assert res.json()[0]["type"] == "requestChat", "Failed with response: " + str(
        res.json()
    )
    logger.info("\n ======= Visitor has requested to chat from auto invitation =======")

    chat_guid = res.json()[0]["payload"]["chatGuid"]

    res_chat_from_auto_invitation = res

    yield (
        res_new_visitor,
        res_chat_from_auto_invitation,
        visitor_ashx_url,
        visitor_guid,
        visitor_session_id,
        campaign_id,
        chat_guid,
    )


@pytest.fixture(scope="function")
def visitor_end_chat(agent_accept_chat):
    """这个方法是在agent_accept_chat fixture之后调用的，不需要传入chat_guid。适用于LiveChatHistory中，也被用于visitor_end_chat_with_teardown中。"""

    def _visitor_end_chat():
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
        logger.info("\n ======= Visitor has ended the chat. =======")
        return (
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
        )

    yield _visitor_end_chat


@pytest.fixture(scope="function")
def visitor_end_chat_solo_action(login, generate_visitor_insite):
    """这个方法是solo action, 没有调用前面的visitor_request_chat或者agent_accept_chat fixture. 需要传入chat_guid。适用于想要调用visitor_end_chat的场景，但是不想要调用visitor_request_chat或者agent_accept_chat的场景。"""
    login_data = login
    site_id = login_data["site_id"]

    (
        res_new_visitor,
        visitor_guid,
        visitor_session_id,
        campaign_id,
        visitor_ashx_url,
    ) = generate_visitor_insite

    def _visitor_end_chat_solo_action(chat_guid):
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
        logger.info("\n ======= Visitor has ended the chat. =======")
        return (
            res_end_chat,
            res_new_visitor,
            visitor_guid,
            visitor_session_id,
            campaign_id,
            visitor_ashx_url,
        )

    yield _visitor_end_chat_solo_action


@pytest.fixture(scope="function")
def visitor_end_chat_with_teardown(
    generate_visitor_insite,
    login_agent_console_new,
    visitor_request_chat,
    visitor_end_chat,
    save_and_delete_chat,
):
    """这个方法是带teardown的。应用于chatserver其他fixture中，用于结束聊天并确保聊天被删除。"""
    (
        res_new_visitor,
        res_request_chat,
        visitor_ashx_url,
        visitor_guid,
        visitor_session_id,
        campaign_id,
        chat_guid,
    ) = visitor_request_chat

    def _visitor_end_chat_with_teardown():
        visitor_end_chat()
        logger.info("\n ======= Now we have a chat-ended visitor. =======")
        return (
            res_new_visitor,
            res_request_chat,
            visitor_ashx_url,
            visitor_guid,
            visitor_session_id,
            campaign_id,
            chat_guid,
        )

    yield _visitor_end_chat_with_teardown
    # pdb.set_trace()
    # 要去调用 save_and_delete_chat fixture, 来确认chat已保存，并最终删除chat
    save_and_delete_chat(chat_guid)


@pytest.fixture(scope="function")
def visitor_end_waiting_chat(visitor_request_chat):
    def _visitor_end_waiting_chat():
        (
            res_new_visitor,
            res_request_chat,
            visitor_ashx_url,
            visitor_guid,
            visitor_session_id,
            campaign_id,
            chat_guid,
        ) = visitor_request_chat
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
        logger.info("\n ======= Visitor has ended the waiting chat. =======")
        return (
            res_end_chat,
            res_new_visitor,
            res_request_chat,
            visitor_ashx_url,
            visitor_guid,
            visitor_session_id,
            campaign_id,
            chat_guid,
        )

    yield _visitor_end_waiting_chat


@pytest.fixture(scope="function")
def visitor_get_initial_messages(agent_accept_chat):
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

    #  ======= visitor get initial messages =======

    req_body_get_initial_messages = [
        {
            "type": "getChatMessages",
            "chatGuid": chat_guid,
            "chatVersion": "",
            "fromId": -1,
            "sessionId": visitor_session_id,
        },
    ]

    # pdb.set_trace()
    res_get_initial_messages = send_request(
        visitor_ashx_url,
        None,
        "POST",
        None,
        None,
        req_body_get_initial_messages,
    )
    # pdb.set_trace()
    assert res_get_initial_messages.status_code == 200, (
        "Failed with status code: "
        + str(res_get_initial_messages.status_code)
        + " and response: "
        + str(res_get_initial_messages.json())
    )
    assert (
        res_get_initial_messages.json()[0]["type"] == "getChatMessages"
    ), "Failed with response: " + str(res_get_initial_messages.json())
    logger.info("\n ======= visitor has got first few messages =======")

    visitor_chat_version = res_get_initial_messages.json()[0]["payload"][-1]["guid"]
    visitor_chat_version_from_id = res_get_initial_messages.json()[0]["payload"][-1][
        "id"
    ]

    yield (
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
    )


@pytest.fixture(scope="function")
def visitor_get_initial_messages_solo_action(visitor_request_chat):
    """这个方法不需要调用agent_accept_chat，适用于跟Agent没有关系的chatbot聊天"""
    (
        res_new_visitor,
        res_request_chat,
        visitor_ashx_url,
        visitor_guid,
        visitor_session_id,
        campaign_id,
        chat_guid,
    ) = visitor_request_chat

    #  ======= visitor get initial messages =======

    req_body = [
        {
            "type": "getChatMessages",
            "chatGuid": chat_guid,
            "chatVersion": "",
            "fromId": -1,
            "sessionId": visitor_session_id,
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
    assert res.json()[0]["type"] == "getChatMessages", "Failed with response: " + str(
        res.json()
    )
    logger.info("\n ======= visitor has got first few messages =======")

    visitor_chat_version = res.json()[0]["payload"][-1]["guid"]
    visitor_chat_version_from_id = res.json()[0]["payload"][-1]["id"]
    res_get_initial_messages = res

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


@pytest.fixture(scope="function")
def visitor_get_latest_messages(visitor_get_initial_messages):
    (
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
    ) = visitor_get_initial_messages

    #  ======= visitor get latest messages =======

    req_body = [
        {
            "type": "getChatMessages",
            "chatGuid": chat_guid,
            "chatVersion": visitor_chat_version,
            "fromId": visitor_chat_version_from_id,
            "sessionId": visitor_session_id,
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
    assert res.json()[0]["type"] == "getChatMessages", "Failed with response: " + str(
        res.json()
    )
    logger.info("\n ======= visitor has got latest messages. =======")

    visitor_chat_version = res.json()[0]["payload"][-1]["guid"]
    visitor_chat_version_from_id = res.json()[0]["payload"][-1]["id"]

    res_visitor_get_latest_messages = res

    yield (
        res_visitor_get_latest_messages,
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
    )


@pytest.fixture(scope="function")
def visitor_get_latest_messages_solo_action(generate_visitor_insite):
    """这个方法是solo action, 没有调用前面的visitor_request_chat或者visitor_get_initial_messages fixture. 需要传入chat_guid, visitor_chat_version, visitor_chat_version_from_id。适用于想要从某一个chat_version开始获取最新的messages."""

    (
        res_new_visitor,
        visitor_guid,
        visitor_session_id,
        campaign_id,
        visitor_ashx_url,
    ) = generate_visitor_insite

    def _visitor_get_latest_messages_solo_action(
        chat_guid, visitor_chat_version, visitor_chat_version_from_id
    ):

        #  ======= visitor get latest messages =======

        req_body = [
            {
                "type": "getChatMessages",
                "chatGuid": chat_guid,
                "chatVersion": visitor_chat_version,
                "fromId": visitor_chat_version_from_id,
                "sessionId": visitor_session_id,
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
            res.json()[0]["type"] == "getChatMessages"
        ), "Failed with response: " + str(res.json())
        logger.info("\n ======= visitor has got latest messages. =======")

        # check if there are messages in the response, if yes, update visitor_chat_version and visitor_chat_version_from_id
        if len(res.json()[0]["payload"]) > 0:
            visitor_chat_version = res.json()[0]["payload"][-1]["guid"]
            visitor_chat_version_from_id = res.json()[0]["payload"][-1]["id"]

        res_visitor_get_latest_messages = res

        return (
            res_visitor_get_latest_messages,
            res_new_visitor,
            visitor_ashx_url,
            visitor_guid,
            visitor_session_id,
            campaign_id,
            chat_guid,
            visitor_chat_version,
            visitor_chat_version_from_id,
        )

    yield _visitor_get_latest_messages_solo_action


@pytest.fixture(scope="function")
def visitor_send_text_message(visitor_get_initial_messages):
    (
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
    ) = visitor_get_initial_messages

    #  ======= visitor send text message =======
    message_guid = str(uuid.uuid4())

    req_body = [
        {
            "type": "batchAction",
            "actions": [
                {
                    "type": "sendChatMessages",
                    "chatGuid": chat_guid,
                    "messages": [
                        {
                            "content": "5oiR5pyJ5LiA5Liq5b6I5Lil6YeN55qE6Zeu6aKY",  # 消息是：我有一个很严重的问题
                            "encoding": "base64",
                            "type": "visitorAddTextMessage",
                            "guid": message_guid,
                            "sender": {"type": "visitor"},
                            "isPassword": False,
                            "quickReplyNextActionId": "00000000-0000-0000-0000-000000000000",
                        }
                    ],
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
            "id": 88,
        }
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
        res.json()[0]["payload"][0]["type"] == "sendChatMessages"
    ), "Failed with response: " + str(res.json())
    logger.info("\n ======= visitor has sent a chinese text message. =======")

    # update visitor latest chat version
    visitor_chat_version = res.json()[0]["payload"][1]["payload"][-1]["guid"]
    visitor_chat_version_from_id = res.json()[0]["payload"][1]["payload"][-1]["id"]

    res_visitor_send_text_message = res
    # pdb.set_trace()

    yield (
        res_visitor_send_text_message,
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
    )


@pytest.fixture(scope="function")
def visitor_send_very_negative_text_message(visitor_get_initial_messages):
    (
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
    ) = visitor_get_initial_messages

    #  ======= visitor send text message =======
    message_guid = str(uuid.uuid4())

    req_body = [
        {
            "type": "batchAction",
            "actions": [
                {
                    "type": "sendChatMessages",
                    "chatGuid": chat_guid,
                    "messages": [
                        {
                            "content": "SSBhbSBleHRyZW1lbHkgYW5ncnkgYW5kIGRlZXBseSBvdXRyYWdlZCBieSBob3cgYmFkbHkgdGhpcyBoYXMgZ29uZS4=",  # I am extremely angry and deeply outraged by how badly this has gone.
                            "encoding": "base64",
                            "type": "visitorAddTextMessage",
                            "guid": message_guid,
                            "sender": {"type": "visitor"},
                            "isPassword": False,
                            "quickReplyNextActionId": "00000000-0000-0000-0000-000000000000",
                        }
                    ],
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
            "id": 88,
        }
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
        res.json()[0]["payload"][0]["type"] == "sendChatMessages"
    ), "Failed with response: " + str(res.json())
    logger.info("\n ======= visitor has sent a very negative text message. =======")

    res_visitor_send_text_message = res
    # pdb.set_trace()

    # update visitor latest chat version
    if res.json()[0]["payload"][1]["payload"]:
        visitor_chat_version = res.json()[0]["payload"][1]["payload"][-1]["guid"]
        visitor_chat_version_from_id = res.json()[0]["payload"][1]["payload"][-1]["id"]

    yield (
        res_visitor_send_text_message,
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
    )


@pytest.fixture(scope="function")
def visitor_send_negative_text_message(visitor_get_initial_messages):
    (
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
    ) = visitor_get_initial_messages

    #  ======= visitor send text message =======
    message_guid = str(uuid.uuid4())

    req_body = [
        {
            "type": "batchAction",
            "actions": [
                {
                    "type": "sendChatMessages",
                    "chatGuid": chat_guid,
                    "messages": [
                        {
                            "content": "SSBhbSBzYWQu",  # I am sad.
                            "encoding": "base64",
                            "type": "visitorAddTextMessage",
                            "guid": message_guid,
                            "sender": {"type": "visitor"},
                            "isPassword": False,
                            "quickReplyNextActionId": "00000000-0000-0000-0000-000000000000",
                        }
                    ],
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
            "id": 88,
        }
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
        res.json()[0]["payload"][0]["type"] == "sendChatMessages"
    ), "Failed with response: " + str(res.json())
    logger.info("\n ======= visitor has sent a negative text message. =======")

    res_visitor_send_text_message = res
    # pdb.set_trace()

    # update visitor latest chat version
    if res.json()[0]["payload"][1]["payload"]:
        visitor_chat_version = res.json()[0]["payload"][1]["payload"][-1]["guid"]
        visitor_chat_version_from_id = res.json()[0]["payload"][1]["payload"][-1]["id"]

    yield (
        res_visitor_send_text_message,
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
    )


@pytest.fixture(scope="function")
def visitor_send_neutral_text_message(visitor_get_initial_messages):
    (
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
    ) = visitor_get_initial_messages

    #  ======= visitor send text message =======
    message_guid = str(uuid.uuid4())

    req_body = [
        {
            "type": "batchAction",
            "actions": [
                {
                    "type": "sendChatMessages",
                    "chatGuid": chat_guid,
                    "messages": [
                        {
                            "content": "aGVsbG8=",  # hello
                            "encoding": "base64",
                            "type": "visitorAddTextMessage",
                            "guid": message_guid,
                            "sender": {"type": "visitor"},
                            "isPassword": False,
                            "quickReplyNextActionId": "00000000-0000-0000-0000-000000000000",
                        }
                    ],
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
            "id": 88,
        }
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
        res.json()[0]["payload"][0]["type"] == "sendChatMessages"
    ), "Failed with response: " + str(res.json())
    logger.info("\n ======= visitor has sent a neutral text message. =======")

    res_visitor_send_text_message = res
    # pdb.set_trace()

    # update visitor latest chat version
    if res.json()[0]["payload"][1]["payload"]:
        visitor_chat_version = res.json()[0]["payload"][1]["payload"][-1]["guid"]
        visitor_chat_version_from_id = res.json()[0]["payload"][1]["payload"][-1]["id"]

    yield (
        res_visitor_send_text_message,
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
    )


@pytest.fixture(scope="function")
def visitor_send_positive_text_message(visitor_get_initial_messages):
    (
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
    ) = visitor_get_initial_messages

    #  ======= visitor send text message =======
    message_guid = str(uuid.uuid4())

    req_body = [
        {
            "type": "batchAction",
            "actions": [
                {
                    "type": "sendChatMessages",
                    "chatGuid": chat_guid,
                    "messages": [
                        {
                            "content": "SSBhbSBoYXBweSB3aXRoIGhvdyB0aGluZ3MgYXJlIGdvaW5nLg==",  # I am happy with how things are going.
                            "encoding": "base64",
                            "type": "visitorAddTextMessage",
                            "guid": message_guid,
                            "sender": {"type": "visitor"},
                            "isPassword": False,
                            "quickReplyNextActionId": "00000000-0000-0000-0000-000000000000",
                        }
                    ],
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
            "id": 88,
        }
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
        res.json()[0]["payload"][0]["type"] == "sendChatMessages"
    ), "Failed with response: " + str(res.json())
    logger.info("\n ======= visitor has sent a positive text message. =======")

    res_visitor_send_text_message = res
    # pdb.set_trace()

    # update visitor latest chat version
    if res.json()[0]["payload"][1]["payload"]:
        visitor_chat_version = res.json()[0]["payload"][1]["payload"][-1]["guid"]
        visitor_chat_version_from_id = res.json()[0]["payload"][1]["payload"][-1]["id"]

    yield (
        res_visitor_send_text_message,
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
    )


@pytest.fixture(scope="function")
def visitor_send_very_positive_text_message(visitor_get_initial_messages):
    (
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
    ) = visitor_get_initial_messages

    #  ======= visitor send text message =======
    message_guid = str(uuid.uuid4())
    very_positive_text_message = "SSBhbSB2ZXJ5IGhhcHB5IGFuZCBpbmNyZWRpYmx5IGdyYXRlZnVsIGZvciB0aGlzIGFtYXppbmcgb3Bwb3J0dW5pdHkh"  # I am very happy and incredibly grateful for this amazing opportunity!
    req_body = [
        {
            "type": "batchAction",
            "actions": [
                {
                    "type": "sendChatMessages",
                    "chatGuid": chat_guid,
                    "messages": [
                        {
                            "content": very_positive_text_message,
                            "encoding": "base64",
                            "type": "visitorAddTextMessage",
                            "guid": message_guid,
                            "sender": {"type": "visitor"},
                            "isPassword": False,
                            "quickReplyNextActionId": "00000000-0000-0000-0000-000000000000",
                        }
                    ],
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
            "id": 88,
        }
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
        res.json()[0]["payload"][0]["type"] == "sendChatMessages"
    ), "Failed with response: " + str(res.json())
    logger.info("\n ======= visitor has sent a very positive text message. =======")

    res_visitor_send_text_message = res
    # pdb.set_trace()

    # update visitor latest chat version
    if res.json()[0]["payload"][1]["payload"]:
        visitor_chat_version = res.json()[0]["payload"][1]["payload"][-1]["guid"]
        visitor_chat_version_from_id = res.json()[0]["payload"][1]["payload"][-1]["id"]

    yield (
        res_visitor_send_text_message,
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
        message_guid,
        very_positive_text_message,
        visitor_chat_version,
        visitor_chat_version_from_id,
    )


@pytest.fixture(scope="function")
def visitor_send_text_message_english(visitor_get_initial_messages):
    (
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
    ) = visitor_get_initial_messages

    #  ======= visitor send text message =======
    message_guid = str(uuid.uuid4())

    req_body = [
        {
            "type": "batchAction",
            "actions": [
                {
                    "type": "sendChatMessages",
                    "chatGuid": chat_guid,
                    "messages": [
                        {
                            "content": "SSBoYXZlIGEgc2VyaW91cyBwcm9ibGVt",  # 消息是：I have a serious problem
                            "encoding": "base64",
                            "type": "visitorAddTextMessage",
                            "guid": message_guid,
                            "sender": {"type": "visitor"},
                            "isPassword": False,
                            "quickReplyNextActionId": "00000000-0000-0000-0000-000000000000",
                        }
                    ],
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
            "id": 88,
        }
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
        res.json()[0]["payload"][0]["type"] == "sendChatMessages"
    ), "Failed with response: " + str(res.json())
    logger.info("\n ======= visitor has sent a english text message. =======")

    # update visitor latest chat version
    visitor_chat_version = res.json()[0]["payload"][1]["payload"][-1]["guid"]
    visitor_chat_version_from_id = res.json()[0]["payload"][1]["payload"][-1]["id"]

    res_visitor_send_text_message_english = res
    # pdb.set_trace()

    yield (
        res_visitor_send_text_message_english,
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
    )


@pytest.fixture(scope="function")
def visitor_send_file(visitor_get_initial_messages):
    (
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
    ) = visitor_get_initial_messages

    #  ======= visitor send file =======
    req_body = [
        {
            "type": "batchAction",
            "actions": [
                {
                    "type": "sendFile",
                    "chatGuid": chat_guid,
                    "fileName": "star.png",
                    "fileKey": "hv4YwbKqL8RW7tLNbGL-RVhTRLguG7cDXcSgTwGxI0YhQXyJ3FIyQAlMgXzaASP9OjUOIItrJSUdv-EpMWcGGgOqPZU_yn5HrjlBVOI_5JViFbEoQODk0HjM0nbvjt5ucEGfOmAVugONthDayDtsBD0hFKG-y8RQ7SQ6w5bgMFsw",
                    "isUseStandbyFileService": False,
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
            "id": 88,
        }
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
        res.json()[0]["payload"][0]["type"] == "sendFile"
    ), "Failed with response: " + str(res.json())
    logger.info("\n ======= visitor has sent a file. =======")

    # update the latest visitor chat version
    visitor_chat_version = res.json()[0]["payload"][1]["payload"][-1]["guid"]
    visitor_chat_version_from_id = res.json()[0]["payload"][1]["payload"][-1]["id"]
    res_send_file = res

    yield (
        res_send_file,
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
    )


@pytest.fixture(scope="function")
def visitor_request_video_chat(visitor_get_initial_messages):
    (
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
    ) = visitor_get_initial_messages

    #  ======= visitor requests video chat =======
    message_guid = str(uuid.uuid4())

    req_body = [
        {
            "type": "batchAction",
            "actions": [
                {
                    "type": "sendChatMessages",
                    "chatGuid": chat_guid,
                    "messages": [
                        {
                            "content": "",
                            "encoding": "base64",
                            "type": "visitorVideoChatRequest",
                            "guid": message_guid,
                            "sender": {"type": "visitor"},
                            "isPassword": False,
                            "quickReplyNextActionId": "00000000-0000-0000-0000-000000000000",
                        }
                    ],
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
            "id": 88,
        }
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
        res.json()[0]["payload"][0]["type"] == "sendChatMessages"
    ), "Failed with response: " + str(res.json())
    logger.info("\n ======= visitor has requested video chat. =======")

    # update the latest visitor chat version
    visitor_chat_version = res.json()[0]["payload"][1]["payload"][-1]["guid"]
    visitor_chat_version_from_id = res.json()[0]["payload"][1]["payload"][-1]["id"]

    res_visitor_request_video_chat = res
    # pdb.set_trace()

    yield (
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
    )


@pytest.fixture(scope="function")
def visitor_request_audio_chat(visitor_get_initial_messages):
    (
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
    ) = visitor_get_initial_messages

    #  ======= visitor requests audio chat =======
    message_guid = str(uuid.uuid4())

    req_body = [
        {
            "type": "batchAction",
            "actions": [
                {
                    "type": "sendChatMessages",
                    "chatGuid": chat_guid,
                    "messages": [
                        {
                            "content": "",
                            "encoding": "base64",
                            "type": "visitorAudioChatRequest",
                            "guid": message_guid,
                            "sender": {"type": "visitor"},
                            "isPassword": False,
                            "quickReplyNextActionId": "00000000-0000-0000-0000-000000000000",
                        }
                    ],
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
            "id": 88,
        }
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
        res.json()[0]["payload"][0]["type"] == "sendChatMessages"
    ), "Failed with response: " + str(res.json())
    logger.info("\n ======= visitor has requested audio chat. =======")

    # update the latest visitor chat version
    visitor_chat_version = res.json()[0]["payload"][1]["payload"][-1]["guid"]
    visitor_chat_version_from_id = res.json()[0]["payload"][1]["payload"][-1]["id"]

    res_visitor_request_audio_chat = res
    # pdb.set_trace()

    yield (
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
    )


@pytest.fixture(scope="function")
def visitor_enter_offline_message(login, visitor_new_visitor):
    login_data = login
    site_id = login_data["site_id"]

    (
        res_new_visitor,
        visitor_guid,
        visitor_session_id,
        campaign_id,
        visitor_ashx_url,
    ) = visitor_new_visitor

    #  ======= visitor enter offline message =======

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
        visitor_ashx_url, None, "POST", None, None, request_body
    )

    # pdb.set_trace()
    assert res_enter_offline_message.status_code == 200, (
        "Failed with status code: "
        + str(res_enter_offline_message.status_code)
        + " and response: "
        + str(res_enter_offline_message.json())
    )
    assert (
        res_enter_offline_message.json()[0]["type"] == "enterOfflineMessage"
    ), "Failed with response: " + str(res_enter_offline_message.json())
    logger.info(
        "\n ======= Now we have a new visitor in offline message status ======="
    )

    yield (
        res_enter_offline_message,
        res_new_visitor,
        visitor_guid,
        visitor_session_id,
        campaign_id,
        visitor_ashx_url,
    )


@pytest.fixture(scope="function")
def visitor_submit_offline_message(login, visitor_new_visitor):
    login_data = login
    site_id = login_data["site_id"]

    (
        res_new_visitor,
        visitor_guid,
        visitor_session_id,
        campaign_id,
        visitor_ashx_url,
    ) = visitor_new_visitor

    #  ======= visitor enter offline message =======

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
                "subject": "Hello subject - need help with my order.",
                "content": "Hello offline message content. I need help with my order. The invoice number is 123456789.",
                "attachment": {},
            },
            "source": {"type": "button", "page": {}},
            "sessionId": visitor_session_id,
            "ssoSessionToken": "",
            "id": 64,
        }
    ]

    res_submit_offline_message = send_request(
        visitor_ashx_url, None, "POST", None, None, request_body
    )

    # pdb.set_trace()
    assert res_submit_offline_message.status_code == 200, (
        "Failed with status code: "
        + str(res_submit_offline_message.status_code)
        + " and response: "
        + str(res_submit_offline_message.json())
    )
    assert (
        res_submit_offline_message.json()[0]["type"] == "submitOfflineMessage"
    ), "Failed with response: " + str(res_submit_offline_message.json())
    logger.info(
        "\n ======= Visitor has submitted the offline message form. A new offline message has been created successfully in chatserver. ======="
    )

    yield (
        res_submit_offline_message,
        res_new_visitor,
        visitor_guid,
        visitor_session_id,
        campaign_id,
        visitor_ashx_url,
    )

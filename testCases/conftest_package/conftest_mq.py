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
def mq_purge_messages(login):
    def _mq_purge_messages(queue_name):
        login_data = login
        vhost = login_data["mq_vhost"]
        req_url = login_data["mq_purge_message_api"].replace("$queue_name$", queue_name)

        res = send_request(
            req_url,
            None,
            "DELETE",
            login_data["mq_auth"],
            login_data["common_headers"],
            {"vhost": vhost, "name": queue_name, "mode": "purge"},
        )

        # pdb.set_trace()
        assert res.status_code == 204, (
            "Failed with status code: "
            + str(res.status_code)
            + " and response: "
            + str(res.json())
        )
        logger.info(f"\n ======= mq_purge_messages succeeded for {queue_name} =======")

    return _mq_purge_messages


@pytest.fixture(scope="function")
def mq_get_messages(login, mq_purge_messages):
    def _mq_get_messages(queue_name):
        login_data = login
        vhost = login_data["mq_vhost"]
        req_url = login_data["mq_get_message_api"].replace("$queue_name$", queue_name)
        for i in range(5):
            sleep(2)
            res = send_request(
                req_url,
                None,
                "POST",
                login_data["mq_auth"],
                login_data["common_headers"],
                {
                    "vhost": vhost,
                    "name": queue_name,
                    "truncate": "50000",
                    "ackmode": "ack_requeue_true",
                    "encoding": "auto",
                    "count": "100",
                },
            )

            # pdb.set_trace()
            assert res.status_code == 200, (
                "Failed with status code: "
                + str(res.status_code)
                + " and response: "
                + str(res.json())
            )
            if len(res.json()) == 1:
                logger.info(
                    f"\n ======= In #{i} check, the fake data has enter into {queue_name} ======="
                )
                break

    return _mq_get_messages


@pytest.fixture(scope="function")
def mq_check_consumer_connected(login):
    def _mq_check_consumer_connected(queue_name):
        login_data = login
        vhost = login_data["mq_vhost"]
        req_url = login_data["mq_queue_api"].replace("$queue_name$", queue_name)

        res = send_request(
            req_url,
            None,
            "GET",
            login_data["mq_auth"],
            login_data["common_headers"],
            None,
        )
        sleep(2)
        # pdb.set_trace()
        assert res.status_code == 200
        assert res.json()["consumers"] > 0, (
            "Failed with status code: "
            + str(res.status_code)
            + " and response: "
            + str(res.json())
        )
        logger.info(
            f"\n ======= Consumer application connected for {queue_name} ======="
        )

    return _mq_check_consumer_connected


@pytest.fixture(scope="function")
def mq_check_message_consumed(login):
    def _mq_check_message_consumed(queue_name):
        login_data = login
        vhost = login_data["mq_vhost"]
        req_url = login_data["mq_queue_api"].replace("$queue_name$", queue_name)

        # loop for 2 seconds x 5 times to check if message has been consumed
        for i in range(5):
            sleep(2)

            res = send_request(
                req_url,
                None,
                "GET",
                login_data["mq_auth"],
                login_data["common_headers"],
                None,
            )
            # pdb.set_trace()
            assert res.status_code == 200, (
                "The message is not consumed. Please check. Failed with status code: "
                + str(res.status_code)
                + " and response: "
                + str(res.json())
            )
            if res.json()["messages"] == 0:
                logger.info(
                    f"\n ======= In #{i} check, all messages has been consumed for {queue_name} ======="
                )
                break

    return _mq_check_message_consumed


@pytest.fixture(scope="function")
def mq_publish_message(login, mq_purge_messages):
    def _mq_publish_message(queue_name, message_body):
        mq_purge_messages(queue_name)

        login_data = login
        vhost = login_data["mq_vhost"]

        message_guid = str(uuid.uuid4())
        site_id = login_data["site_id"]
        agent_id = login_data["agent_id"]

        # we will replace the following common parameters in the message_body
        message_body = replace_dict_value_multi(
            message_body,
            {
                "$vhost$": vhost,
                "$queue_name$": queue_name,
                "$message_guid$": message_guid,
                "$site_id$": site_id,
                "$agent_id$": agent_id,
            },
        )

        # pdb.set_trace()

        res = send_request(
            login_data["mq_publish_api"],
            None,
            "POST",
            login_data["mq_auth"],
            login_data["common_headers"],
            message_body,
        )
        sleep(2)
        # pdb.set_trace()
        assert res.status_code == 200
        assert res.json()["routed"] == True
        logger.info(
            f"\n ======= mq_publish_message succeeded for {queue_name} with message_id: {message_guid}, message_body: {message_body} ======="
        )

    return _mq_publish_message


@pytest.fixture(scope="function")
def mq_publish_ban_added(login, mq_publish_message):
    login_data = login
    ban_guid = str(uuid.uuid4())

    def _mq_publish_ban_added(queue_name, message_body):
        visitor_guid = str(uuid.uuid4())
        message_body = replace_dict_value_multi(
            message_body,
            {
                "$ban_guid$": ban_guid,
                "$visitor_guid$": visitor_guid,
            },
        )
        # pdb.set_trace()
        mq_publish_message(queue_name, message_body)

    yield _mq_publish_ban_added

    # loop for 2 seconds x 5 times to check if banned visitor has been saved to DB by ReportingConsumerService, if yes, then delete it
    request_url_delete = login_data["api_url"] + "/livechat/bannedVisitors/" + ban_guid
    for i in range(6):
        sleep(2)
        res_delete = send_request(
            request_url_delete,
            None,
            "DELETE",
            None,
            login_data["common_headers"],
            None,
        )

        # pdb.set_trace()
        if res_delete.status_code == 204:
            logger.info(
                f"\n ======= mq-created banned visitor has been deleted in the #{i} attempt ======="
            )
            break
        if i == 5:
            logger.error(
                "\n ======= ERROR: mq-created banned visitor has not been deleted after 10 seconds. You should check the DB and clean dirty data if neccessary. ======="
            )


@pytest.fixture(scope="function")
def mq_publish_chat_ended(login, mq_publish_message, save_and_delete_chat):
    login_data = login
    campaign_id = str(uuid.uuid4())
    agent_id = login_data["agent_id"]
    agent_email = login_data["user_data"]["email"]
    chat_guid = str(uuid.uuid4())

    def _mq_publish_chat_ended(queue_name, message_body):
        message_guid = str(uuid.uuid4())
        visitor_guid = str(uuid.uuid4())
        session_guid = str(uuid.uuid4())
        request_start_time = (datetime.utcnow() - timedelta(seconds=20)).strftime(
            "%Y-%m-%dT%H:%M:%S.%fZ"
        )
        end_time = (datetime.utcnow() - timedelta(seconds=10)).strftime(
            "%Y-%m-%dT%H:%M:%S.%fZ"
        )
        submit_time = (datetime.utcnow() - timedelta(seconds=5)).strftime(
            "%Y-%m-%dT%H:%M:%S.%fZ"
        )
        message_body = replace_dict_value_multi(
            message_body,
            {
                "$campaign_id$": campaign_id,
                "$request_start_time$": request_start_time,
                "$end_time$": end_time,
                "$chat_guid$": chat_guid,
                "$visitor_guid$": visitor_guid,
                "$session_guid$": session_guid,
                "$submit_time$": submit_time,
                "$agent_email$": agent_email,
            },
        )
        # pdb.set_trace()
        mq_publish_message(queue_name, message_body)

    yield _mq_publish_chat_ended

    save_and_delete_chat(chat_guid)


@pytest.fixture(scope="function")
def mq_publish_chat_missed(login, mq_publish_message, save_and_delete_chat):
    login_data = login
    campaign_id = str(uuid.uuid4())
    agent_id = login_data["agent_id"]
    agent_email = login_data["user_data"]["email"]
    chat_guid = str(uuid.uuid4())

    def _mq_publish_chat_missed(queue_name, message_body):
        message_guid = str(uuid.uuid4())
        visitor_guid = str(uuid.uuid4())
        session_guid = str(uuid.uuid4())
        request_start_time = (datetime.utcnow() - timedelta(seconds=20)).strftime(
            "%Y-%m-%dT%H:%M:%S.%fZ"
        )
        end_time = (datetime.utcnow() - timedelta(seconds=10)).strftime(
            "%Y-%m-%dT%H:%M:%S.%fZ"
        )
        submit_time = (datetime.utcnow() - timedelta(seconds=5)).strftime(
            "%Y-%m-%dT%H:%M:%S.%fZ"
        )
        message_body = replace_dict_value_multi(
            message_body,
            {
                "$campaign_id$": campaign_id,
                "$request_start_time$": request_start_time,
                "$end_time$": end_time,
                "$chat_guid$": chat_guid,
                "$visitor_guid$": visitor_guid,
                "$session_guid$": session_guid,
                "$submit_time$": submit_time,
                "$agent_email$": agent_email,
            },
        )
        # pdb.set_trace()
        mq_publish_message(queue_name, message_body)

    yield _mq_publish_chat_missed

    save_and_delete_chat(chat_guid)


@pytest.fixture(scope="function")
def mq_publish_chat_refused(login, mq_publish_message, save_and_delete_chat):
    login_data = login
    campaign_id = str(uuid.uuid4())
    agent_id = login_data["agent_id"]
    agent_email = login_data["user_data"]["email"]
    chat_guid = str(uuid.uuid4())

    def _mq_publish_chat_refused(queue_name, message_body):
        message_guid = str(uuid.uuid4())
        visitor_guid = str(uuid.uuid4())
        session_guid = str(uuid.uuid4())
        request_start_time = (datetime.utcnow() - timedelta(seconds=20)).strftime(
            "%Y-%m-%dT%H:%M:%S.%fZ"
        )
        end_time = (datetime.utcnow() - timedelta(seconds=10)).strftime(
            "%Y-%m-%dT%H:%M:%S.%fZ"
        )
        submit_time = (datetime.utcnow() - timedelta(seconds=5)).strftime(
            "%Y-%m-%dT%H:%M:%S.%fZ"
        )
        message_body = replace_dict_value_multi(
            message_body,
            {
                "$message_guid$": message_guid,
                "$campaign_id$": campaign_id,
                "$agent_id$": agent_id,
                "$request_start_time$": request_start_time,
                "$end_time$": end_time,
                "$chat_guid$": chat_guid,
                "$visitor_guid$": visitor_guid,
                "$session_guid$": session_guid,
                "$submit_time$": submit_time,
                "$agent_email$": agent_email,
            },
        )
        # pdb.set_trace()
        mq_publish_message(queue_name, message_body)

    yield _mq_publish_chat_refused

    save_and_delete_chat(chat_guid)


@pytest.fixture(scope="function")
def mq_publish_offline_message_submitted(
    login, mq_publish_message, save_and_delete_offline_message
):
    login_data = login
    campaign_id = str(uuid.uuid4())

    def _mq_publish_offline_message_submitted(queue_name, message_body):
        message_guid = str(uuid.uuid4())
        chat_guid = str(uuid.uuid4())
        visitor_guid = str(uuid.uuid4())
        session_guid = str(uuid.uuid4())
        time = (datetime.utcnow() - timedelta(seconds=20)).strftime(
            "%Y-%m-%dT%H:%M:%S.%fZ"
        )
        visit_time = (datetime.utcnow() - timedelta(seconds=60)).strftime(
            "%Y-%m-%dT%H:%M:%S.%fZ"
        )
        message_body = replace_dict_value_multi(
            message_body,
            {
                "$message_guid$": message_guid,
                "$campaign_id$": campaign_id,
                "$chat_guid$": chat_guid,
                "$time$": time,
                "$visitor_guid$": visitor_guid,
                "$session_guid$": session_guid,
                "$visit_time$": visit_time,
            },
        )
        # pdb.set_trace()
        mq_publish_message(queue_name, message_body)

    yield _mq_publish_offline_message_submitted

    save_and_delete_offline_message(campaign_id)

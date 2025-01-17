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
import base64

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
def init_location(login):
    login_data = login
    request_url_create = login_data["api_url"] + "/queue/locations"
    request_param = {"siteId": login_data["site_id"]}
    request_body = {
        "themeColor": "#329fd9",
        "greetingMessage": "Welcome!",
        "name": "temp location",
        "logo": None,
        "desks": [
            {"name": "desk1", "order": 1},
            {"name": "desk2", "order": 2},
        ],
    }

    res = send_request(
        request_url_create,
        request_param,
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
    logger.info("\n ======= location has been created =======")
    yield res

    created_id = res.json()["id"]
    request_url_delete = login_data["api_url"] + "/queue/locations/" + created_id
    r = send_request(
        request_url_delete,
        request_param,
        "DELETE",
        None,
        login_data["common_headers"],
        None,
    )
    assert r.status_code == 204
    logger.info("\n ======= newly-created location has been deleted =======")


@pytest.fixture(scope="session")
def init_queue(login, init_location):
    login_data = login
    location = init_location
    location_id = location.json()["id"]

    request_url_create = login_data["api_url"] + "/queue/queues"
    request_param = {"siteId": login_data["site_id"]}
    request_body = {"name": "temp queue", "locationId": location_id, "description": ""}

    res = send_request(
        request_url_create,
        request_param,
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
    )  # the status code should be 201. it's a bug.
    logger.info("\n ======= queue has been created =======")
    yield res

    created_id = res.json()["id"]
    request_url_delete = login_data["api_url"] + "/queue/queues/" + created_id
    res_delete = send_request(
        request_url_delete,
        request_param,
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
    logger.info("\n ======= newly-created queue has been deleted =======")


@pytest.fixture(scope="module")
def init_queue_notification(login, init_queue):
    login_data = login
    site_id = login_data["site_id"]
    queue = init_queue
    queue_id = queue.json()["id"]
    location_id = queue.json()["locationId"]

    queue_notification_templates = init_queue.json()["notificationTemplates"]
    for i in range(len(queue_notification_templates)):
        encoded_text = base64.b64encode(
            queue_notification_templates[i]["text"].encode("utf-8")
        ).decode("utf-8")
        queue_notification_templates[i][
            "text"
        ] = f"data:text/plain;base64,{encoded_text}"
        encoded_text = base64.b64encode(
            queue_notification_templates[i]["text"].encode("utf-8")
        ).decode("utf-8")
        queue_notification_templates[i][
            "text"
        ] = f"data:text/plain;base64,{encoded_text}"
        queue_notification_templates[i]["isEnabled"] = True
        del queue_notification_templates[i]["defaultText"]
        del queue_notification_templates[i]["siteId"]
        del queue_notification_templates[i]["isDeleted"]

    # ======== enable queue notification ========
    request_url_enable_queue_notification = (
        login_data["api_url"] + f"/queue/queues/{queue_id}"
    )
    request_param = {"siteId": site_id}

    request_body_enable_queue_notification = {
        "id": queue_id,
        "siteId": site_id,
        "name": "temp queue",
        "locationId": location_id,
        "notificationTemplates": queue_notification_templates,
        "greetingMessage": "Thanks for joining the queue. Please fill in the information required below to get started.",
    }

    res = send_request(
        request_url_enable_queue_notification,
        request_param,
        "PUT",
        None,
        login_data["common_headers"],
        request_body_enable_queue_notification,
    )
    # pdb.set_trace()
    assert res.status_code == 200
    logger.info("\n ======= queue notification has been enabled =======")
    yield res


@pytest.fixture(scope="function")
def init_queue_session(login, init_queue, remove_session):
    login_data = login
    site_id = login_data["site_id"]
    queue = init_queue
    queue_id = queue.json()["id"]
    location_id = queue.json()["locationId"]
    name_field_id = queue.json()["fields"][0]["id"]
    phone_field_id = queue.json()["fields"][1]["id"]
    email_field_id = queue.json()["fields"][2]["id"]
    name = fake.name()
    phone = fake.phone_number()
    email = fake.email()

    working_hours_list = queue.json()["workingHours"]
    for i in range(len(working_hours_list)):
        working_hours_list[i]["isEnabled"] = True
        working_hours_list[i]["startTime"] = "00:00:00"
        working_hours_list[i]["endTime"] = "23:59:59"
        working_hours_list[i]["availableServingAgentsCount"] = 1

    # ======== update queue working hours to make sure queue is open ========
    request_url_update_queue = login_data["api_url"] + f"/queue/queues/{queue_id}"
    request_param = {"siteId": login_data["site_id"]}

    request_body_update_queue = {
        "id": queue_id,
        "name": "temp queue",
        "locationId": location_id,
        "greetingMessage": "<p>updated</p>",
        "AboutToStartNotificationMinutes": 30,
        "workingHours": working_hours_list,
    }

    res_queue = send_request(
        request_url_update_queue,
        request_param,
        "PUT",
        None,
        login_data["common_headers"],
        request_body_update_queue,
    )
    # pdb.set_trace()
    assert res_queue.status_code == 200
    assert res_queue.json()["workingHours"][6]["isEnabled"] == True

    # ======== create queue session ========
    request_url_create = (
        login_data["api_url"] + f"/queue/joinQueue/Queues/{queue_id}/sessions"
    )
    request_body = {
        "fieldResults": [
            {"fieldId": name_field_id, "value": name},
            {"fieldId": phone_field_id, "value": phone},
            {"fieldId": email_field_id, "value": email},
        ]
    }

    res = send_request(
        request_url_create, request_param, "POST", None, None, request_body
    )

    session_id = res.json()["id"]

    assert res.status_code == 200
    assert res.json()["status"] == "created"
    logger.info("\n ======= queue session has been created =======")
    yield res

    # ======== remove queue session ========
    remove_session(queue_id, session_id)


@pytest.fixture(scope="function")
def init_2queue_sessions(login, init_queue, init_queue_session):
    login_data = login
    site_id = login_data["site_id"]
    queue = init_queue
    queue_id = queue.json()["id"]
    name_field_id = queue.json()["fields"][0]["id"]
    phone_field_id = queue.json()["fields"][1]["id"]
    email_field_id = queue.json()["fields"][2]["id"]
    name = fake.name()
    phone = fake.phone_number()
    email = fake.email()
    session1 = init_queue_session.json()

    # ======== create queue session2 ========
    request_url_create = (
        login_data["api_url"] + f"/queue/joinQueue/Queues/{queue_id}/sessions"
    )
    request_param = {"siteId": login_data["site_id"]}
    request_body_session = {
        "fieldResults": [
            {"fieldId": name_field_id, "value": name},
            {"fieldId": phone_field_id, "value": phone},
            {"fieldId": email_field_id, "value": email},
        ]
    }

    res = send_request(
        request_url_create, request_param, "POST", None, None, request_body_session
    )

    session2 = res.json()

    assert res.status_code == 200
    assert session2["status"] == "created"
    logger.info("\n ======= queue session2 has been created =======")
    yield session1, session2

    # ======== remove queue session2 ========
    created_id = session2["id"]
    request_url_delete = (
        login_data["api_url"]
        + f"/queue/realtime/queues/{queue_id}/sessions/{created_id}:remove?siteId={site_id}"
    )
    res_remove = send_request(
        request_url_delete,
        request_param,
        "POST",
        None,
        login_data["common_headers"],
        None,
    )
    assert res_remove.status_code == 200
    logger.info("\n ======= queue session2 has been removed =======")


@pytest.fixture(scope="function")
def init_queue_session_without_removed(login, init_queue):
    login_data = login
    site_id = login_data["site_id"]
    queue = init_queue
    queue_id = queue.json()["id"]
    location_id = queue.json()["locationId"]
    name_field_id = queue.json()["fields"][0]["id"]
    phone_field_id = queue.json()["fields"][1]["id"]
    email_field_id = queue.json()["fields"][2]["id"]
    name = fake.name()
    phone = fake.phone_number()
    email = fake.email()

    working_hours_list = queue.json()["workingHours"]
    for i in range(len(working_hours_list)):
        working_hours_list[i]["isEnabled"] = True
        working_hours_list[i]["startTime"] = "00:00:00"
        working_hours_list[i]["endTime"] = "23:59:59"
        working_hours_list[i]["availableServingAgentsCount"] = 1

    # ======== update queue working hours to make sure queue is open ========
    request_url_update_queue = login_data["api_url"] + f"/queue/queues/{queue_id}"
    request_param = {"siteId": login_data["site_id"]}

    request_body_update_queue = {
        "id": queue_id,
        "name": "temp queue",
        "locationId": location_id,
        "greetingMessage": "<p>updated</p>",
        "AboutToStartNotificationMinutes": 30,
        "workingHours": working_hours_list,
    }

    res_queue = send_request(
        request_url_update_queue,
        request_param,
        "PUT",
        None,
        login_data["common_headers"],
        request_body_update_queue,
    )
    # pdb.set_trace()
    assert res_queue.status_code == 200
    assert res_queue.json()["workingHours"][6]["isEnabled"] == True

    # ======== create queue session ========
    request_url_create = (
        login_data["api_url"] + f"/queue/joinQueue/Queues/{queue_id}/sessions"
    )
    request_body = {
        "fieldResults": [
            {"fieldId": name_field_id, "value": name},
            {"fieldId": phone_field_id, "value": phone},
            {"fieldId": email_field_id, "value": email},
        ]
    }

    res = send_request(
        request_url_create, request_param, "POST", None, None, request_body
    )

    # pdb.set_trace()
    assert res.status_code == 200
    assert res.json()["status"] == "created"
    logger.info("\n ======= queue session has been created =======")
    yield res


@pytest.fixture(scope="function")
def init_queue_session_summoned(login, init_queue_session_without_removed):
    login_data = login
    site_id = login_data["site_id"]
    queue_id = init_queue_session_without_removed.json()["queueId"]
    session_id = init_queue_session_without_removed.json()["id"]

    request_url_summon = (
        login_data["api_url"]
        + f"/queue/realtime/Queues/{queue_id}/sessions/{session_id}:summon"
    )
    request_param = {"siteId": site_id}

    res_summoned = send_request(
        request_url_summon,
        request_param,
        "POST",
        None,
        login_data["common_headers"],
        {},
    )

    assert res_summoned.status_code == 200, (
        "Failed with status code: "
        + str(res_summoned.status_code)
        + " and response: "
        + str(res_summoned.json())
    )

    logger.info("\n ======= queue session has been set as summoned =======")

    yield res_summoned


@pytest.fixture(scope="function")
def init_queue_session_noshow(
    login, init_queue_session_summoned, noshow_session, remove_session
):
    login_data = login
    site_id = login_data["site_id"]
    queue_id = init_queue_session_summoned.json()["queueId"]
    session_id = init_queue_session_summoned.json()["id"]

    # ======== noshow queue session ========
    res_noshow = noshow_session(queue_id, session_id)
    yield res_noshow

    # ======== remove queue session ========
    remove_session(queue_id, session_id)


@pytest.fixture(scope="function")
def init_queue_session_noshow_without_removed(
    login, init_queue_session_summoned, noshow_session
):
    login_data = login
    site_id = login_data["site_id"]
    queue_id = init_queue_session_summoned.json()["queueId"]
    session_id = init_queue_session_summoned.json()["id"]

    # ======== noshow queue session ========
    res_noshow = noshow_session(queue_id, session_id)
    yield res_noshow


@pytest.fixture(scope="function")
def init_queue_session_arrived(login, init_queue_session_summoned):
    login_data = login
    site_id = login_data["site_id"]
    queue_id = init_queue_session_summoned.json()["queueId"]
    session_id = init_queue_session_summoned.json()["id"]

    # ======== arrive queue session ========
    request_url_arrive = (
        login_data["api_url"]
        + f"/queue/realtime/Queues/{queue_id}/sessions/{session_id}:arrive"
    )
    request_param = {"siteId": site_id}

    res_arrive = send_request(
        request_url_arrive,
        request_param,
        "POST",
        None,
        login_data["common_headers"],
        {},
    )

    assert res_arrive.status_code == 200
    assert res_arrive.json()["status"] == "arrived"
    logger.info("\n ======= queue session has been arrived =======")
    yield res_arrive


@pytest.fixture(scope="function")
def init_queue_session_ended(login, init_queue_session_arrived, end_session):
    login_data = login
    site_id = login_data["site_id"]
    queue_id = init_queue_session_arrived.json()["queueId"]
    session_id = init_queue_session_arrived.json()["id"]

    # ======== end queue session ========
    res_ended = end_session(queue_id, session_id)
    yield res_ended


@pytest.fixture(scope="function")
def remove_session(login):
    def _remove_session(queue_id, session_id):
        login_data = login
        site_id = login_data["site_id"]

        request_url_remove = (
            login_data["api_url"]
            + f"/queue/realtime/Queues/{queue_id}/sessions/{session_id}:remove"
        )
        request_param = {"siteId": site_id}

        res_remove = send_request(
            request_url_remove,
            request_param,
            "POST",
            None,
            login_data["common_headers"],
            {},
        )

        assert res_remove.status_code == 200, (
            "Failed with status code: "
            + str(res_remove.status_code)
            + " and response: "
            + str(res_remove.json())
        )
        logger.info("\n ======= queue session has been set as removed =======")
        return res_remove

    yield _remove_session


@pytest.fixture(scope="function")
def end_session(login):
    def _end_session(queue_id, session_id):
        login_data = login
        site_id = login_data["site_id"]

        request_url_end = (
            login_data["api_url"]
            + f"/queue/realtime/Queues/{queue_id}/sessions/{session_id}:end"
        )
        request_param = {"siteId": site_id}

        res_end = send_request(
            request_url_end,
            request_param,
            "POST",
            None,
            login_data["common_headers"],
            {},
        )

        # pdb.set_trace()
        assert res_end.status_code == 200, (
            "Failed with status code: "
            + str(res_end.status_code)
            + " and response: "
            + str(res_end.json())
        )
        logger.info("\n ======= queue session has been set as ended =======")
        return res_end

    yield _end_session


@pytest.fixture(scope="function")
def noshow_session(login):
    def _noshow_session(queue_id, session_id):
        login_data = login
        site_id = login_data["site_id"]

        request_url_end = (
            login_data["api_url"]
            + f"/queue/realtime/Queues/{queue_id}/sessions/{session_id}:noshow"
        )
        request_param = {"siteId": site_id}

        res_noshow = send_request(
            request_url_end,
            request_param,
            "POST",
            None,
            login_data["common_headers"],
            {},
        )

        # pdb.set_trace()
        assert res_noshow.status_code == 200, (
            "Failed with status code: "
            + str(res_noshow.status_code)
            + " and response: "
            + str(res_noshow.json())
        )
        logger.info("\n ======= queue session has been set as noshow =======")
        return res_noshow

    yield _noshow_session

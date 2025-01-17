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
    generate_small_ip,
    generate_big_ip,
    replace_request_body_data_with_test_data,
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
def create_banned_ip(login, clean_up_banned_ip):
    login_data = login

    from_ip = generate_small_ip()
    to_ip = generate_big_ip()

    request_url_create = login_data["api_url"] + "/livechat/bannedIps"
    request_body = {
        "ipRangeFrom": from_ip,
        "ipRangeTo": to_ip,
        "comment": "added by pytest",
    }

    res = send_request(
        request_url_create,
        None,
        "POST",
        None,
        login_data["common_headers"],
        request_body,
    )
    assert res.status_code == 201, (
        "Failed with status code: "
        + str(res.status_code)
        + " and response: "
        + str(res.json())
    )
    logger.info("\n ======= banned ip has been created =======")
    yield res

    created_id = res.json()["id"]
    request_url_delete = login_data["api_url"] + "/livechat/bannedIps/" + created_id
    res_delete = send_request(
        request_url_delete, None, "DELETE", None, login_data["common_headers"], None
    )
    assert res_delete.status_code == 204, (
        "Failed with status code: "
        + str(res_delete.status_code)
        + " and response: "
        + str(res_delete.json())
    )
    logger.info("\n ======= newly-created banned ip has been deleted =======")


@pytest.fixture(scope="session")
def clean_up_banned_ip(login):
    login_data = login
    request_url_get = login_data["api_url"] + "/livechat/bannedIps"
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

    if len(res_get.json()["bannedIps"]) > 0:
        ips_to_clean = []
        for item in res_get.json()["bannedIps"]:
            ips_to_clean.append(item["id"])

        request_url_delete = login_data["api_url"] + "/livechat/bannedIps"
        res_delete = send_request(
            request_url_delete,
            None,
            "DELETE",
            None,
            login_data["common_headers"],
            ips_to_clean,
        )
        # pdb.set_trace()
        assert res_delete.status_code == 204, (
            "Failed with status code: "
            + str(res_delete.status_code)
            + " and response: "
            + str(res_delete.json())
        )
        logger.info("\n ======= existing banned ips have been cleaned up =======")


@pytest.fixture(scope="function")
def create_banned_visitor(login):
    login_data = login

    request_url_create = login_data["api_url"] + "/livechat/bannedVisitors"
    request_body = {
        "visitorId": str(uuid.uuid4()),
        "agentId": login_data["agent_id"],
        "comment": "added by pytest",
    }

    res = send_request(
        request_url_create,
        None,
        "POST",
        None,
        login_data["common_headers"],
        request_body,
    )
    assert res.status_code == 201, (
        "Failed with status code: "
        + str(res.status_code)
        + " and response: "
        + str(res.json())
    )
    logger.info("\n ======= banned visitor has been created =======")
    yield res

    created_id = res.json()["id"]
    request_url_delete = (
        login_data["api_url"] + "/livechat/bannedVisitors/" + created_id
    )
    res_delete = send_request(
        request_url_delete, None, "DELETE", None, login_data["common_headers"], None
    )
    assert res_delete.status_code == 204, (
        "Failed with status code: "
        + str(res_delete.status_code)
        + " and response: "
        + str(res_delete.json())
    )
    logger.info("\n ======= newly-created banned visitor has been deleted =======")


@pytest.fixture(scope="function")
def create_banned_visitor_without_delete(login):
    login_data = login

    request_url_create = login_data["api_url"] + "/livechat/bannedVisitors"
    request_body = {
        "visitorId": str(uuid.uuid4()),
        "agentId": login_data["agent_id"],
        "comment": "added by pytest",
    }

    res = send_request(
        request_url_create,
        None,
        "POST",
        None,
        login_data["common_headers"],
        request_body,
    )
    assert res.status_code == 201, (
        "Failed with status code: "
        + str(res.status_code)
        + " and response: "
        + str(res.json())
    )
    logger.info("\n ======= banned visitor has been created =======")
    yield res


@pytest.fixture(scope="function")
def delete_banned_visitor(login):
    def _delete_banned_visitor():
        login_data = login
        request_url_get = login_data["api_url"] + "/livechat/bannedVisitors"
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

        if len(res_get.json()["bannedVisitors"]) > 0:
            visitors_to_clean = []
            for item in res_get.json()["bannedVisitors"]:
                visitors_to_clean.append(item["id"])

            request_url_delete = login_data["api_url"] + "/livechat/bannedVisitors"
            res_delete = send_request(
                request_url_delete,
                None,
                "DELETE",
                None,
                login_data["common_headers"],
                visitors_to_clean,
            )
            # pdb.set_trace()
            assert res_delete.status_code == 204, (
                "Failed with status code: "
                + str(res_delete.status_code)
                + " and response: "
                + str(res_delete.json())
            )
            logger.info("\n ======= all banned visitors have been deleted =======")

    yield _delete_banned_visitor


@pytest.fixture(scope="function")
def check_banned_visitor_save_then_remove(login):
    login_data = login

    def _check_banned_visitor_save_then_remove(visitor_guid):
        for i in range(15):
            sleep(2)
            res_get_banned_visitor = send_request(
                login_data["api_url"] + "/LiveChat/bannedVisitors",
                None,
                "GET",
                None,
                login_data["common_headers"],
                None,
            )
            assert res_get_banned_visitor.status_code == 200, (
                "Failed with status code: "
                + str(res_get_banned_visitor.status_code)
                + " and response: "
                + str(res_get_banned_visitor.json())
            )
            if (len(res_get_banned_visitor.json()["bannedVisitors"]) == 1) and (
                res_get_banned_visitor.json()["bannedVisitors"][0]["visitorId"]
                == visitor_guid
            ):
                banned_visitor_record_id = res_get_banned_visitor.json()[
                    "bannedVisitors"
                ][0]["id"]
                request_url_delete = (
                    login_data["api_url"]
                    + "/livechat/bannedVisitors/"
                    + banned_visitor_record_id
                )
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
                logger.info(
                    "\n ======= banned visitor have been saved to db and then remove successfully ======="
                )
                break
        else:
            raise AssertionError(
                "Visitor with GUID {} was not found in banned visitors after 15 attempts.".format(
                    visitor_guid
                )
            )

    yield _check_banned_visitor_save_then_remove


@pytest.fixture(scope="function")
def check_banned_ip_save_then_remove(login):
    login_data = login
    yield
    for i in range(15):
        sleep(2)
        res_get_banned_ip = send_request(
            login_data["api_url"] + "/LiveChat/bannedIps",
            None,
            "GET",
            None,
            login_data["common_headers"],
            None,
        )
        assert res_get_banned_ip.status_code == 200, (
            "Failed with status code: "
            + str(res_get_banned_ip.status_code)
            + " and response: "
            + str(res_get_banned_ip.json())
        )
        if len(res_get_banned_ip.json()["bannedIps"]) == 1:
            banned_ip_record_id = res_get_banned_ip.json()["bannedIps"][0]["id"]
            request_url_delete = (
                login_data["api_url"] + "/livechat/bannedIps/" + banned_ip_record_id
            )
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
            logger.info(
                "\n ======= banned ip have been saved to db and then remove successfully ======="
            )
            break


@pytest.fixture(scope="function")
def delete_banned_visitor_after(delete_banned_visitor):
    yield
    delete_banned_visitor()


@pytest.fixture(scope="function")
def init_campaign(login, clean_up_init_campaign):
    login_data = login
    request_url_create = login_data["api_url"] + "/livechat/campaigns"
    request_body = {
        "name": "Temporary Campaign",
        "description": "This is a campaign for testing",
        "language": "english",
    }

    res = send_request(
        request_url_create,
        None,
        "POST",
        None,
        login_data["common_headers"],
        request_body,
    )
    assert res.status_code == 201, (
        "Failed with status code: "
        + str(res.status_code)
        + " and response: "
        + str(res.json())
    )
    logger.info("\n ======= campaign has been created =======")
    yield res

    created_id = res.json()["id"]
    request_url_delete = login_data["api_url"] + "/livechat/campaigns/" + created_id
    res_delete = send_request(
        request_url_delete, None, "DELETE", None, login_data["common_headers"], None
    )
    assert res_delete.status_code == 204, (
        "Failed with status code: "
        + str(res_delete.status_code)
        + " and response: "
        + str(res_delete.json())
    )
    logger.info("\n ======= newly-created campaign has been deleted =======")


# create a fixture that will search and delete all campaigns with name "Temporary Campaign"
@pytest.fixture(scope="session")
def clean_up_init_campaign(login):
    login_data = login
    request_url_get = login_data["api_url"] + "/livechat/campaigns?keywords=Temporary"
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

    if len(res_get.json()) > 0:
        campaign_id = res_get.json()[0]["id"]
        request_url_delete = (
            login_data["api_url"] + "/livechat/campaigns/" + campaign_id
        )
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
        logger.info("\n ======= existing init campaign has been cleaned up =======")


@pytest.fixture(scope="function")
def update_campaign_offline_message_send_to_specific_email_address(
    login, init_campaign
):
    login_data = login
    campaign_id = init_campaign.json()["id"]

    request_url = (
        login_data["api_url"]
        + f"/livechat/campaigns/{campaign_id}/offlineMessageConfig"
    )
    request_body = {
        "type": "systemOfflineMessageWindow",
        "emailOfflineMessageTo": "customEmailAddress",
        "customEmailAddresses": "offlinearchive@mail.com",
    }
    res = send_request(
        request_url,
        None,
        "PUT",
        None,
        login_data["common_headers"],
        request_body,
    )
    # pdb.set_trace()
    assert res.status_code == 200, "Failed with response: " + str(res.json())
    logger.info(
        "\n ======= update_campaign_offline_message_send_to_specific_email_address succeeded ======="
    )

    yield res


@pytest.fixture(scope="function")
def update_campaign_offline_message_trigger_task_bot(
    login, init_campaign, init_task_bot
):
    login_data = login
    campaign_id = init_campaign.json()["id"]
    task_bot_id = init_task_bot.json()["taskbotId"]

    request_url = (
        login_data["api_url"]
        + f"/livechat/campaigns/{campaign_id}/offlineMessageConfig"
    )
    request_body = {
        "type": "triggerTaskbot",
        "taskbotId": task_bot_id,
        "isInputAreaEnabledWhenUsedInOfflineMessage": True,
    }
    res = send_request(
        request_url,
        None,
        "PUT",
        None,
        login_data["common_headers"],
        request_body,
    )
    # pdb.set_trace()
    assert res.status_code == 200, "Failed with response: " + str(res.json())
    logger.info(
        "\n ======= update_campaign_offline_message_trigger_task_bot succeeded ======="
    )

    yield res


# create a fixture to add all types of custom fields to a wrapup form in a campaign
@pytest.fixture(scope="function")
def update_campaign_wrapup_add_all_fields(
    login,
    init_campaign,
    init_custom_field_text,
    init_custom_field_textarea,
    init_custom_field_radiobox,
    init_custom_field_checkbox,
    init_custom_field_dropdownlist,
    init_custom_field_checkboxlist,
):

    login_data = login
    campaign_id = init_campaign.json()["id"]

    custom_fields_list = [
        {
            "id": init_custom_field_text.json()["id"],
            "name": init_custom_field_text.json()["name"],
        },
        {
            "id": init_custom_field_textarea.json()["id"],
            "name": init_custom_field_textarea.json()["name"],
        },
        {
            "id": init_custom_field_radiobox.json()["id"],
            "name": init_custom_field_radiobox.json()["name"],
        },
        {
            "id": init_custom_field_checkbox.json()["id"],
            "name": init_custom_field_checkbox.json()["name"],
        },
        {
            "id": init_custom_field_dropdownlist.json()["id"],
            "name": init_custom_field_dropdownlist.json()["name"],
        },
        {
            "id": init_custom_field_checkboxlist.json()["id"],
            "name": init_custom_field_checkboxlist.json()["name"],
        },
    ]

    request_url = login_data["api_url"] + f"/livechat/wrapupFormFields"

    # iterate the list to add each custom field to wrapup form
    for custom_field in custom_fields_list:
        request_body = {
            "fieldId": custom_field["id"],
            "label": custom_field["name"],
            "isVisible": True,
            "isRequired": False,
            "campaignId": campaign_id,
            "flag": 0,
        }
        res = send_request(
            request_url,
            None,
            "POST",
            None,
            login_data["common_headers"],
            request_body,
        )
        # pdb.set_trace()
        assert res.status_code == 201, "Failed with response: " + str(res.json())

    logger.info("\n ======= update_campaign_wrapup_add_all_fields succeeded =======")
    yield campaign_id, custom_fields_list


@pytest.fixture(scope="function")
def update_campaign_wrapup_set_fields_invisible(login, init_campaign):
    login_data = login
    campaign_id = init_campaign.json()["id"]

    # first, get wrapup fields
    req_url_get = (
        login_data["api_url"]
        + f"/livechat/wrapupFormFields?campaignId={campaign_id}&sortBy=order&sortOrder=asc"
    )

    res_get = send_request(
        req_url_get,
        None,
        "GET",
        None,
        login_data["common_headers"],
        None,
    )
    # pdb.set_trace()
    assert res_get.status_code == 200, "Failed with response: " + str(res_get.json())

    # iterate the returned wrapup fields list to update each field's visible to false
    for wrapup_field in res_get.json():
        id = wrapup_field["id"]
        req_url_update = login_data["api_url"] + f"/livechat/wrapupFormFields/{id}"
        res_update = send_request(
            req_url_update,
            None,
            "PUT",
            None,
            login_data["common_headers"],
            {"isVisible": False},
        )
        # pdb.set_trace()
        assert res_update.status_code == 200, "Failed with response: " + str(
            res_update.json()
        )

    logger.info(
        "\n ======= update_campaign_set_wrapup_fields_invisible succeeded ======="
    )


@pytest.fixture(scope="function")
def update_campaign_set_email_transcripts_for_archiving(login, init_campaign):
    """update chat window configuration to enable email transcripts for archiving"""
    login_data = login
    campaign_id = init_campaign.json()["id"]

    # get chat window configurations first
    request_url = (
        login_data["api_url"] + f"/livechat/campaigns/{campaign_id}/chatWindow"
    )
    res_get = send_request(
        request_url,
        None,
        "GET",
        None,
        login_data["common_headers"],
        None,
    )
    # pdb.set_trace()
    assert res_get.status_code == 200, "Failed with response: " + str(res_get.json())
    req_update_body = res_get.json()
    req_update_body["isTranscriptSentForArchiving"] = True
    req_update_body["receivingEmailAddressesForArchivingTranscripts"] = [
        "comm100henry@163.com"
    ]
    # pdb.set_trace()

    # then update chat window configuration
    res_update_chat_window = send_request(
        request_url,
        None,
        "PUT",
        None,
        login_data["common_headers"],
        req_update_body,
    )
    # pdb.set_trace()

    assert res_update_chat_window.status_code == 200, "Failed with response: " + str(
        res_update_chat_window.json()
    )
    logger.info(
        "\n ======= update chat window configuration to enable email transcripts for archiving succeeded ======="
    )


@pytest.fixture(scope="function")
def update_campaign_enable_pre_chat(login, init_campaign):
    login_data = login
    campaign_id = init_campaign.json()["id"]

    # enable pre-chat
    request_url_enable_pre_chat = (
        login_data["api_url"] + f"/livechat/campaigns/{campaign_id}/preChat:enable"
    )

    res_enable_pre_chat = send_request(
        request_url_enable_pre_chat,
        None,
        "POST",
        None,
        login_data["common_headers"],
        None,
    )
    assert res_enable_pre_chat.status_code == 200, (
        "Failed with status code: "
        + str(res_enable_pre_chat.status_code)
        + " and response: "
        + str(res_enable_pre_chat.json())
    )
    logger.info("\n ======= update_campaign_enable_pre_chat succeeded =======")


@pytest.fixture(scope="function")
def update_campaign_pre_chat_enable_all_fields(
    login,
    init_campaign,
    update_campaign_enable_pre_chat,
    init_field_product_service,
    init_custom_field_text,
    init_custom_field_textarea,
    init_custom_field_radiobox,
    init_custom_field_checkbox,
    init_custom_field_dropdownlist,
    init_custom_field_checkboxlist,
):
    login_data = login
    campaign_id = init_campaign.json()["id"]

    # get pre-chat fields first
    req_url = login_data["api_url"] + f"/livechat/campaigns/{campaign_id}/preChat"

    res_get = send_request(
        req_url,
        None,
        "GET",
        None,
        login_data["common_headers"],
        None,
    )
    assert res_get.status_code == 200, (
        "Failed with status code: "
        + str(res_get.status_code)
        + " and response: "
        + str(res_get.json())
    )
    # pdb.set_trace()

    pre_chat_form_fields = res_get.json()["preChatFormFields"]
    # iterate the returned pre-chat fields list, set every field's visible to true
    for field in pre_chat_form_fields:
        field["isVisible"] = True

    # pdb.set_trace()
    # add all custom fields to pre-chat fields
    pre_chat_form_fields.extend(
        [
            {
                "fieldId": init_custom_field_text.json()["id"],
                "label": init_custom_field_text.json()["name"],
                "isVisible": True,
                "isRequired": False,
                "fieldOptions": [],
                "type": "text",
                "leftText": "Highly unlikely",
                "rightText": "Highly likely",
                "order": 8,
            },
            {
                "fieldId": init_custom_field_textarea.json()["id"],
                "label": init_custom_field_textarea.json()["name"],
                "isVisible": True,
                "isRequired": False,
                "fieldOptions": [],
                "type": "textArea",
                "leftText": "Highly unlikely",
                "rightText": "Highly likely",
                "order": 9,
            },
            {
                "fieldId": init_custom_field_radiobox.json()["id"],
                "label": init_custom_field_radiobox.json()["name"],
                "isVisible": True,
                "isRequired": False,
                "fieldOptions": [],
                "type": "radioBox",
                "leftText": "Highly unlikely",
                "rightText": "Highly likely",
                "order": 10,
            },
            {
                "fieldId": init_custom_field_checkbox.json()["id"],
                "label": init_custom_field_checkbox.json()["name"],
                "isVisible": True,
                "isRequired": False,
                "fieldOptions": [],
                "type": "checkBox",
                "leftText": "Highly unlikely",
                "rightText": "Highly likely",
                "order": 11,
            },
            {
                "fieldId": init_custom_field_dropdownlist.json()["id"],
                "label": init_custom_field_dropdownlist.json()["name"],
                "isVisible": True,
                "isRequired": False,
                "fieldOptions": [],
                "type": "dropdownList",
                "leftText": "Highly unlikely",
                "rightText": "Highly likely",
                "order": 12,
            },
            {
                "fieldId": init_custom_field_checkboxlist.json()["id"],
                "label": init_custom_field_checkboxlist.json()["name"],
                "isVisible": True,
                "isRequired": False,
                "fieldOptions": [],
                "type": "checkboxList",
                "leftText": "Highly unlikely",
                "rightText": "Highly likely",
                "order": 13,
            },
        ]
    )

    # pdb.set_trace()
    # update pre-chat fields, add custom fields
    req_body_update = {"preChatFormFields": pre_chat_form_fields}
    res = send_request(
        req_url,
        None,
        "PUT",
        None,
        login_data["common_headers"],
        req_body_update,
    )
    # pdb.set_trace()

    assert res.status_code == 200, (
        "Failed with status code: "
        + str(res.status_code)
        + " and response: "
        + str(res.json())
    )
    logger.info(
        "\n ======= update_campaign_pre_chat_enable_all_fields succeeded ======="
    )

    yield res


@pytest.fixture(scope="function")
def update_campaign_pre_chat_trigger_task_bot(
    login, init_campaign, update_campaign_enable_pre_chat, init_task_bot
):
    login_data = login
    campaign_id = init_campaign.json()["id"]
    task_bot_id = init_task_bot.json()["taskbotId"]

    req_url = login_data["api_url"] + f"/livechat/campaigns/{campaign_id}/preChat"

    req_body = {
        "type": "taskbot",
        "taskbotId": task_bot_id,
        "isInputAreaEnabledWhenUsedInPreChat": True,
    }
    res = send_request(
        req_url,
        None,
        "PUT",
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
    logger.info(
        "\n ======= update_campaign_pre_chat_trigger_task_bot succeeded ======="
    )

    yield res


@pytest.fixture(scope="function")
def update_campaign_enable_post_chat(login, init_campaign):
    login_data = login
    campaign_id = init_campaign.json()["id"]

    # enable post chat
    request_url_enable_post_chat = (
        login_data["api_url"] + f"/livechat/campaigns/{campaign_id}/postChat:enable"
    )

    res_enable_post_chat = send_request(
        request_url_enable_post_chat,
        None,
        "POST",
        None,
        login_data["common_headers"],
        None,
    )
    assert res_enable_post_chat.status_code == 200, (
        "Failed with status code: "
        + str(res_enable_post_chat.status_code)
        + " and response: "
        + str(res_enable_post_chat.json())
    )
    logger.info("\n ======= update_campaign_enable_post_chat succeeded =======")


@pytest.fixture(scope="function")
def update_campaign_enable_chatbot(login, init_campaign, create_keyword_chatbot):
    login_data = login
    campaign_id = init_campaign.json()["id"]
    chatbot_id = create_keyword_chatbot.json()["id"]

    # enable chatbot integration
    req_url = (
        login_data["api_url"]
        + f"/livechat/campaigns/{campaign_id}/integrationChatBotConfig"
    )
    req_body = {
        "isEnabled": True,
        "selectedChatBotId": chatbot_id,
        "isChatbotAllocatedWhenAgentOnline": True,
        "isDistributeChatsWhenQueueLengthReachesEnabled": False,
        "queueLength": 1,
        "percentageToChatbot": 100,
        "distributeChatsToChatbotOption": "byPercentage",  # go to chatbot 100% even when agent is online
        "isChatbotAllocatedWhenAgentOffline": True,
    }

    res = send_request(
        req_url,
        None,
        "PUT",
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
    logger.info("\n ======= update_campaign_enable_chatbot succeeded =======")


# create a fixture to get the built-in auto invitation list
@pytest.fixture(scope="function")
def get_campaign_builtin_auto_invitations(login, init_campaign):
    login_data = login
    campaign_id = init_campaign.json()["id"]

    req_url = (
        login_data["api_url"]
        + f"/livechat/autoInvitations?campaignId={campaign_id}&sortBy=order&sortOrder=asc"
    )

    res = send_request(
        req_url,
        None,
        "GET",
        None,
        login_data["common_headers"],
        None,
    )
    assert res.status_code == 200, (
        "Failed with status code: "
        + str(res.status_code)
        + " and response: "
        + str(res.json())
    )
    logger.info("\n ======= get_campaign_builtin_auto_invitations succeeded =======")

    yield res


@pytest.fixture(scope="function")
def update_campaign_add_auto_invitation(login, init_campaign):
    login_data = login
    campaign_id = init_campaign.json()["id"]

    # add one auto invitation to the campaign that will trigger every time
    req_url = login_data["api_url"] + f"/livechat/autoInvitations"
    req_body = {
        "name": "temp auto invitation",
        "isEnabled": True,
        "style": "bubble",
        "bubbleInvitationHeader": "agentAvatar",
        "text": "Hello, how may I help you? - by pytest",
        "textBackgroundColor": "#0033E2",
        "isTypingAreaDisplayed": True,
        "position": "centered",
        "conditionMetType": "all",
        "logicalExpression": "",
        "autoInvitationConditions": [
            {
                "fieldName": "{!Visitor.Number of chats}",
                "operator": "isLessThan",
                "value": "100",
                "order": 1,
                "description": "Number of chats is less than 100",
            }
        ],
        "isDisplayedOnceInOneSession": False,
        "isInvitationHiddenInMobile": False,
        "campaignId": campaign_id,
    }

    res = send_request(
        req_url,
        None,
        "POST",
        None,
        login_data["common_headers"],
        req_body,
    )
    assert res.status_code == 201, (
        "Failed with status code: "
        + str(res.status_code)
        + " and response: "
        + str(res.json())
    )
    logger.info("\n ======= update_campaign_add_auto_invitation succeeded =======")

    # wait for 5 seconds to make sure the auto invitation is reflected in chat server cache.
    sleep(5)

    yield res

    res_delete = send_request(
        req_url + "/" + res.json()["id"],
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
    logger.info("\n ======= newly created auto invitation is deleted =======")


@pytest.fixture(scope="function")
def update_campaign_post_chat_enable_all_fields(
    login,
    init_campaign,
    update_campaign_enable_post_chat,
    init_custom_field_text,
    init_custom_field_textarea,
    init_custom_field_radiobox,
    init_custom_field_checkbox,
    init_custom_field_dropdownlist,
    init_custom_field_checkboxlist,
):
    login_data = login
    campaign_id = init_campaign.json()["id"]

    # get post-chat fields first
    req_url = login_data["api_url"] + f"/livechat/campaigns/{campaign_id}/postChat"

    res_get = send_request(
        req_url,
        None,
        "GET",
        None,
        login_data["common_headers"],
        None,
    )
    assert res_get.status_code == 200, (
        "Failed with status code: "
        + str(res_get.status_code)
        + " and response: "
        + str(res_get.json())
    )
    # pdb.set_trace()

    post_chat_form_fields = res_get.json()["postChatFormFields"]
    # # The default Rating & Comment fields are visible by default. So we don't need to iterate the returned post-chat fields list, set every field's visible to true
    # add all custom fields to post-chat fields
    post_chat_form_fields.extend(
        [
            {
                "fieldId": init_custom_field_text.json()["id"],
                "label": init_custom_field_text.json()["name"],
                "isVisible": True,
                "isRequired": False,
                "fieldOptions": [],
                "type": "text",
                "leftText": "Highly unlikely",
                "rightText": "Highly likely",
                "order": 3,
            },
            {
                "fieldId": init_custom_field_textarea.json()["id"],
                "label": init_custom_field_textarea.json()["name"],
                "isVisible": True,
                "isRequired": False,
                "fieldOptions": [],
                "type": "textArea",
                "leftText": "Highly unlikely",
                "rightText": "Highly likely",
                "order": 4,
            },
            {
                "fieldId": init_custom_field_radiobox.json()["id"],
                "label": init_custom_field_radiobox.json()["name"],
                "isVisible": True,
                "isRequired": False,
                "fieldOptions": [],
                "type": "radioBox",
                "leftText": "Highly unlikely",
                "rightText": "Highly likely",
                "order": 5,
            },
            {
                "fieldId": init_custom_field_checkbox.json()["id"],
                "label": init_custom_field_checkbox.json()["name"],
                "isVisible": True,
                "isRequired": False,
                "fieldOptions": [],
                "type": "checkBox",
                "leftText": "Highly unlikely",
                "rightText": "Highly likely",
                "order": 6,
            },
            {
                "fieldId": init_custom_field_dropdownlist.json()["id"],
                "label": init_custom_field_dropdownlist.json()["name"],
                "isVisible": True,
                "isRequired": False,
                "fieldOptions": [],
                "type": "dropdownList",
                "leftText": "Highly unlikely",
                "rightText": "Highly likely",
                "order": 7,
            },
            {
                "fieldId": init_custom_field_checkboxlist.json()["id"],
                "label": init_custom_field_checkboxlist.json()["name"],
                "isVisible": True,
                "isRequired": False,
                "fieldOptions": [],
                "type": "checkboxList",
                "leftText": "Highly unlikely",
                "rightText": "Highly likely",
                "order": 8,
            },
        ]
    )

    # pdb.set_trace()
    # update post-chat fields, add custom fields
    req_body_update = {"postChatFormFields": post_chat_form_fields}
    res = send_request(
        req_url,
        None,
        "PUT",
        None,
        login_data["common_headers"],
        req_body_update,
    )

    # pdb.set_trace()
    assert res.status_code == 200, (
        "Failed with status code: "
        + str(res.status_code)
        + " and response: "
        + str(res.json())
    )
    logger.info(
        "\n ======= update_campaign_post_chat_enable_all_fields succeeded ======="
    )

    yield res


@pytest.fixture(scope="function")
def init_campaign_with_all_features(
    login,
    init_campaign,
    update_campaign_set_email_transcripts_for_archiving,
    update_campaign_enable_pre_chat,
    update_campaign_enable_post_chat,
):
    logger.info(
        "\n ======= campaign has been created and all features enabled. ======="
    )
    yield init_campaign


@pytest.fixture(scope="function")
def init_campaign_with_chatbot(
    login,
    init_campaign,
    update_campaign_enable_chatbot,
):
    logger.info("\n ======= campaign has been created and chatbot enabled. =======")
    yield init_campaign


@pytest.fixture(scope="function")
def init_campaign_with_task_bot(
    login,
    init_campaign,
    update_campaign_pre_chat_trigger_task_bot,
    update_campaign_offline_message_trigger_task_bot,
):
    logger.info("\n ======= campaign has been created and task bot enabled. =======")
    yield init_campaign


@pytest.fixture(scope="function")
def init_campaign_with_all_features_old(login):
    login_data = login
    request_url_create = login_data["api_url"] + "/livechat/campaigns"
    request_body = {
        "name": "Temporary Campaign with all features",
        "description": "This is a campaign for testing",
        "language": "english",
    }

    res_create = send_request(
        request_url_create,
        None,
        "POST",
        None,
        login_data["common_headers"],
        request_body,
    )
    assert res_create.status_code == 201, (
        "Failed with status code: "
        + str(res_create.status_code)
        + " and response: "
        + str(res_create.json())
    )

    # ========== enable all features ==========
    created_id = res_create.json()["id"]

    # Update Chat Window - Automatically email chat transcripts for archiving or followup
    # get chat window configurations first
    request_url = login_data["api_url"] + f"/livechat/campaigns/{created_id}/chatWindow"
    res_get = send_request(
        request_url,
        None,
        "GET",
        None,
        login_data["common_headers"],
        None,
    )
    # pdb.set_trace()
    assert res_get.status_code == 200, "Failed with response: " + str(res_get.json())
    req_update_body = res_get.json()
    req_update_body["isTranscriptSentForArchiving"] = True
    req_update_body["receivingEmailAddressesForArchivingTranscripts"] = [
        "comm100henry@163.com"
    ]
    # pdb.set_trace()

    # then update chat window configuration
    res_update_chat_window = send_request(
        request_url,
        None,
        "PUT",
        None,
        login_data["common_headers"],
        req_update_body,
    )
    # pdb.set_trace()

    assert res_update_chat_window.status_code == 200, "Failed with response: " + str(
        res_update_chat_window.json()
    )

    # enable pre-chat
    request_url_enable_pre_chat = (
        login_data["api_url"] + f"/livechat/campaigns/{created_id}/preChat:enable"
    )

    res_enable_pre_chat = send_request(
        request_url_enable_pre_chat,
        None,
        "POST",
        None,
        login_data["common_headers"],
        None,
    )
    assert res_enable_pre_chat.status_code == 200, (
        "Failed with status code: "
        + str(res_enable_pre_chat.status_code)
        + " and response: "
        + str(res_enable_pre_chat.json())
    )

    # enable post chat
    request_url_enable_post_chat = (
        login_data["api_url"] + f"/livechat/campaigns/{created_id}/postChat:enable"
    )

    res_enable_post_chat = send_request(
        request_url_enable_post_chat,
        None,
        "POST",
        None,
        login_data["common_headers"],
        None,
    )
    assert res_enable_post_chat.status_code == 200, (
        "Failed with status code: "
        + str(res_enable_post_chat.status_code)
        + " and response: "
        + str(res_enable_post_chat.json())
    )

    # return campaign
    logger.info(
        "\n ======= campaign has been created and all features enabled. ======="
    )
    yield res_create

    request_url_delete = login_data["api_url"] + "/livechat/campaigns/" + created_id
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
        "\n ======= newly-created campaign with all features has been deleted ======="
    )


@pytest.fixture(scope="session")
def init_field_product_service(login):
    login_data = login

    req_url_get = login_data["api_url"] + "/livechat/fields"

    res_get = send_request(
        req_url_get,
        None,
        "GET",
        None,
        login_data["common_headers"],
        None,
    )
    # iterate the returned fields list to find the product/service field
    for field in res_get.json():
        if field["name"] == "ProductService" and field["isSystem"] == True:
            break

    req_url = login_data["api_url"] + "/livechat/fields/" + field["id"]
    request_body = {
        "name": "ProductService",
        "type": "dropdownList",
        "fieldOptions": [
            {"value": "LiveChat"},
            {"value": "Bot"},
            {"value": "KnowledgeBase"},
            {"value": "Ticketing"},
        ],
        "leftText": "",
        "rightText": "",
        "isSystem": True,
    }

    res = send_request(
        req_url,
        None,
        "PUT",
        None,
        login_data["common_headers"],
        request_body,
    )

    # pdb.set_trace()
    assert res.status_code == 200, (
        "Failed with response code: "
        + str(res.status_code)
        + " and response: "
        + str(res.json())
    )
    logger.info("\n ======= Product/Service field has been updated. =======")
    yield res

    # restore the product/service field to default blank value is not possible because the fieldOptions is not allowed to be empty
    # since this will impact other cases, so we don't do the teardown now.


@pytest.fixture(scope="session")
def clean_up_temp_fields(login):
    login_data = login
    request_url_get = login_data["api_url"] + "/livechat/fields"
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

    if len(res_get.json()) > 0:
        for field in res_get.json():
            if "temp" in field["name"]:
                field_id = field["id"]
                request_url_delete = (
                    login_data["api_url"] + "/livechat/fields/" + field_id
                )
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
        logger.info("\n ======= existing temp fields have been cleaned up =======")


@pytest.fixture(scope="function")
def init_custom_field_text(login):
    login_data = login
    request_url_create = login_data["api_url"] + "/livechat/fields"
    request_body = {"name": "init temp text field", "type": "text", "fieldOptions": []}

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
        "Failed with response code: "
        + str(res.status_code)
        + " and response: "
        + str(res.json())
    )
    logger.info("\n ======= text custom field has been created =======")
    yield res

    created_id = res.json()["id"]
    request_url_delete = login_data["api_url"] + "/livechat/fields/" + created_id
    r = send_request(
        request_url_delete, None, "DELETE", None, login_data["common_headers"], None
    )
    assert r.status_code == 204, (
        "Failed with status code: "
        + str(r.status_code)
        + " and response: "
        + str(r.json())
    )
    logger.info("\n ======= newly-created text custom field has been deleted =======")


@pytest.fixture(scope="function")
def init_custom_field_textarea(login):
    login_data = login
    request_url_create = login_data["api_url"] + "/livechat/fields"
    request_body = {
        "name": "init temp textArea field",
        "type": "textArea",
        "fieldOptions": [],
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
        "Failed with response code: "
        + str(res.status_code)
        + " and response: "
        + str(res.json())
    )
    logger.info("\n ======= TextArea custom field has been created =======")
    yield res

    created_id = res.json()["id"]
    request_url_delete = login_data["api_url"] + "/livechat/fields/" + created_id
    r = send_request(
        request_url_delete, None, "DELETE", None, login_data["common_headers"], None
    )
    assert r.status_code == 204, (
        "Failed with status code: "
        + str(r.status_code)
        + " and response: "
        + str(r.json())
    )
    logger.info(
        "\n ======= newly-created TextArea custom field has been deleted ======="
    )


@pytest.fixture(scope="function")
def init_custom_field_radiobox(login):
    login_data = login
    request_url_create = login_data["api_url"] + "/livechat/fields"
    request_body = {
        "name": "init temp radioBox field",
        "type": "radioBox",
        "fieldOptions": [{"value": "rb1"}, {"value": "rb2"}, {"value": "rb3"}],
        "leftText": "Highly unlikely",
        "rightText": "Highly likely",
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
        "Failed with response code: "
        + str(res.status_code)
        + " and response: "
        + str(res.json())
    )
    logger.info("\n ======= radioBox custom field has been created =======")
    yield res

    created_id = res.json()["id"]
    request_url_delete = login_data["api_url"] + "/livechat/fields/" + created_id
    r = send_request(
        request_url_delete, None, "DELETE", None, login_data["common_headers"], None
    )
    assert r.status_code == 204, (
        "Failed with status code: "
        + str(r.status_code)
        + " and response: "
        + str(r.json())
    )
    logger.info(
        "\n ======= newly-created radioBox custom field has been deleted ======="
    )


@pytest.fixture(scope="function")
def init_custom_field_checkbox(login):
    login_data = login
    request_url_create = login_data["api_url"] + "/livechat/fields"
    request_body = {
        "name": "init temp checkBox field",
        "type": "checkBox",
        "fieldOptions": [],
        "leftText": "Highly unlikely",
        "rightText": "Highly likely",
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
        "Failed with response code: "
        + str(res.status_code)
        + " and response: "
        + str(res.json())
    )
    logger.info("\n ======= checkBox custom field has been created =======")
    yield res

    created_id = res.json()["id"]
    request_url_delete = login_data["api_url"] + "/livechat/fields/" + created_id
    r = send_request(
        request_url_delete, None, "DELETE", None, login_data["common_headers"], None
    )
    assert r.status_code == 204, (
        "Failed with status code: "
        + str(r.status_code)
        + " and response: "
        + str(r.json())
    )
    logger.info(
        "\n ======= newly-created checkBox custom field has been deleted ======="
    )


@pytest.fixture(scope="function")
def init_custom_field_dropdownlist(login):
    login_data = login
    request_url_create = login_data["api_url"] + "/livechat/fields"
    request_body = {
        "name": "init temp dropdownList field",
        "type": "dropdownList",
        "fieldOptions": [{"value": "ddl1"}, {"value": "ddl2"}, {"value": "ddl3"}],
        "leftText": "Highly unlikely",
        "rightText": "Highly likely",
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
        "Failed with response code: "
        + str(res.status_code)
        + " and response: "
        + str(res.json())
    )
    logger.info("\n ======= dropdownList custom field has been created =======")
    yield res

    created_id = res.json()["id"]
    request_url_delete = login_data["api_url"] + "/livechat/fields/" + created_id
    r = send_request(
        request_url_delete, None, "DELETE", None, login_data["common_headers"], None
    )
    assert r.status_code == 204, (
        "Failed with status code: "
        + str(r.status_code)
        + " and response: "
        + str(r.json())
    )
    logger.info(
        "\n ======= newly-created dropdownList custom field has been deleted ======="
    )


@pytest.fixture(scope="function")
def init_custom_field_checkboxlist(login):
    login_data = login
    request_url_create = login_data["api_url"] + "/livechat/fields"
    request_body = {
        "name": "init temp checkboxList field",
        "type": "checkboxList",
        "fieldOptions": [{"value": "cbl1"}, {"value": "cbl2"}, {"value": "cbl3"}],
        "leftText": "Highly unlikely",
        "rightText": "Highly likely",
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
        "Failed with response code: "
        + str(res.status_code)
        + " and response: "
        + str(res.json())
    )
    logger.info("\n ======= checkboxList custom field has been created =======")
    yield res

    created_id = res.json()["id"]
    request_url_delete = login_data["api_url"] + "/livechat/fields/" + created_id
    r = send_request(
        request_url_delete, None, "DELETE", None, login_data["common_headers"], None
    )
    assert r.status_code == 204, (
        "Failed with status code: "
        + str(r.status_code)
        + " and response: "
        + str(r.json())
    )
    logger.info(
        "\n ======= newly-created checkboxList custom field has been deleted ======="
    )


@pytest.fixture(scope="session")
def clean_up_temp_custom_variable(login):
    login_data = login
    request_url_get = login_data["api_url"] + "/LiveChat/customVariables"
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

    if len(res_get.json()) > 0:
        for cv in res_get.json():
            if "temp" in cv["name"]:
                cv_id = cv["id"]
                request_url_delete = (
                    login_data["api_url"] + "/LiveChat/customVariables/" + cv_id
                )
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
        logger.info(
            "\n ======= existing temp custom variables have been cleaned up ======="
        )


@pytest.fixture(scope="module")
def create_custom_variable(login, clean_up_temp_custom_variable):
    login_data = login

    request_url_create = login_data["api_url"] + "/LiveChat/customVariables"
    request_body = {
        "name": "temp cv",
        "value": "",
        "hyperlink": "",
        "type": "text",
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
    logger.info("\n ======= new custom variable has been created =======")
    yield res

    created_id = res.json()["id"]
    request_url_delete = (
        login_data["api_url"] + "/LiveChat/customVariables/" + created_id
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
    logger.info("\n ======= newly-created custom variable has been deleted =======")


@pytest.fixture(scope="module")
def enable_custom_variable_config(login):
    login_data = login
    # need enable custom variable config first
    request_url_enable = login_data["api_url"] + "/LiveChat/customVariableConfig:enable"
    res_enable = send_request(
        request_url_enable,
        None,
        "POST",
        None,
        login_data["common_headers"],
        None,
    )

    # pdb.set_trace()
    assert res_enable.status_code == 200, (
        "Failed with status code: "
        + str(res_enable.status_code)
        + " and response: "
        + str(res_enable.json())
    )
    logger.info("\n ======= custom variable config has been enabled =======")
    yield res_enable

    # teardown: disable custom variable config
    request_url_disable = (
        login_data["api_url"] + "/LiveChat/customVariableConfig:disable"
    )
    res_disable = send_request(
        request_url_disable,
        None,
        "POST",
        None,
        login_data["common_headers"],
        None,
    )

    # pdb.set_trace()
    assert res_disable.status_code == 200, (
        "Failed with status code: "
        + str(res_disable.status_code)
        + " and response: "
        + str(res_disable.json())
    )
    logger.info("\n ======= custom variable config has been disabled =======")


@pytest.fixture(scope="module")
def init_custom_variable(enable_custom_variable_config, create_custom_variable):
    res = create_custom_variable
    sleep(5)  # make sure chat server cache is updated

    logger.info(
        "\n ======= custom variable config has been enabled and new custom variable has been created ======="
    )
    yield res


@pytest.fixture(scope="session")
def clean_up_init_secure_form(login):
    login_data = login
    request_url_get = login_data["api_url"] + "/LiveChat/secureforms"
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

    if len(res_get.json()["secureForms"]) > 0:
        for form in res_get.json()["secureForms"]:
            if "temp" in form["name"]:
                form_id = form["id"]
                request_url_delete = (
                    login_data["api_url"] + "/LiveChat/secureforms/" + form_id
                )
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
        logger.info(
            "\n ======= existing temp secure forms have been cleaned up ======="
        )


@pytest.fixture(scope="function")
def create_secure_form(login, clean_up_init_secure_form):
    login_data = login
    request_url_create = login_data["api_url"] + "/LiveChat/secureforms"
    request_body = {
        "name": "temp secure form",
        "description": "",
        "secureFormFields": [
            {
                "name": "Card Number",
                "type": "cardNumber",
                "secureFormFieldOptions": [],
                "isVisible": True,
                "isRequired": True,
                "order": 1,
                "required": False,
                "visible": False,
            },
            {
                "name": "Expiration Date",
                "type": "expiration",
                "secureFormFieldOptions": [],
                "isVisible": True,
                "isRequired": True,
                "order": 2,
            },
            {
                "name": "CSC/CVV",
                "type": "csc/cvv",
                "secureFormFieldOptions": [],
                "isVisible": True,
                "isRequired": False,
                "order": 3,
            },
            {
                "name": "Name on Card",
                "type": "text",
                "secureFormFieldOptions": [],
                "isVisible": True,
                "isRequired": False,
                "order": 4,
            },
            {
                "name": "Date",
                "type": "datePicker",
                "secureFormFieldOptions": [],
                "isVisible": True,
                "isRequired": False,
                "order": 5,
            },
            {
                "name": "Radio box",
                "type": "radioBox",
                "secureFormFieldOptions": [
                    {"displayText": "radioBox-option1"},
                    {"displayText": "radioBox-option2"},
                    {"displayText": "radioBox-option3"},
                ],
                "isVisible": True,
                "isRequired": False,
                "order": 6,
            },
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
    assert res.status_code == 201, (
        "Failed with status code: "
        + str(res.status_code)
        + " and response: "
        + str(res.json())
    )
    logger.info("\n ======= secure form has been created =======")
    yield res

    created_id = res.json()["id"]
    request_url_delete = login_data["api_url"] + "/LiveChat/secureforms/" + created_id
    res_delete = send_request(
        request_url_delete, None, "DELETE", None, login_data["common_headers"], None
    )
    assert res_delete.status_code == 204, (
        "Failed with status code: "
        + str(res_delete.status_code)
        + " and response: "
        + str(res_delete.json())
    )
    logger.info("\n ======= newly-created secure form has been deleted =======")


@pytest.fixture(scope="function")
def init_secure_form(create_secure_form):
    res = create_secure_form
    sleep(5)  # make sure chat server cache is updated
    logger.info(
        "\n ======= secure form has been created and updated in chatserver cache. ======="
    )
    yield res


@pytest.fixture(scope="function")
def init_enable_screen_sharing(login):
    login_data = login
    request_url_enable = login_data["api_url"] + "/LiveChat/screenSharingConfig:enable"
    res_enable = send_request(
        request_url_enable,
        None,
        "POST",
        None,
        login_data["common_headers"],
        None,
    )
    assert res_enable.status_code == 200, (
        "Failed with status code: "
        + str(res_enable.status_code)
        + " and response: "
        + str(res_enable.json())
    )
    logger.info("\n ======= desktop screen sharing has been enabled =======")
    yield res_enable

    request_url_disable = (
        login_data["api_url"] + "/LiveChat/screenSharingConfig:disable"
    )
    res_disable = send_request(
        request_url_disable,
        None,
        "POST",
        None,
        login_data["common_headers"],
        None,
    )
    assert res_disable.status_code == 200, (
        "Failed with status code: "
        + str(res_disable.status_code)
        + " and response: "
        + str(res_disable.json())
    )
    logger.info("\n ======= desktop screen sharing has been disabled =======")


@pytest.fixture(scope="function")
def enable_audio_video_chat(login):
    login_data = login
    request_url_enable = login_data["api_url"] + "/LiveChat/audioVideoChatConfig:enable"
    res_enable = send_request(
        request_url_enable,
        None,
        "POST",
        None,
        login_data["common_headers"],
        None,
    )
    assert res_enable.status_code == 200, (
        "Failed with response code: "
        + str(res_enable.status_code)
        + " and response: "
        + str(res_enable.json())
    )
    logger.info("\n ======= Audio & Video Chat has been enabled =======")
    yield res_enable

    request_url_disable = (
        login_data["api_url"] + "/LiveChat/audioVideoChatConfig:disable"
    )
    res_disable = send_request(
        request_url_disable,
        None,
        "POST",
        None,
        login_data["common_headers"],
        None,
    )
    assert res_disable.status_code == 200, (
        "Failed with response code: "
        + str(res_disable.status_code)
        + " and response: "
        + str(res_disable.json())
    )
    logger.info("\n ======= Audio & Video Chat has been disabled =======")


@pytest.fixture(scope="function")
def disable_audio_video_chat_before_and_after(disable_audio_video_chat):
    res_disable = disable_audio_video_chat()
    yield res_disable
    disable_audio_video_chat()


@pytest.fixture(scope="function")
def disable_audio_video_chat_after(disable_audio_video_chat):
    yield None
    disable_audio_video_chat()


@pytest.fixture(scope="function")
def disable_audio_video_chat(login):
    login_data = login

    def _disable_audio_video_chat():
        request_url_disable = (
            login_data["api_url"] + "/LiveChat/audioVideoChatConfig:disable"
        )
        res_disable = send_request(
            request_url_disable,
            None,
            "POST",
            None,
            login_data["common_headers"],
            None,
        )
        assert res_disable.status_code == 200, (
            "Failed with response code: "
            + str(res_disable.status_code)
            + " and response: "
            + str(res_disable.json())
        )
        logger.info("\n ======= Audio & Video Chat has been disabled =======")

    yield _disable_audio_video_chat


@pytest.fixture(scope="function")
def enable_auto_distribution(login):
    login_data = login
    request_url_enable = (
        login_data["api_url"] + "/LiveChat/autoDistributionConfig:enable"
    )
    res_enable = send_request(
        request_url_enable,
        None,
        "POST",
        None,
        login_data["common_headers"],
        None,
    )
    assert res_enable.status_code == 200, (
        "Failed with response code: "
        + str(res_enable.status_code)
        + " and response: "
        + str(res_enable.json())
    )
    logger.info("\n ======= auto distribution has been enabled =======")
    sleep(5)  # make sure chat server cache is updated
    yield res_enable

    request_url_disable = (
        login_data["api_url"] + "/LiveChat/autoDistributionConfig:disable"
    )
    res_disable = send_request(
        request_url_disable,
        None,
        "POST",
        None,
        login_data["common_headers"],
        None,
    )
    assert res_disable.status_code == 200, (
        "Failed with response code: "
        + str(res_disable.status_code)
        + " and response: "
        + str(res_disable.json())
    )
    logger.info("\n ======= auto distribution has been disabled =======")


@pytest.fixture(scope="function")
def update_auto_distribution_with_multiple_backup_departments(
    login, enable_auto_distribution, init_4departments
):
    login_data = login
    request_url = login_data["api_url"] + "/LiveChat/autodistributionconfig"

    (
        create_department,
        create_2nd_department,
        create_3rd_department,
        create_4th_department_not_available_in_live_chat,
        department1_id,
        department2_id,
        department3_id,
        department4_id,
    ) = init_4departments

    request_body = {
        "departmentAutoDistributionConfigs": [
            {
                "departmentId": department1_id,
                "autoDistributionMethod": "roundRobin",
                "backupDepartments": [
                    {
                        "departmentId": department1_id,
                        "backupDepartmentId": department2_id,
                        "order": 1,
                    },
                    {
                        "departmentId": department1_id,
                        "backupDepartmentId": department3_id,
                        "order": 2,
                    },
                ],
            },
            {
                "departmentId": department2_id,
                "backupDepartmentId": department1_id,
                "autoDistributionMethod": "capabilityWeighted",
                "backupDepartments": [
                    {
                        "departmentId": department2_id,
                        "backupDepartmentId": department3_id,
                        "order": 1,
                    },
                ],
            },
            {
                "departmentId": department3_id,
                "backupDepartmentId": department2_id,
                "backupDepartments": [],
            },
        ],
    }

    res = send_request(
        request_url,
        None,
        "PUT",
        None,
        login_data["common_headers"],
        request_body,
    )

    assert res.status_code == 200, (
        "Failed with response code: "
        + str(res.status_code)
        + " and response: "
        + str(res.json())
    )
    logger.info(
        "\n ======= auto distribution has been updated with multiple backup departments ======="
    )
    sleep(5)  # make sure chat server cache is updated
    yield department1_id, department2_id, department3_id


@pytest.fixture(scope="function")
def enable_visitor_sso(login):
    login_data = login
    request_url_enable = login_data["api_url"] + "/livechat/visitorSsoConfig:enable"
    res_enable = send_request(
        request_url_enable,
        None,
        "POST",
        None,
        login_data["common_headers"],
        None,
    )
    assert res_enable.status_code == 200, (
        "Failed with response code: "
        + str(res_enable.status_code)
        + " and response: "
        + str(res_enable.json())
    )
    logger.info("\n ======= visitor sso has been enabled =======")
    yield res_enable

    request_url_disable = login_data["api_url"] + "/livechat/visitorSsoConfig:disable"
    res_disable = send_request(
        request_url_disable,
        None,
        "POST",
        None,
        login_data["common_headers"],
        None,
    )
    assert res_disable.status_code == 200, (
        "Failed with response code: "
        + str(res_disable.status_code)
        + " and response: "
        + str(res_disable.json())
    )
    logger.info("\n ======= visitor sso has been disabled =======")


@pytest.fixture(scope="function")
def integration_visitor_sso_with_saml(
    login, init_campaign, enable_visitor_sso, clean_visitor_sso_settings
):
    """the integrate data now is used okta app with livechat3 application, when we use to real integrate with saml, we need to refactor this fixture."""
    login_data = login
    request_url = login_data["api_url"] + "/livechat/visitorSsoConfig"
    campaign_id = init_campaign.json()["id"]
    request_body = {
        "protocolType": "samlSso",
        "signInUrl": "https://dev-87375063.okta.com/app/dev-87375063_visitorsso_1/exkhsbph8waNTT2Fp5d7/sso/saml",
        "artifactResolutionServiceUrl": "",
        "logoutUrl": "https://dev-87375063.okta.com",
        "samlCertificate": "-----BEGIN CERTIFICATE-----\nMIIDqDCCApCgAwIBAgIGAZAlaLFMMA0GCSqGSIb3DQEBBQUAMIGUMQswCQYDVQQGEwJVUzETMBEG\nA1UECAwKQ2FsaWZvcm5pYTEWMBQGA1UEBwwNU2FuIEZyYW5jaXNjbzENMAsGA1UECgwET2t0YTEU\nMBIGA1UECwwLU1NPUHJvdmlkZXIxFTATBgNVBAMMDGRldi04NzM3NTA2MzEcMBoGCSqGSIb3DQEJ\nARYNaW5mb0Bva3RhLmNvbTAeFw0yNDA2MTcwODU0MzZaFw0zNDA2MTcwODU1MzZaMIGUMQswCQYD\nVQQGEwJVUzETMBEGA1UECAwKQ2FsaWZvcm5pYTEWMBQGA1UEBwwNU2FuIEZyYW5jaXNjbzENMAsG\nA1UECgwET2t0YTEUMBIGA1UECwwLU1NPUHJvdmlkZXIxFTATBgNVBAMMDGRldi04NzM3NTA2MzEc\nMBoGCSqGSIb3DQEJARYNaW5mb0Bva3RhLmNvbTCCASIwDQYJKoZIhvcNAQEBBQADggEPADCCAQoC\nggEBAOo+m13OBhFF5782+spKK8MnZNX0bn8f4qWaJJTGuk8lWX+I2UyrcpmJTwjWQZH4RaEecDRW\nCEv6hX5n67tOE/xRNlLltpdYBxpnVgj112xuYC1/a/ma99a+ktBO6PhAGFX4CDQijfcJTVqqoZGR\nxt+UlzrlSQtg41L/SxgaAXZ9ziyk2ZIBRz3TVjgvX4fE6TPDOWJq35k/cnHZkx8D9BmkcxRE3K1A\nOiDILwnLmx39FTSf4+gKDY5Yt6rOMmb1cSgvQk665XUytp5cduguC3QhLIXZStW+qirfqFNICiwj\niOEPhGqEEKYgNzIQA9lVMkm6hxSa8sGkw/c51dOcTOUCAwEAATANBgkqhkiG9w0BAQUFAAOCAQEA\nGgtHYUb+ISmj2dQiw3u3jHgzC8OIh7E4IXfHMQ9yW/x4RwSZKUqv7LsDEUubd7bqIDeDl6WdY97q\nOpAR6ob1HiDQ4zrK80Qnw/24OAgcfrkYxaE9LVXb/h33kNNbhOqTmVXuLIGHEGnFAbkE03x6cGNT\n9sNbP9BZINBVG99FYczlqtuypeH0IhF7Sj0I/V6utuGU6G/4KTni0kjtNeHOs37Gn3qrEABOtt0J\nyU35rE3gqeYQAlM5c0/wun1qiHxkdASqgubC3ujAVmD1F3jHUHy5Vmz1q8Tcm5myrHKwMLF1Jl6v\n4mFrh6HfcimriUwAgArIvCvAwD+o5YQBXY5waA==\n-----END CERTIFICATE-----",
        "jwtLoginUrl": "",
        "jwtCertificate": "",
        "visitorSsoFieldMappings": [
            {
                "idpAttribute": "name",
                "comm100Field": "{!Visitor.Name}",
                "order": 1,
            },
            {
                "idpAttribute": "email",
                "comm100Field": "{!Visitor.Email}",
                "order": 2,
            },
        ],
        "visitorSsos": [
            {
                "campaignId": campaign_id,
                "signInOption": "signInOptional",
                "isPreChatFormSkipped": "true",
                "ifOpenLoginPageInEmbeddedChatWindow": "false",
            },
        ],
        "isEnabled": "true",
        "jwtLogoutUrl": "",
    }
    res_saml = send_request(
        request_url,
        None,
        "PUT",
        None,
        login_data["common_headers"],
        request_body,
    )
    assert res_saml.status_code == 200, (
        "Failed with response code: "
        + str(res_saml.status_code)
        + " and response: "
        + str(res_saml.json())
    )
    logger.info("\n ======= visitor sso has been set with saml =======")
    yield res_saml


@pytest.fixture(scope="function")
def clean_visitor_sso_settings(login):
    yield
    login_data = login
    request_url_clean = login_data["api_url"] + "/livechat/visitorSsoConfig"
    request_body_clean = {
        "protocolType": "samlSso",
        "artifactResolutionServiceUrl": "",
        "logoutUrl": "",
        "samlCertificate": "",
        "jwtLoginUrl": "",
        "jwtCertificate": "",
        "visitorSsoFieldMappings": [],
        "isEnabled": "true",
        "jwtLogoutUrl": "",
    }
    res_clean = send_request(
        request_url_clean,
        None,
        "PUT",
        None,
        login_data["common_headers"],
        request_body_clean,
    )
    assert res_clean.status_code == 200, (
        "Failed with response code: "
        + str(res_clean.status_code)
        + " and response: "
        + str(res_clean.json())
    )
    logger.info("\n ======= visitor sso settings has been clean =======")


@pytest.fixture(scope="function")
def integration_visitor_sso_with_jwt(
    login, init_campaign, enable_visitor_sso, clean_visitor_sso_settings
):
    """this fixture data should be refactored when need real integrate with jwt sso, need add custom js code to the integrate campaign"""
    login_data = login
    request_url = login_data["api_url"] + "/livechat/visitorSsoConfig"
    campaign_id = init_campaign.json()["id"]
    request_body = {
        "protocolType": "jwtSso",
        "signInUrl": "",
        "logoutUrl": "",
        "artifactResolutionServiceUrl": "",
        "samlCertificate": "",
        "jwtLoginUrl": "",
        "jwtLogoutUrl": "",
        "jwtCertificate": "-----BEGIN PUBLIC KEY-----\nMIGfMA0GCSqGSIb3DQEBAQUAA4GNADCBiQKBgQCVQvCqwMa9Fv+O6L3Wel7ZEv907BtEuHzweHFY7T5Y2wsMyvlnsBTyl4M2iDpOLf/c2FN8/WL5hcR6bB1ME0KBhEwNnEcx+BT9AZupuKzu4iG4UIHvET5q8noY8MDSLCymEr/2+kJSKdPJ7/ODrS7MkjeysnA5gt3ZZjyFvqYWBwIDAQAB\n-----END PUBLIC KEY-----",
        "visitorSsoFieldMappings": [
            {
                "idpAttribute": "name",
                "comm100Field": "{!Visitor.Name}",
                "order": 1,
            },
            {
                "idpAttribute": "email",
                "comm100Field": "{!Visitor.Email}",
                "order": 2,
            },
        ],
        "visitorSsos": [
            {
                "campaignId": campaign_id,
                "signInOption": "signInOptional",
                "isPreChatFormSkipped": "true",
                "ifOpenLoginPageInEmbeddedChatWindow": "false",
            },
        ],
    }
    res_jwt = send_request(
        request_url,
        None,
        "PUT",
        None,
        login_data["common_headers"],
        request_body,
    )
    assert res_jwt.status_code == 200, (
        "Failed with response code: "
        + str(res_jwt.status_code)
        + " and response: "
        + str(res_jwt.json())
    )
    logger.info("\n ======= visitor sso has been set with jwt =======")
    yield res_jwt


@pytest.fixture(scope="function")
def enable_ticket_integration(login):
    login_data = login
    request_url_enable = (
        login_data["api_url"] + "/LiveChat/integrationTicketConfig:enable"
    )
    res_enable = send_request(
        request_url_enable,
        None,
        "POST",
        None,
        login_data["common_headers"],
        None,
    )
    assert res_enable.status_code == 200, (
        "Failed with response code: "
        + str(res_enable.status_code)
        + " and response: "
        + str(res_enable.json())
    )
    logger.info("\n ======= Comm100 Ticketing Integration has been enabled. =======")
    yield res_enable

    request_url_disable = (
        login_data["api_url"] + "/LiveChat/integrationTicketConfig:disable"
    )
    res_disable = send_request(
        request_url_disable,
        None,
        "POST",
        None,
        login_data["common_headers"],
        None,
    )
    assert res_disable.status_code == 200, (
        "Failed with response code: "
        + str(res_enable.status_code)
        + " and response: "
        + str(res_enable.json())
    )
    logger.info("\n ======= Comm100 Ticketing Integration has been disabled. =======")


@pytest.fixture(scope="function")
def enable_and_update_ticketing_integration_with_auto_create_ticket_from_offline_message(
    login, enable_ticket_integration
):
    login_data = login
    request_url = login_data["api_url"] + "/LiveChat/integrationTicketConfig"
    request_select_body = {
        "isTicketManuallyCreatedForAcceptChat": True,
        "isTicketManuallyCreatedFromTranscriptPage": True,
        "isTicketAutoCreatedForOfflineMessage": True,
        "isEnabled": True,
    }
    res_select = send_request(
        request_url,
        None,
        "PUT",
        None,
        login_data["common_headers"],
        request_select_body,
    )
    assert res_select.status_code == 200, (
        "Failed with response code: "
        + str(res_select.status_code)
        + " and response: "
        + str(res_select.json())
    )
    logger.info(
        "\n ======= auto_create_ticket_from_offline_message has been selected. ======="
    )
    yield res_select

    request_url_deselect = login_data["api_url"] + "/LiveChat/integrationTicketConfig"
    request_deselect_body = {
        "isTicketManuallyCreatedForAcceptChat": True,
        "isTicketManuallyCreatedFromTranscriptPage": True,
        "isTicketAutoCreatedForOfflineMessage": False,
        "isEnabled": True,
    }
    res_deselect = send_request(
        request_url_deselect,
        None,
        "PUT",
        None,
        login_data["common_headers"],
        request_deselect_body,
    )
    assert res_deselect.status_code == 200, (
        "Failed with response code: "
        + str(res_deselect.status_code)
        + " and response: "
        + str(res_deselect.json())
    )
    logger.info(
        "\n ======= auto_create_ticket_from_offline_message has been deselected. ======="
    )


@pytest.fixture(scope="function")
def enable_gotomeeting_integration(login):
    login_data = login
    request_url_enable = (
        login_data["api_url"] + "/LiveChat/integrationGotoMeetingConfig:enable"
    )
    res_enable = send_request(
        request_url_enable,
        None,
        "POST",
        None,
        login_data["common_headers"],
        None,
    )
    assert res_enable.status_code == 200, (
        "Failed with response code: "
        + str(res_enable.status_code)
        + " and response: "
        + str(res_enable.json())
    )
    logger.info("\n ======= Gotomeeting Integration has been enabled. =======")
    yield res_enable

    request_url_disable = (
        login_data["api_url"] + "/LiveChat/integrationGotoMeetingConfig:disable"
    )
    res_disable = send_request(
        request_url_disable,
        None,
        "POST",
        None,
        login_data["common_headers"],
        None,
    )
    assert res_disable.status_code == 200, (
        "Failed with response code: "
        + str(res_enable.status_code)
        + " and response: "
        + str(res_enable.json())
    )
    logger.info("\n ======= Gotomeeting Integration has been disabled. =======")


@pytest.fixture(scope="function")
def enable_zendesk_integration(login):
    login_data = login
    request_url_enable = login_data["api_url"] + "/LiveChat/integrationZendeskConfig"
    request_body_enable = {
        "isEnabled": True,
        "siteName": "2019comm100",
        "userName": "zendesk@comm100.com",
        "password": "comm100_1234",
    }
    res_enable = send_request(
        request_url_enable,
        None,
        "PUT",
        None,
        login_data["common_headers"],
        request_body_enable,
    )
    assert res_enable.status_code == 200, (
        "Failed with response code: "
        + str(res_enable.status_code)
        + " and response: "
        + str(res_enable.json())
    )
    logger.info("\n ======= zendesk Integration has been enabled. =======")
    yield res_enable

    request_url_disable = login_data["api_url"] + "/LiveChat/integrationZendeskConfig"
    request_body_disable = {
        "isEnabled": False,
        "siteName": "2019comm100",
        "userName": "zendesk@comm100.com",
        "password": "**********",
    }
    res_disable = send_request(
        request_url_disable,
        None,
        "PUT",
        None,
        login_data["common_headers"],
        request_body_disable,
    )
    assert res_disable.status_code == 200, (
        "Failed with response code: "
        + str(res_enable.status_code)
        + " and response: "
        + str(res_enable.json())
    )
    logger.info(
        "\n ======= zendesk Integration has been disabled. need wait for 3 mins to let consumer load the cache ======="
    )
    # wait for 3 minutes to make sure the zendesk integration config is disabled in zendesk consumer cache.
    sleep(180)


@pytest.fixture(scope="function")
def enable_dynamic365_integration(login):
    login_data = login
    request_url_enable = (
        login_data["api_url"] + "/LiveChat/integrationDynamics365Config:connect"
    )
    request_body_enable = {
        "isOnPremise": "false",
        "instanceUrl": "https://comm100.crm3.dynamics.com",
        "azureADTenantID": "67648efa-5ddc-4372-b505-62b86a1f61c6",
        "azureADAppID": "29dad7b2-7d9c-46aa-b8ed-19386514175e",
        "azureADAppSecret": "uDQ8Q~c6Tr6eD.t2wWvVpbzCJimgOFppPYISqbGJ",
        "password": "",
        "authority": "",
        "isEnabled": "false",
        "isDynamics365EntityCreatedAutomaticallyWhenChatEnded": "true",
        "autoActionWhenChatEnded": "createOrUpdateContactThenAttachCase",
        "contactAutoUpdateStrategyWhenChatEnded": "doNotUpdateContact",
        "autoActionWhenOfflineMessageReceived": "createOrUpdateContactThenAttachCase",
        "contactAutoUpdateStrategyWhenOfflineMessageReceived": "doNotUpdateContact",
        "integrationDynamics365FieldMappings": [],
        "integrationDynamics365EntityIdentificationRules": [],
    }
    res_enable = send_request(
        request_url_enable,
        None,
        "POST",
        None,
        login_data["common_headers"],
        request_body_enable,
    )
    assert res_enable.status_code == 200, (
        "Failed with response code: "
        + str(res_enable.status_code)
        + " and response: "
        + str(res_enable.json())
    )
    logger.info("\n ======= dynamic365 Integration has been enabled. =======")
    yield res_enable

    request_url_disable = (
        login_data["api_url"] + "/LiveChat/integrationDynamics365Config:disconnect"
    )
    request_body_disable = {}
    res_disable = send_request(
        request_url_disable,
        None,
        "POST",
        None,
        login_data["common_headers"],
        request_body_disable,
    )
    assert res_disable.status_code == 200, (
        "Failed with response code: "
        + str(res_enable.status_code)
        + " and response: "
        + str(res_enable.json())
    )
    logger.info("\n ======= dynamic365 Integration has been disabled.  =======")


@pytest.fixture(scope="function")
def enable_dynamic365_integration_whitout_disconnect(login):
    login_data = login
    request_url_enable = (
        login_data["api_url"] + "/LiveChat/integrationDynamics365Config:connect"
    )
    request_body_enable = {
        "isOnPremise": "false",
        "instanceUrl": "https://comm100.crm3.dynamics.com",
        "azureADTenantID": "67648efa-5ddc-4372-b505-62b86a1f61c6",
        "azureADAppID": "29dad7b2-7d9c-46aa-b8ed-19386514175e",
        "azureADAppSecret": "uDQ8Q~c6Tr6eD.t2wWvVpbzCJimgOFppPYISqbGJ",
        "password": "",
        "authority": "",
        "isEnabled": "false",
        "isDynamics365EntityCreatedAutomaticallyWhenChatEnded": "false",
        "autoActionWhenChatEnded": "createOrUpdateContactThenAttachCase",
        "contactAutoUpdateStrategyWhenChatEnded": "doNotUpdateContact",
        "autoActionWhenOfflineMessageReceived": "createOrUpdateContactThenAttachCase",
        "contactAutoUpdateStrategyWhenOfflineMessageReceived": "doNotUpdateContact",
        "integrationDynamics365FieldMappings": [],
        "integrationDynamics365EntityIdentificationRules": [],
    }
    res_enable = send_request(
        request_url_enable,
        None,
        "POST",
        None,
        login_data["common_headers"],
        request_body_enable,
    )
    assert res_enable.status_code == 200, (
        "Failed with response code: "
        + str(res_enable.status_code)
        + " and response: "
        + str(res_enable.json())
    )
    logger.info("\n ======= dynamic365 Integration has been enabled. =======")
    yield res_enable


@pytest.fixture(scope="function")
def get_dynamic365_integration_config(login, enable_dynamic365_integration):

    req_url = login["api_url"] + "/LiveChat/integrationDynamics365Config"

    res = send_request(
        req_url,
        None,
        "GET",
        None,
        login["common_headers"],
        None,
    )
    assert res.status_code == 200, (
        "Failed with response code: "
        + str(res.status_code)
        + " and response: "
        + str(res.json())
    )
    logger.info("\n ======= get_dynamic365_integration_config succeeded. =======")
    yield res


@pytest.fixture(scope="function")
def update_dynamic365_integration_config(login, get_dynamic365_integration_config):

    req_url = login["api_url"] + "/LiveChat/integrationDynamics365Config"

    res_get = get_dynamic365_integration_config.json()

    req_body = {
        "isDynamics365EntityCreatedAutomaticallyWhenChatEnded": "true",
        "autoActionWhenChatEnded": "createOrUpdateContactThenAttachCase",
        "contactAutoUpdateStrategyWhenChatEnded": "doNotUpdateContact",
        "autoActionWhenOfflineMessageReceived": "createOrUpdateContactThenAttachCase",
        "contactAutoUpdateStrategyWhenOfflineMessageReceived": "doNotUpdateContact",
    }

    req_body = replace_request_body_data_with_test_data(res_get, req_body)

    # pdb.set_trace()

    res = send_request(
        req_url,
        None,
        "PUT",
        None,
        login["common_headers"],
        req_body,
    )
    assert res.status_code == 200, (
        "Failed with response code: "
        + str(res.status_code)
        + " and response: "
        + str(res.json())
    )

    logger.info("\n ======= update_dynamic365_integration_config succeeded. =======")
    yield res


@pytest.fixture(scope="function")
def update_dynamic365_integration_field_mappings(
    login, get_dynamic365_integration_config
):

    req_url = login["api_url"] + "/LiveChat/integrationDynamics365Config"

    res_get = get_dynamic365_integration_config.json()

    res_get["integrationDynamics365FieldMappings"].extend(
        [
            {
                "isValidForUpdate": "true",
                "isValidForCreate": "true",
                "dynamics365FieldLabel": "Company Name",
                "siteId": 0,
                "dynamics365Entity": "contact",
                "dynamics365Field": "parentcustomerid",
                "comm100Field": "{!LiveChatFields.Company}",
                "isDisplayedInAgentConsole": "true",
                "isDeleted": "false",
                "id": "c8da9ac6-edb1-4dce-80ef-1f2d9aafdc46",
            }
        ]
    )

    req_body = res_get

    res = send_request(
        req_url,
        None,
        "PUT",
        None,
        login["common_headers"],
        req_body,
    )
    assert res.status_code == 200, (
        "Failed with response code: "
        + str(res.status_code)
        + " and response: "
        + str(res.json())
    )

    logger.info(
        "\n ======= update_dynamic365_integration_field_mappings succeeded. ======="
    )
    yield res


@pytest.fixture(scope="function")
def update_dynamic365_integration_identify_account_with_visitor_name(
    login, get_dynamic365_integration_config
):

    req_url = login["api_url"] + "/LiveChat/integrationDynamics365Config"

    res_get = get_dynamic365_integration_config.json()

    for item in res_get["integrationDynamics365EntityIdentificationRules"]:
        if item["dynamics365Entity"] == "account":
            item["integrationDynamics365EntityIdentificationRuleConditions"].extend(
                [
                    {
                        "dynamics365Field": "name",
                        "comm100Field": "{!Visitor.Name}",
                        "order": 1,
                        "ruleId": "50afc3e2-4da7-4b1d-9b4a-01e8a34aacef",
                    }
                ]
            )

    req_body = res_get

    # pdb.set_trace()

    res = send_request(
        req_url,
        None,
        "PUT",
        None,
        login["common_headers"],
        req_body,
    )
    assert res.status_code == 200, (
        "Failed with response code: "
        + str(res.status_code)
        + " and response: "
        + str(res.json())
    )

    logger.info(
        "\n ======= update_dynamic365_integration_identify_account_with_visitor_name succeeded. ======="
    )
    yield res


@pytest.fixture(scope="function")
def enable_salesforce_integration(login):
    login_data = login

    logger.info("\n ======= salesforce integration has been enabled. =======")
    yield None

    # teardown: disable salesforce integration
    logger.info("\n ======= salesforce integration has been disabled.  =======")


@pytest.fixture(scope="function")
def get_salesforce_integration_config(login, enable_salesforce_integration):

    req_url = login["api_url"] + "/LiveChat/integrationSalesforceConfig"

    res = send_request(
        req_url,
        None,
        "GET",
        None,
        login["common_headers"],
        None,
    )
    assert res.status_code == 200, (
        "Failed with response code: "
        + str(res.status_code)
        + " and response: "
        + str(res.json())
    )
    logger.info("\n ======= get_salesforce_integration_config succeeded. =======")
    yield res


@pytest.fixture(scope="function")
def update_salesforce_integration_identify_account(
    login, get_salesforce_integration_config
):

    req_url = login["api_url"] + "/LiveChat/integrationSalesforceConfig"

    res_get = get_salesforce_integration_config.json()

    res_get["integrationSalesforceCustomRuleFieldMappings"].extend(
        [
            {
                "salesforceObject": "account",
                "objectIdentityComm100Field": "{!Visitor.Name}",
                "objectIdentitySalesforceField": "Name",
                "objectIdentityIndex": 1,
            }
        ]
    )

    req_body = res_get

    res = send_request(
        req_url,
        None,
        "PUT",
        None,
        login["common_headers"],
        req_body,
    )
    assert res.status_code == 200, (
        "Failed with response code: "
        + str(res.status_code)
        + " and response: "
        + str(res.json())
    )

    logger.info(
        "\n ======= update_salesforce_integration_identify_account succeeded. ======="
    )
    yield res


@pytest.fixture(scope="module")
def init_webhook(login):
    login_data = login
    request_url_create = login_data["api_url"] + "/LiveChat/webhooks"
    request_body = {
        "event": "offlineMessageIsSubmitted",
        "targetUrl": "https://enkuiid6j65gf.x.pipedream.net/",
    }

    res = send_request(
        request_url_create,
        None,
        "POST",
        None,
        login_data["common_headers"],
        request_body,
    )
    assert res.status_code == 201, (
        "Failed with status code: "
        + str(res.status_code)
        + " and response: "
        + str(res.json())
    )
    logger.info("\n ======= webhook has been created =======")
    yield res

    created_id = res.json()["id"]
    request_url_delete = login_data["api_url"] + "/LiveChat/webhooks/" + created_id
    res_delete = send_request(
        request_url_delete, None, "DELETE", None, login_data["common_headers"], None
    )
    assert res_delete.status_code == 204, (
        "Failed with status code: "
        + str(res_delete.status_code)
        + " and response: "
        + str(res_delete.json())
    )
    logger.info("\n ======= newly-created webhook has been deleted =======")


@pytest.fixture(scope="function")
def enable_shift_config(login):
    login_data = login
    request_url_enable = login_data["api_url"] + "/LiveChat/shiftConfig:enable"
    res_enable = send_request(
        request_url_enable,
        None,
        "POST",
        None,
        login_data["common_headers"],
        None,
    )
    assert res_enable.status_code == 200, (
        "Failed with response code: "
        + str(res_enable.status_code)
        + " and response: "
        + str(res_enable.json())
    )
    logger.info("\n ======= Shift config has been enabled =======")
    yield res_enable

    request_url_disable = login_data["api_url"] + "/LiveChat/shiftConfig:disable"
    res_disable = send_request(
        request_url_disable,
        None,
        "POST",
        None,
        login_data["common_headers"],
        None,
    )
    assert res_disable.status_code == 200, (
        "Failed with response code: "
        + str(res_enable.status_code)
        + " and response: "
        + str(res_enable.json())
    )
    logger.info("\n ======= Shift config has been disabled =======")


@pytest.fixture(scope="function")
def create_shift(login):
    login_data = login
    agent_id = login_data["agent_id"]
    request_url_create = login_data["api_url"] + "/LiveChat/shifts"
    request_body = {
        "name": "temp shift",
        "timeZone": "China Standard Time",
        "agentIds": [agent_id],
    }

    res = send_request(
        request_url_create,
        None,
        "POST",
        None,
        login_data["common_headers"],
        request_body,
    )
    assert res.status_code == 201, (
        "Failed with status code: "
        + str(res.status_code)
        + " and response: "
        + str(res.json())
    )
    logger.info("\n ======= shift has been created =======")
    yield res

    created_id = res.json()["id"]
    request_url_delete = login_data["api_url"] + "/LiveChat/shifts/" + created_id
    res_delete = send_request(
        request_url_delete, None, "DELETE", None, login_data["common_headers"], None
    )
    assert res_delete.status_code == 204, (
        "Failed with status code: "
        + str(res_delete.status_code)
        + " and response: "
        + str(res_delete.json())
    )
    logger.info("\n ======= newly-created shift has been deleted =======")


@pytest.fixture(scope="function")
def init_shift(login, enable_shift_config, create_shift):
    # wait for new department added to chat server cache as interval is 5s
    time.sleep(6)
    yield create_shift


@pytest.fixture(scope="function")
def init_webhook_with_event_type_for_webhook_consumer(login):
    created_id = None
    login_data = login

    def _init_webhook_with_event_type_for_webhook_consumer(event_type: str):
        nonlocal created_id
        # login_data = login
        request_url_create = login_data["api_url"] + "/LiveChat/webhooks"
        request_body = {
            "event": event_type,
            "targetUrl": "https://enkuiid6j65gf.x.pipedream.net/",
        }

        res = send_request(
            request_url_create,
            None,
            "POST",
            None,
            login_data["common_headers"],
            request_body,
        )
        assert res.status_code == 201, (
            "Failed with status code: "
            + str(res.status_code)
            + " and response: "
            + str(res.json())
        )
        logger.info(
            "\n ======= webhook with type %s has been created, need wait for 3 mins to let consumer load the cache  =======",
            event_type,
        )
        # wait for 3 minutes to make sure the webhook config is reflected in webhook consumer cache.
        sleep(180)
        created_id = res.json()["id"]
        return res

    yield _init_webhook_with_event_type_for_webhook_consumer
    # pdb.set_trace()
    request_url_delete = login_data["api_url"] + "/LiveChat/webhooks/" + created_id
    res_delete = send_request(
        request_url_delete, None, "DELETE", None, login_data["common_headers"], None
    )
    assert res_delete.status_code == 204, (
        "Failed with status code: "
        + str(res_delete.status_code)
        + " and response: "
        + str(res_delete.json())
    )
    logger.info("\n ======= newly-created webhook has been deleted =======")
    # wait for 3 minutes to make sure the webhook config is reflected in webhook consumer cache. 想了一下应该是不需要等,因为每个用例都单独创建自己的event,不会有A用例创建了B用例的event的情况
    # sleep(180)


@pytest.fixture(scope="session")
def init_webhook_with_full_event_type_for_webhook_consumer(login):
    login_data = login
    event_types = [
        "offlineMessageIsSubmitted",
        "chatStarts",
        "chatEnds",
        "chatIsWrappedUp",
        "agentStatusChanges",
        "chatIsRequested",
        "chatIsTransferred",
    ]

    event_type_ids = []

    for event_type in event_types:
        request_url_create = login_data["api_url"] + "/LiveChat/webhooks"
        request_body = {
            "event": event_type,
            "targetUrl": "https://enkuiid6j65gf.x.pipedream.net/",
        }

        res = send_request(
            request_url_create,
            None,
            "POST",
            None,
            login_data["common_headers"],
            request_body,
        )
        assert res.status_code == 201, (
            "Failed with status code: "
            + str(res.status_code)
            + " and response: "
            + str(res.json())
        )
        created_id = res.json()["id"]
        event_type_ids.append(created_id)
        logger.info(
            "\n ======= webhook with type %s has been created, need wait for 3 mins to let consumer load the cache  =======",
            event_type,
        )
    # wait for 3 minutes to make sure the webhook config is reflected in webhook consumer cache.
    sleep(180)
    yield event_type_ids

    for created_id in event_type_ids:
        request_url_delete = login_data["api_url"] + "/LiveChat/webhooks/" + created_id
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
            "\n ======= newly-created webhook %s has been deleted, need wait for 3 mins to let consumer load the cache  =======",
            event_type,
        )
    # wait for 3 minutes to make sure the webhook config is reflected in webhook consumer cache.
    sleep(180)


@pytest.fixture(scope="module")
def init_conversion_action(login):
    login_data = login
    request_url_create = login_data["api_url"] + "/LiveChat/conversionActions"
    request_body = {
        "name": "new conversion action",
        "isEnabled": True,
        "type": "URL",
        "usedToDetermineConversionCustomVariableId": "00000000-0000-0000-0000-000000000000",
        "operator": "contains",
        "value": "comm100",
        "isCaseSensitive": True,
        "isValueAssignedToConversion": True,
        "valueSource": "inputAValue",
        "chatAssociatedWithConversion": "theFirstChat",
        "isChatInLastCertainDaysConsidered": True,
        "chatInLastDays": 1,
        "isChatWithAtLeastCertainVisitorMessagesConsidered": True,
        "visitorMessagesAtLeast": 1,
        "isVariableIncludedInTranscript": True,
        "appendFieldList": ["{!Visitor.Time Zone}"],
        "assignedValueFromInputting": 10,
    }

    res = send_request(
        request_url_create,
        None,
        "POST",
        None,
        login_data["common_headers"],
        request_body,
    )
    assert res.status_code == 201, (
        "Failed with status code: "
        + str(res.status_code)
        + " and response: "
        + str(res.json())
    )
    logger.info("\n ======= conversion action has been created =======")
    yield res

    created_id = res.json()["id"]
    request_url_delete = (
        login_data["api_url"] + "/LiveChat/conversionActions/" + created_id
    )
    res_delete = send_request(
        request_url_delete, None, "DELETE", None, login_data["common_headers"], None
    )
    assert res_delete.status_code == 204, (
        "Failed with status code: "
        + str(res_delete.status_code)
        + " and response: "
        + str(res_delete.json())
    )
    logger.info("\n ======= newly-created conversion action has been deleted =======")


@pytest.fixture(scope="function")
def init_conversion_action_api_type(login):
    login_data = login
    request_url_create = login_data["api_url"] + "/LiveChat/conversionActions"
    request_body = {
        "name": "by_api",
        "isEnabled": True,
        "type": "API",
        "usedToDetermineConversionCustomVariableId": "00000000-0000-0000-0000-000000000000",
        "operator": "is",
        "value": "",
        "isCaseSensitive": True,
        "isValueAssignedToConversion": False,
        "valueSource": "inputAValue",
        "chatAssociatedWithConversion": "theFirstChat",
        "isChatInLastCertainDaysConsidered": False,
        "chatInLastDays": 1,
        "isChatWithAtLeastCertainVisitorMessagesConsidered": False,
        "visitorMessagesAtLeast": 1,
        "isVariableIncludedInTranscript": False,
        "appendFieldList": [],
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
    logger.info("\n ======= conversion action with api type has been created =======")
    yield res

    created_id = res.json()["id"]
    request_url_delete = (
        login_data["api_url"] + "/LiveChat/conversionActions/" + created_id
    )
    res_delete = send_request(
        request_url_delete, None, "DELETE", None, login_data["common_headers"], None
    )
    assert res_delete.status_code == 204, (
        "Failed with status code: "
        + str(res_delete.status_code)
        + " and response: "
        + str(res_delete.json())
    )
    logger.info("\n ======= newly-created conversion action has been deleted =======")


@pytest.fixture(scope="function")
def conversion_achieved(login):
    def _conversion_achieved(conversion_name: str, visitor_guid: str):
        login_data = login
        req_url = login_data["api_url"] + "/LiveChat/conversionActions/achieved"
        req_body = {
            "name": conversion_name,
            "value": 100,
            "visitorGuid": visitor_guid,
        }

        res = send_request(
            req_url,
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
        logger.info(
            "\n ======= conversion action has been marked as successful via api. ======="
        )

    yield _conversion_achieved


@pytest.fixture(scope="session")
def clean_up_init_segment(login):
    login_data = login
    request_url_get = login_data["api_url"] + "/LiveChat/segments"
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

    if len(res_get.json()) > 0:
        for segment in res_get.json():
            if "temp" in segment["name"]:
                segment_id = segment["id"]
                request_url_delete = (
                    login_data["api_url"] + "/LiveChat/segments/" + segment_id
                )
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
        logger.info("\n ======= existing temp segments have been cleaned up =======")


@pytest.fixture(scope="function")
def create_segment(login, clean_up_init_segment):
    login_data = login
    # create a segment that will always be matched
    request_url_create = login_data["api_url"] + "/LiveChat/segments"
    request_body = {
        "name": "temp segment",
        "isEnabled": True,
        "color": "#0033e2",
        "description": "",
        "conditionMetType": "all",
        "logicalExpression": "",
        "segmentConditions": [
            {
                "fieldName": "{!Visitor.Number of visits}",
                "operator": "isLessThan",
                "value": "100",
                "order": 1,
                "description": "Number of visits is less than 100",
            },
        ],
        "alertToType": "none",
        "agentIds": [],
        "departmentIds": [],
    }

    res_create = send_request(
        request_url_create,
        None,
        "POST",
        None,
        login_data["common_headers"],
        request_body,
    )
    assert res_create.status_code == 201, (
        "Failed with status code: "
        + str(res_create.status_code)
        + " and response: "
        + str(res_create.json())
    )
    logger.info("\n ======= segment has been created =======")
    yield res_create

    # teardown: delete segment
    created_id = res_create.json()["id"]
    request_url_delete = login_data["api_url"] + "/LiveChat/segments/" + created_id
    res_delete = send_request(
        request_url_delete, None, "DELETE", None, login_data["common_headers"], None
    )
    assert res_delete.status_code == 204, (
        "Failed with status code: "
        + str(res_delete.status_code)
        + " and response: "
        + str(res_delete.json())
    )
    logger.info("\n ======= newly-created segment has been deleted =======")


@pytest.fixture(scope="function")
def enable_segment_config(login):
    login_data = login
    # need enable segment config first
    request_url_enable = login_data["api_url"] + "/LiveChat/segmentConfig:enable"
    res_enable = send_request(
        request_url_enable,
        None,
        "POST",
        None,
        login_data["common_headers"],
        None,
    )
    assert res_enable.status_code == 200, (
        "Failed with status code: "
        + str(res_enable.status_code)
        + " and response: "
        + str(res_enable.json())
    )
    logger.info("\n ======= segment config has been enabled =======")
    yield res_enable

    # teardown: disable segment config
    request_url_disable = login_data["api_url"] + "/LiveChat/segmentConfig:disable"
    res_disable = send_request(
        request_url_disable,
        None,
        "POST",
        None,
        login_data["common_headers"],
        None,
    )
    assert res_disable.status_code == 200, (
        "Failed with status code: "
        + str(res_disable.status_code)
        + " and response: "
        + str(res_disable.json())
    )
    logger.info("\n ======= segment config has been disabled =======")


@pytest.fixture(scope="function")
def init_segment(login, enable_segment_config, create_segment):
    login_data = login

    res_create = create_segment
    sleep(5)  # make sure chat server cache is updated
    yield res_create


# create a fixture as factory to ban a visitor, using visitor_guid as parameter
@pytest.fixture(scope="function")
def ban_visitor(login):
    login_data = login
    req_url = login_data["api_url"] + "/livechat/bannedVisitors"

    def _ban_visitor(visitor_guid: str):
        req_body_create = {"visitorId": visitor_guid, "comment": ""}

        res_create = send_request(
            req_url,
            None,
            "POST",
            None,
            login_data["common_headers"],
            req_body_create,
        )

        # pdb.set_trace()
        assert res_create.status_code == 201, "Failed with response: " + str(
            res_create.json()
        )
        logger.info(
            f"\n =======  visitor guid banned via livechatapi successfully ======="
        )

        # wait for banned visitor added to chat server cache as interval is 5s
        time.sleep(5)

    yield _ban_visitor

    # get banned visitor list first
    res_get_banned_visitors = send_request(
        req_url, None, "GET", None, login_data["common_headers"], None
    )
    assert res_get_banned_visitors.status_code == 200, "Failed with response: " + str(
        res_get_banned_visitors.json()
    )

    banned_visitor_list = res_get_banned_visitors.json()["bannedVisitors"]
    banned_visitor_record_id_list = []
    # iterate banned_visitor_list to get all banned visitor record ids
    for banned_visitor in banned_visitor_list:
        banned_visitor_record_id_list.append(banned_visitor["id"])

    # delete all banned visitor guids
    res_delete = send_request(
        req_url,
        None,
        "DELETE",
        None,
        login_data["common_headers"],
        banned_visitor_record_id_list,
    )

    # pdb.set_trace()
    assert res_delete.status_code == 204, "Failed with response: " + str(
        res_delete.json()
    )
    logger.info(
        f"\n ======= All banned visitor guids have been deleted. You can use these visitors again. ======="
    )


def delete_banned_visitor_guid(login, banned_visitor_record_id):
    login_data = login

    request_url_delete = (
        login_data["api_url"] + "/livechat/bannedVisitors/" + banned_visitor_record_id
    )

    res_delete = send_request(
        request_url_delete,
        None,
        "DELETE",
        None,
        login_data["common_headers"],
        None,
    )

    # pdb.set_trace()
    assert res_delete.status_code == 204, "Failed with response: " + str(
        res_delete.json()
    )
    logger.info(f"\n =======  banned visitor guid has been deleted =======")


@pytest.fixture(scope="session")
def get_wrapup_category_option(login):
    login_data = login
    req_url = login_data["api_url"] + "/livechat/wrapupCategoryOptions"

    res = send_request(
        req_url,
        None,
        "GET",
        None,
        login_data["common_headers"],
        None,
    )

    # pdb.set_trace()
    assert res.status_code == 200, "Failed with response: " + str(res.json())
    first_option_id = res.json()[0]["id"]
    second_option_id = res.json()[1]["id"]

    logger.info("\n ======= get_wrapup_category_option succeeded. =======")
    yield res, first_option_id, second_option_id

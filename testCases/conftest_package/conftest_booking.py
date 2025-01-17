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
def init_booking_page(login):
    login_data = login
    request_url_create = login_data["api_url"] + "/Booking/bookingHomePages"
    request_body = {
        "themeColor": "#329fd9",
        "greetingMessage": "Welcome!",
        "name": "temp booking page",
        "logo": None,
    }
    request_params = {"siteId": login_data["site_id"]}

    res = send_request(
        request_url_create,
        request_params,
        "POST",
        None,
        login_data["common_headers"],
        request_body,
    )
    # pdb.set_trace()
    assert res.status_code == 201
    logger.info("\n ======= booking page has been created =======")
    yield res

    created_id = res.json()["id"]
    request_url_delete = (
        login_data["api_url"] + "/Booking/bookingHomePages/" + created_id
    )
    res_delete = send_request(
        request_url_delete,
        request_params,
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
    logger.info("\n ======= newly-created booking page has been deleted =======")


@pytest.fixture(scope="module")
def init_service(login, init_booking_page):
    login_data = login
    booking_page = init_booking_page
    booking_page_id = booking_page.json()["id"]

    request_url_create = login_data["api_url"] + "/Booking/services"
    request_body = {
        "name": "temp service",
        "color": "#329ed8",
        "bookingHomePageId": booking_page_id,
        "description": "",
        "duration": 30,
    }
    request_params = {"siteId": login_data["site_id"]}

    res_create = send_request(
        request_url_create,
        request_params,
        "POST",
        None,
        login_data["common_headers"],
        request_body,
    )
    # pdb.set_trace()
    assert res_create.status_code == 201
    logger.info("\n ======= service has been created =======")
    yield res_create

    created_id = res_create.json()["id"]
    request_url_delete = login_data["api_url"] + "/Booking/services/" + created_id
    res_delete = send_request(
        request_url_delete,
        request_params,
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
    logger.info("\n ======= newly-created service has been deleted =======")


@pytest.fixture(scope="module")
def init_agent_page(login, init_service):
    login_data = login
    agent1_id = login_data["agent_id"]
    agent2_id = login_data["agent2_id"]
    service = init_service
    service_id = service.json()["id"]

    # We need to add agents to service first.
    request_url = login_data["api_url"] + f"/Booking/services/{service_id}"
    request_body = {
        "id": service_id,
        "agentIds": [agent1_id, agent2_id],
        "minimumLeadTime": 1,
    }  # we need to set mimumLeadTime to 1 hour so that we can book for next day.
    request_params = {"siteId": login_data["site_id"]}

    res = send_request(
        request_url,
        request_params,
        "PUT",
        None,
        login_data["common_headers"],
        request_body,
    )
    # pdb.set_trace()
    assert res.status_code == 200

    logger.info("\n ======= 2 agents has been added to newly-created service =======")

    # add the agent1 and agent2 sat & sun working hour so we can add appointment every next day
    request_url_get = login_data["api_url"] + f"/Booking/agentHomePages"

    res_get = send_request(
        request_url_get,
        request_params,
        "GET",
        None,
        login_data["common_headers"],
        None,
    )
    # pdb.set_trace()
    assert res_get.status_code == 200

    # get agent1 agent page data
    request_url_agent1_get = (
        login_data["api_url"] + f"/Booking/agentHomePages/" + res_get.json()[0]["id"]
    )
    request_get_agent1 = send_request(
        request_url_agent1_get,
        request_params,
        "GET",
        None,
        login_data["common_headers"],
        None,
    )
    assert request_get_agent1.status_code == 200

    request_url_agent1_update = (
        login_data["api_url"] + f"/Booking/agentHomePages/" + res_get.json()[0]["id"]
    )
    # pdb.set_trace()

    request_update_agent1_body = request_get_agent1.json()
    request_update_agent1_body["workingHours"].extend(
        [
            {
                "dayOfWeek": "Saturday",
                "startTime": "09:00:00",
                "endTime": "17:00:00",
                "availableServices": [service_id],
                "isEnabled": True,
            },
            {
                "dayOfWeek": "Sunday",
                "startTime": "09:00:00",
                "endTime": "17:00:00",
                "availableServices": [service_id],
                "isEnabled": True,
            },
        ]
    )
    # pdb.set_trace()
    request_update_agent1 = send_request(
        request_url_agent1_update,
        request_params,
        "PUT",
        None,
        login_data["common_headers"],
        request_update_agent1_body,
    )
    assert request_update_agent1.status_code == 200

    # get agent2 agent page data
    request_url_agent2_get = (
        login_data["api_url"] + f"/Booking/agentHomePages/" + res_get.json()[1]["id"]
    )
    request_get_agent2 = send_request(
        request_url_agent2_get,
        request_params,
        "GET",
        None,
        login_data["common_headers"],
        None,
    )
    assert request_get_agent2.status_code == 200

    request_url_agent2_update = (
        login_data["api_url"] + f"/Booking/agentHomePages/" + res_get.json()[1]["id"]
    )
    request_update_agent2_body = request_get_agent2.json()
    request_update_agent2_body["workingHours"].extend(
        [
            {
                "dayOfWeek": "Saturday",
                "startTime": "09:00:00",
                "endTime": "17:00:00",
                "availableServices": [service_id],
                "isEnabled": True,
            },
            {
                "dayOfWeek": "Sunday",
                "startTime": "09:00:00",
                "endTime": "17:00:00",
                "availableServices": [service_id],
                "isEnabled": True,
            },
        ]
    )
    request_update_agent2 = send_request(
        request_url_agent2_update,
        request_params,
        "PUT",
        None,
        login_data["common_headers"],
        request_update_agent2_body,
    )
    assert request_update_agent2.status_code == 200

    # Then we can get agent pages.
    request_url_get = login_data["api_url"] + f"/Booking/agentHomePages"

    res_get = send_request(
        request_url_get,
        request_params,
        "GET",
        None,
        login_data["common_headers"],
        None,
    )
    # pdb.set_trace()
    assert res_get.status_code == 200

    logger.info("\n ======= 2 agent pages have been generated =======")
    yield res_get


@pytest.fixture(scope="module")
def init_agent_page_agent_calendar_account(login, init_agent_page):
    # logger.info("\n ======= start to integrate ex server =======")
    login_data = login
    agent1_id = login_data["agent_id"]

    # agent_page = init_agent_page

    # agent_page_id = agent_page.json()[0]["id"]

    request_url = login_data["api_url"] + f"/Booking/agentCalendarAccounts"
    request_body = {
        "agentId": agent1_id,
        "calendarType": "MicrosoftExchange",
        "configuration": '{"exchangeEmailAddress":"api@es.com","exchangeServerUrl":"https://es.testing.comm100dev.io/ews/exchange.asmx","exchangeUserName":"api"}',
        "credential": '{"exchangePassword":"Aa00000000"}',
    }
    request_params = {"siteId": login_data["site_id"]}

    res_integration = send_request(
        request_url,
        request_params,
        "POST",
        None,
        login_data["common_headers"],
        request_body,
    )

    calendar_account_id = res_integration.json()["id"]
    # pdb.set_trace()
    assert res_integration.status_code == 200
    assert res_integration.json()["agentId"] == agent1_id
    assert res_integration.json()["calendarType"] == "MicrosoftExchange"
    assert res_integration.json()["isDeleted"] == False

    logger.info(
        "\n ======= exchange server integration account api successfully ======="
    )

    yield res_integration

    # disconnect exchange server
    request_url_disconnect = (
        login_data["api_url"]
        + f"/booking/agentCalendarAccounts/{calendar_account_id}:disconnect"
    )
    # request_body_disconnect = { }

    res_integration_disconnect = send_request(
        request_url_disconnect,
        request_params,
        "POST",
        None,
        login_data["common_headers"],
        None,
    )
    # pdb.set_trace()
    assert res_integration_disconnect.status_code == 200
    logger.info(
        "\n ======= exchange server disconnect account api successfully ======="
    )


@pytest.fixture(scope="module")
def init_agent_page_agent_calendar_account2(login, init_agent_page):
    login_data = login
    agent2_id = login_data["agent2_id"]

    # agent_page = init_agent_page

    # agent_page_id = agent_page.json()[0]["id"]

    request_url = login_data["api_url"] + f"/Booking/agentCalendarAccounts"
    request_body = {
        "agentId": agent2_id,
        "calendarType": "MicrosoftExchange",
        "configuration": '{"exchangeEmailAddress":"api2@es.com","exchangeServerUrl":"https://es.testing.comm100dev.io/ews/exchange.asmx","exchangeUserName":"api2"}',
        "credential": '{"exchangePassword":"Aa00000000"}',
    }
    request_params = {"siteId": login_data["site_id"]}

    res_integration = send_request(
        request_url,
        request_params,
        "POST",
        login_data["auth2"],
        None,
        request_body,
    )

    calendar_account_id = res_integration.json()["id"]
    # pdb.set_trace()
    assert res_integration.status_code == 200
    assert res_integration.json()["agentId"] == agent2_id
    assert res_integration.json()["calendarType"] == "MicrosoftExchange"
    assert res_integration.json()["isDeleted"] == False

    logger.info(
        "\n ======= exchange server integration account api2 successfully ======="
    )

    yield res_integration

    # disconnect exchange server
    request_url_disconnect = (
        login_data["api_url"]
        + f"/booking/agentCalendarAccounts/{calendar_account_id}:disconnect"
    )
    # request_body_disconnect = { }

    res_integration_disconnect = send_request(
        request_url_disconnect,
        request_params,
        "POST",
        login_data["auth2"],
        None,
        None,
    )
    # pdb.set_trace()
    assert res_integration_disconnect.status_code == 200
    logger.info(
        "\n ======= exchange server disconnect account api2 successfully ======="
    )


@pytest.fixture(scope="module")
def init_appointment(login, init_service, init_agent_page):
    login_data = login
    service = init_service
    service_id = service.json()["id"]
    request_params = {"siteId": login_data["site_id"]}

    # get service fields
    request_url_get = (
        login_data["api_url"] + f"/Booking/services/{service_id}?include=serviceField"
    )

    res_get = send_request(
        request_url_get,
        request_params,
        "GET",
        None,
        login_data["common_headers"],
        None,
    )
    # pdb.set_trace()
    assert res_get.status_code == 200

    # then we can create appointment
    name_field_id = res_get.json()["serviceFields"][1]["id"]
    email_field_id = res_get.json()["serviceFields"][0]["id"]
    name = fake.name()
    email = fake.email()
    next_monday_date = get_next_weekday(0)

    request_url = login_data["api_url"] + f"/booking/appointments"
    request_body = {
        "appointmentFieldResults": [
            {"fieldId": name_field_id, "fieldValue": name},
            {"fieldId": email_field_id, "fieldValue": email},
        ],
        "appointmentStartTime": next_monday_date + "T09:00:00.000",
        "appointmentEndTime": next_monday_date + "T09:30:00.000",
        "visitorTimeZone": "China Standard Time",
        "serviceId": service_id,
    }

    res_create = send_request(
        request_url,
        request_params,
        "POST",
        None,
        None,
        request_body,
    )
    # pdb.set_trace()
    assert res_create.status_code == 201
    assert res_create.json()["createdByType"] == "Visitor"
    logger.info("\n ======= appointment has been created by visitor =======")
    yield res_create

    # ======== cancel newly-created appointment ========
    created_id = res_create.json()["id"]
    request_url_delete = (
        login_data["api_url"] + f"/booking/appointments/{created_id}:cancel"
    )
    res_cancel = send_request(
        request_url_delete,
        request_params,
        "POST",
        None,
        None,
        {"cancelMessage": "cancel this by visitor"},
    )
    # pdb.set_trace()
    assert res_cancel.status_code == 200
    assert res_cancel.json()["status"] == "cancelled"
    assert res_cancel.json()["cancelledByType"] == "visitor"

    logger.info(
        "\n  ======= newly-created appointment has been cancelled by visitor ======= "
    )


@pytest.fixture(scope="module")
def init_appointment_by_agent(login, init_service, init_agent_page):
    login_data = login
    service = init_service
    service_id = service.json()["id"]
    request_params = {"siteId": login_data["site_id"]}

    # get service fields
    request_url_get = (
        login_data["api_url"] + f"/Booking/services/{service_id}?include=serviceField"
    )

    res_get = send_request(
        request_url_get,
        request_params,
        "GET",
        None,
        login_data["common_headers"],
        None,
    )
    # pdb.set_trace()
    assert res_get.status_code == 200

    # then we can create appointment
    name_field_id = res_get.json()["serviceFields"][1]["id"]
    email_field_id = res_get.json()["serviceFields"][0]["id"]
    name = fake.name()
    email = fake.email()
    next_monday_date = get_next_weekday(0)

    request_url = login_data["api_url"] + f"/booking/appointments"
    request_body = {
        "appointmentFieldResults": [
            {"fieldId": name_field_id, "fieldValue": name},
            {"fieldId": email_field_id, "fieldValue": email},
        ],
        "appointmentStartTime": next_monday_date + "T09:00:00.000",
        "appointmentEndTime": next_monday_date + "T09:30:00.000",
        "visitorTimeZone": "China Standard Time",
        "serviceId": service_id,
    }

    res_create = send_request(
        request_url,
        request_params,
        "POST",
        None,
        login_data["common_headers"],
        request_body,
    )
    # pdb.set_trace()
    assert res_create.status_code == 201
    assert res_create.json()["createdByType"] == "Agent"
    logger.info("\n ======= appointment has been created by agent =======")
    yield res_create

    # ======== cancel newly-created appointment ========
    created_id = res_create.json()["id"]
    request_url_delete = (
        login_data["api_url"] + f"/booking/appointments/{created_id}:cancel"
    )
    res_cancel = send_request(
        request_url_delete,
        request_params,
        "POST",
        None,
        login_data["common_headers"],
        {"cancelMessage": "cancel this by agent"},
    )
    # pdb.set_trace()
    assert res_cancel.status_code == 200
    assert res_cancel.json()["status"] == "cancelled"
    assert res_cancel.json()["cancelledByType"] == "agent"

    logger.info(
        "\n ======= newly-created appointment has been cancelled by agent ======="
    )


@pytest.fixture(scope="module")
def init_appointment_by_agent_in_exchange(
    login, init_service, init_agent_page, init_agent_page_agent_calendar_account
):
    login_data = login
    agent_id = login_data["agent_id"]
    service = init_service
    service_id = service.json()["id"]
    request_params = {"siteId": login_data["site_id"]}

    # get service fields
    request_url_get = (
        login_data["api_url"] + f"/Booking/services/{service_id}?include=serviceField"
    )

    res_get = send_request(
        request_url_get,
        request_params,
        "GET",
        None,
        login_data["common_headers"],
        None,
    )
    # pdb.set_trace()
    assert res_get.status_code == 200

    # then we can create appointment
    for i in range(len(res_get.json()["serviceFields"])):
        if res_get.json()["serviceFields"][i]["name"] == "Name":
            name_field_id = res_get.json()["serviceFields"][i]["id"]
        if res_get.json()["serviceFields"][i]["name"] == "Email":
            email_field_id = res_get.json()["serviceFields"][i]["id"]

    # name_field_id = res_get.json()["serviceFields"][1]["id"]
    # email_field_id = res_get.json()["serviceFields"][0]["id"]
    name = fake.name()
    email = fake.email()
    next_monday_date = get_next_weekday(0)

    request_url = login_data["api_url"] + f"/booking/appointments"
    request_body = {
        "appointmentFieldResults": [
            {"fieldId": name_field_id, "fieldValue": name},
            {"fieldId": email_field_id, "fieldValue": email},
        ],
        "appointmentStartTime": next_monday_date + "T09:00:00.000",
        "appointmentEndTime": next_monday_date + "T09:30:00.000",
        "visitorTimeZone": "China Standard Time",
        "serviceId": service_id,
    }

    res_create = send_request(
        request_url,
        request_params,
        "POST",
        None,
        login_data["common_headers"],
        request_body,
    )
    # pdb.set_trace()
    assert res_create.status_code == 201, ("Response is: ", res_create.json())
    assert res_create.json()["createdByType"] == "Agent"
    logger.info("\n ======= appointment has been created by agent =======")

    # get exchange appointment
    sleep(5)  # wait for appointment to be synced to exchange server
    request_url_get_exchange_appointment = (
        login_data["api_url"] + f"/booking/appointments:calendarSearch"
    )

    request_body_get_exchange_appointment = {
        "agentIds": [agent_id],
        "startTime": next_monday_date + "T00:00:00.000Z",
        "endTime": next_monday_date + "T16:00:00.000Z",
    }
    res_get_exchange_appointment = send_request(
        request_url_get_exchange_appointment,
        request_params,
        "POST",
        None,
        login_data["common_headers"],
        request_body_get_exchange_appointment,
    )
    # pdb.set_trace()
    while res_get_exchange_appointment.status_code != 200:
        sleep(5)
        res_get_exchange_appointment = send_request(
            request_url_get_exchange_appointment,
            request_params,
            "POST",
            None,
            login_data["common_headers"],
            request_body_get_exchange_appointment,
        )
        # pdb.set_trace()
    assert (
        res_get_exchange_appointment.status_code == 200
    )  # henrytodo: sometimes it's 500
    # assert res_get_exchange_appointment.json()[0]["calendarType"] == "MicrosoftExchange"
    logger.info("\n ======= exchange appointment has been returned =======")

    yield res_get_exchange_appointment

    # ======== cancel newly-created appointment ========
    created_id = res_create.json()["id"]
    request_url_delete = (
        login_data["api_url"] + f"/booking/appointments/{created_id}:cancel"
    )
    res_cancel = send_request(
        request_url_delete,
        request_params,
        "POST",
        None,
        login_data["common_headers"],
        {"cancelMessage": "cancel this by agent"},
    )
    # pdb.set_trace()
    assert res_cancel.status_code == 200
    assert res_cancel.json()["status"] == "cancelled"
    assert res_cancel.json()["cancelledByType"] == "agent"

    logger.info(
        "\n ======= newly-created appointment has been cancelled by agent ======="
    )


@pytest.fixture(scope="module")
def init_microsoft_exchange_tomorrow_data_in_exchange_server(
    login, init_service, init_agent_page, init_agent_page_agent_calendar_account
):
    login_data = login
    service = init_service
    service_id = service.json()["id"]
    request_params = {"siteId": login_data["site_id"]}

    # get service fields
    request_url_get = (
        login_data["api_url"] + f"/Booking/services/{service_id}?include=serviceField"
    )

    res_get = send_request(
        request_url_get,
        request_params,
        "GET",
        None,
        login_data["common_headers"],
        None,
    )
    # pdb.set_trace()
    assert res_get.status_code == 200

    # then we can create appointment
    for i in range(len(res_get.json()["serviceFields"])):
        if res_get.json()["serviceFields"][i]["name"] == "Name":
            name_field_id = res_get.json()["serviceFields"][i]["id"]
        if res_get.json()["serviceFields"][i]["name"] == "Email":
            email_field_id = res_get.json()["serviceFields"][i]["id"]

    # name_field_id = res_get.json()["serviceFields"][1]["id"]
    # email_field_id = res_get.json()["serviceFields"][2]["id"]
    name = fake.name()
    email = "api2@es.com"
    tomorrow_date = (datetime.now() + timedelta(days=1)).strftime("%Y-%m-%d")

    request_url = login_data["api_url"] + f"/booking/appointments"
    request_body = {
        "appointmentFieldResults": [
            {"fieldId": name_field_id, "fieldValue": name},
            {"fieldId": email_field_id, "fieldValue": email},
        ],
        "appointmentStartTime": tomorrow_date + "T09:00:00.000",
        "appointmentEndTime": tomorrow_date + "T09:30:00.000",
        "visitorTimeZone": "China Standard Time",
        "serviceId": service_id,
        "agentId": login_data["agent_id"],
    }

    res_create = send_request(
        request_url,
        request_params,
        "POST",
        None,
        login_data["common_headers"],
        request_body,
    )
    # pdb.set_trace()
    assert res_create.status_code == 201
    assert res_create.json()["createdByType"] == "Agent"
    logger.info("\n ======= appointment has been created by agent =======")

    yield res_create

    # ======== cancel newly-created appointment ========
    created_id = res_create.json()["id"]
    request_url_delete = (
        login_data["api_url"] + f"/booking/appointments/{created_id}:cancel"
    )
    res_cancel = send_request(
        request_url_delete,
        request_params,
        "POST",
        None,
        login_data["common_headers"],
        {"cancelMessage": "cancel this by agent"},
    )
    # pdb.set_trace()
    assert res_cancel.status_code == 200
    assert res_cancel.json()["status"] == "cancelled"
    assert res_cancel.json()["cancelledByType"] == "agent"

    logger.info(
        "\n ======= newly-created appointment has been cancelled by agent ======="
    )

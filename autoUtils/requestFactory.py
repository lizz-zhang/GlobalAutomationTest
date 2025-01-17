# -*- coding: utf-8 -*-
"""
======================
@author:nash
@time:12/17/2021:3:18 PM
@email:nash.xiang@comm100.com
======================
"""

import requests

from autoUtils.fileReader import read_config_file

import logging
import requests
from autoUtils.fileReader import read_config_file
from autoUtils.manage_global_data import ManageGlobalData
from urllib.parse import urlparse
logger = logging.getLogger(__name__)

def test_api_request(request_url, request_type, request_header, request_body):
    response = None
    if request_type == 'GET':
        response = requests.get(request_url, json=request_body, headers=request_header)
    elif request_type == 'POST':
        response = requests.post(request_url, json=request_body, headers=request_header)
    elif request_type == 'PUT':
        response = requests.put(request_url, json=request_body, headers=request_header)
    elif request_type == 'DELETE':
        response = requests.delete(request_url, json=request_body, headers=request_header)

    return response

def test_api_basic_auth_request(request_url, request_type, request_body):
    response = None
    environment = ManageGlobalData().get_global_value()
    config_data_json_dict = read_config_file('environments.json')
    email_name = config_data_json_dict[environment]['agent']['email']
    password = config_data_json_dict[environment]['agent']['apiKey']
    common_header = config_data_json_dict[environment]['commonHeaders']
    if request_type == 'GET':
        response = requests.get(request_url, auth=(email_name,password), headers=common_header)
    elif request_type == 'POST':
        response = requests.post(request_url, auth=(email_name,password), json=request_body, headers=common_header)
    elif request_type == 'PUT':
        response = requests.put(request_url, auth=(email_name,password), json=request_body, headers=common_header)
    elif request_type == 'DELETE':
        response = requests.delete(request_url, auth=(email_name,password), json=request_body, headers=common_header)

    return response

def get_root_domain(url):
    parsed_url = urlparse(url)
    domain_parts = parsed_url.netloc.split(".")
    if len(domain_parts) > 2:
        return "." + ".".join(domain_parts[-2:])
    return parsed_url.netloc

def send_request(
    request_url,
    request_params,
    request_type,
    request_auth,
    request_header,
    request_body,
    request_data=None,
):
    response = None

    if request_type == "GET":
        response = requests.get(
            request_url,
            params=request_params,
            auth=request_auth,
            headers=request_header,
        )
    elif request_type == "POST":
        response = requests.post(
            request_url,
            params=request_params,
            auth=request_auth,
            json=request_body,
            headers=request_header,
            data=request_data,
        )
    elif request_type == "PUT":
        response = requests.put(
            request_url,
            params=request_params,
            auth=request_auth,
            json=request_body,
            headers=request_header,
        )
    elif request_type == "DELETE":
        response = requests.delete(
            request_url,
            params=request_params,
            auth=request_auth,
            headers=request_header,
            json=request_body,
        )

    return response

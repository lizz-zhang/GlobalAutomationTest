# -*- coding: utf-8 -*-
"""
======================
@author:Mila
@time:04/27/2022:3:18 PM
@email:Mila.song@comm100.com
======================
"""
import json
import pdb
import pytest
import allure
import os

# from autoUtils.assertFactory import commonResponseAssert, illegalInputTestResponseAssert, afterCaseActionAndAssert
import requests

from autoUtils.assertFactory import commonResponseAssert
from autoUtils.requestFactory import test_api_request
from autoUtils.ymlLib import ReadFile
# from autoUtils.optionUtil import searchAndChangeDict, ifItemInKeysAndValueNotNone
from autoUtils.manage_global_data import ManageGlobalData

basedir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))))
fileName = basedir + '\\apiTestData\\global\\platform\\loginApi\\' + os.path.basename(__file__).split('.')[0] + '.yml'
readfile = ReadFile(fileName)
cases, parameters = readfile.get_businessTests_data()

class TestLogin:
    # request_url, request_type, request_header, request_body
    @pytest.mark.loginapi
    @pytest.mark.mila
    @pytest.mark.smoke
    @pytest.mark.parametrize('case, http, expect', list(parameters), ids=cases)
    @pytest.mark.parametrize('initial_data', ['agents'], indirect=True)
    def test_login(self, case, http, expect, login, initial_data):
        login_info = login
        env_dash = login_info['dashUrl']
        initial_agent = initial_data
        site_id = ManageGlobalData().get_site_id()
        body_temp = str(http['body']).replace("$siteId$", str(site_id))
        get_response = test_api_request(env_dash + http['path'].replace('$siteId$', str(site_id)), http['method'],login_info['commonHeader'], body_temp)
        commonResponseAssert(get_response, expect)

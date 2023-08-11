# -*- coding: utf-8 -*-
import json
import pdb
import pytest
import allure
import os

# from autoUtils.assertFactory import commonResponseAssert, illegalInputTestResponseAssert, afterCaseActionAndAssert
import requests

from autoUtils.assertFactory import commonResponseAssert
from autoUtils.requestFactory import test_api_request, test_api_basic_auth_request
from autoUtils.ymlLib import ReadFile
# from autoUtils.optionUtil import searchAndChangeDict, ifItemInKeysAndValueNotNone
# from autoUtils.manage_global_data import ManageGlobalData

basedir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))))
fileName = basedir + '\\apiTestData\\global\\platform\\globalApi\\' + os.path.basename(__file__).split('.')[0] + '.yml'
readfile = ReadFile(fileName)
cases, parameters = readfile.get_businessTests_data()

cases_api_key, parameters_api_key = readfile.get_businessTests_data()
cases_oauth_token, parameters_oauth_token = readfile.get_businessTests_data()
for i in range(len(cases_api_key)):
    cases_api_key[i] = cases_api_key[i]+'[api_key]'
for i in range(len(cases_oauth_token)):
    cases_oauth_token[i] = cases_oauth_token[i] + '[oauth_token]'

class TestCurrentAgent:
    # request_url, request_type, request_header, request_body
    @pytest.mark.globalapi
    @pytest.mark.mila
    @pytest.mark.smoke
    @pytest.mark.parametrize('case, http, expect', list(parameters), ids=cases)
    def test_currentagent(self, case, http, expect, login):
        login_info = login
        env_dash = login_info['dashUrl']
        get_response = test_api_request(env_dash + http['path'], http['method'],login_info['commonHeader'], None)
        commonResponseAssert(get_response, expect)

    @pytest.mark.parametrize('case, http, expect', list(parameters_api_key), ids=cases_api_key)
    @pytest.mark.globalapi
    @pytest.mark.mila
    @pytest.mark.smoke
    def test_currentagent_api_key(self, case, http, expect, login):
        login_info = login
        env_dash = login_info['dashUrl']
        get_response = test_api_basic_auth_request(env_dash + http['path'], http['method'], None)
        commonResponseAssert(get_response, expect)

    @pytest.mark.parametrize('case, http, expect', list(parameters_oauth_token), ids=cases_oauth_token)
    @pytest.mark.globalapi
    @pytest.mark.mila
    @pytest.mark.smoke
    def test_currentagent_oauth_token(self, case, http, expect, login):
        login_info = login
        env_dash = login_info['dashUrl']
        get_response = test_api_request(env_dash + http['path'], http['method'], login_info['commonHeader'], None)
        commonResponseAssert(get_response, expect)

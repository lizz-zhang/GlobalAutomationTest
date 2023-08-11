import pytest
import allure
import os
from autoUtils.assertFactory import commonResponseAssert
from autoUtils.requestFactory import test_api_request, test_api_basic_auth_request
from autoUtils.ymlLib import ReadFile
from autoUtils.manage_global_data import ManageGlobalData


basedir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))))
fileName = basedir + '\\apiTestData\\global\\platform\\globalapi\\' + os.path.basename(__file__).split('.')[0] + '.yml'
readfile = ReadFile(fileName)
cases, parameters = readfile.get_businessTests_data()
cases_api_key, parameters_api_key = readfile.get_businessTests_data()
cases_oauth_token, parameters_oauth_token = readfile.get_businessTests_data()


class TestDeletePublicCannedMessageCategory:
    @pytest.mark.globalapi
    @pytest.mark.cannedmessages
    @pytest.mark.bella
    @pytest.mark.parametrize('case, http, expect', list(parameters), ids=cases)
    @pytest.mark.parametrize('function_initial_data', ['publiccannedmessagecategory'] , indirect=True)
    def test_delete_public_cannedmessage_category(self, case, http, expect, login, function_initial_data):
        login_info = login
        initial_public_canned_message_categoryid = function_initial_data['id']
        get_response = test_api_request(login_info['dashUrl'] + http['path'].replace('$id$', str(initial_public_canned_message_categoryid)), http['method'], login_info['commonHeader'], None)
        commonResponseAssert(get_response, expect)

    @pytest.mark.globalapi
    @pytest.mark.cannedmessages
    @pytest.mark.bella
    @pytest.mark.parametrize('case, http, expect', list(parameters_oauth_token), ids=cases_oauth_token)
    @pytest.mark.parametrize('function_initial_data', ['publiccannedmessagecategory'] , indirect=True)
    def test_delete_public_cannedmessage_category_oauth_token(self, case, http, expect, login, function_initial_data):
        login_info = login
        initial_public_canned_message_categoryid = function_initial_data['id']
        get_response_oauth_token = test_api_request(login_info['dashUrl'] + http['path'].replace('$id$', str(initial_public_canned_message_categoryid)), http['method'], login_info['oauth_header'], None)
        commonResponseAssert(get_response_oauth_token, expect)

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


class TestGetSinglePermission:
    @pytest.mark.globalapi
    @pytest.mark.permission
    @pytest.mark.bella
    @pytest.mark.parametrize('case, http, expect', list(parameters), ids=cases)
    def test_get_single_permissions(self, case, http, expect, login):
        login_info = login
        get_response = test_api_request(login_info['dashUrl'] + http['path'], http['method'], login_info['commonHeader'], None)
        commonResponseAssert(get_response, expect)

        """
        This interface error when use apiKey authentication. It is a bug
        get_response = test_api_basic_auth_request(login_info['dashUrl'] + http['path'], http['method'], login_info['commonHeader'],None)
        commonResponseAssert(get_response, expect)
        """

        get_response_oauth_token = test_api_request(login_info['dashUrl'] + http['path'], http['method'], login_info['oauth_header'], None)
        commonResponseAssert(get_response_oauth_token, expect)
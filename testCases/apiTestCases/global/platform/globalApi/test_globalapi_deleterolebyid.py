import pytest
import allure
import os
from autoUtils.assertFactory import commonResponseAssert
from autoUtils.requestFactory import test_api_request, test_api_basic_auth_request
from autoUtils.ymlLib import ReadFile
from autoUtils.manage_global_data import ManageGlobalData
import logging

logger = logging.getLogger(__name__)
basedir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))))
fileName = basedir + '\\apiTestData\\global\\platform\\globalApi\\' + os.path.basename(__file__).split('.')[0] + '.yml'
readfile = ReadFile(fileName)
cases, parameters = readfile.get_businessTests_data()
cases_api_key, parameters_api_key = readfile.get_businessTests_data()
cases_oauth_token, parameters_oauth_token = readfile.get_businessTests_data()
for i in range(len(cases_api_key)):
    cases_api_key[i] = cases_api_key[i] + '[api_key]'
for i in range(len(cases_oauth_token)):
    cases_oauth_token[i] = cases_oauth_token[i] + '[oauth_token]'


@allure.feature('delete a role by id')
class TestDeleteRoleById:
    @pytest.mark.parametrize('case, http, expect', list(parameters), ids=cases)
    @pytest.mark.parametrize('function_initial_data', ['roles'], indirect=True)
    @pytest.mark.globaltest
    @pytest.mark.oden
    @pytest.mark.smoke
    @pytest.mark.globalapi
    def test_delete_role_by_id(self, case, http, expect, login, function_initial_data):
        login_info = login
        initial_role = function_initial_data
        site_id = ManageGlobalData().get_site_id()
        get_response = test_api_request(login_info['dashUrl'] + http['path'].replace('$id$', initial_role['id']).replace('$siteId$', str(site_id)), http['method'], login_info['commonHeader'],
                                        None)

        commonResponseAssert(get_response, expect)

    @pytest.mark.parametrize('case, http, expect', list(parameters_api_key), ids=cases_api_key)
    @pytest.mark.parametrize('function_initial_data', ['roles'], indirect=True)
    @pytest.mark.globaltest
    @pytest.mark.oden
    @pytest.mark.smoke
    @pytest.mark.globalapi
    def test_delete_role_by_id_apikey(self, case, http, expect, login, function_initial_data):
        login_info = login
        initial_role = function_initial_data
        site_id = ManageGlobalData().get_site_id()
        get_response = test_api_basic_auth_request(login_info['dashUrl'] + http['path'].replace('$id$', initial_role['id']).replace('$siteId$', str(site_id)), http['method'],
                                        None)

        commonResponseAssert(get_response, expect)

    @pytest.mark.parametrize('case, http, expect', list(parameters_oauth_token), ids=cases_oauth_token)
    @pytest.mark.parametrize('function_initial_data', ['roles'], indirect=True)
    @pytest.mark.globaltest
    @pytest.mark.oden
    @pytest.mark.smoke
    @pytest.mark.globalapi
    def test_delete_role_by_id_oauth_token(self, case, http, expect, login, function_initial_data):
        login_info = login
        initial_role = function_initial_data
        site_id = ManageGlobalData().get_site_id()
        get_response = test_api_request(login_info['dashUrl'] + http['path'].replace('$id$', initial_role['id']).replace('$siteId$', str(site_id)), http['method'], login_info['oauth_header'],
                                        None)

        commonResponseAssert(get_response, expect)
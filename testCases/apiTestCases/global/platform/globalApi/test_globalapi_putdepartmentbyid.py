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
fileName = basedir + '\\apiTestData\\global\\platform\\globalapi\\' + os.path.basename(__file__).split('.')[0] + '.yml'
readfile = ReadFile(fileName)
cases, parameters = readfile.get_businessTests_data()
cases_api_key, parameters_api_key = readfile.get_businessTests_data()
cases_oauth_token, parameters_oauth_token = readfile.get_businessTests_data()
for i in range(len(cases_api_key)):
    cases_api_key[i] = cases_api_key[i]+'[api_key]'
for i in range(len(cases_oauth_token)):
    cases_oauth_token[i] = cases_oauth_token[i] + '[oauth_token]'



@allure.feature('put a department by id')
class TestPutDepartmentById:
    @pytest.mark.parametrize('case, http, expect', list(parameters), ids=cases)
    @pytest.mark.globalapi
    @pytest.mark.mila
    @pytest.mark.smoke
    def test_put_department_by_id(self, case, http, expect, login, create_and_delete_department):
        login_info = login
        initial_department = create_and_delete_department
        site_id = ManageGlobalData().get_site_id()
        get_response = test_api_request(login_info['dashUrl'] + http['path'].replace('$id$', initial_department['id']).replace('$siteId$', str(site_id)), http['method'], login_info['commonHeader'],
                                        http['body'])
        commonResponseAssert(get_response, expect)

    @pytest.mark.parametrize('case, http, expect', list(parameters_api_key), ids=cases_api_key)
    @pytest.mark.globalapi
    @pytest.mark.mila
    @pytest.mark.smoke
    def test_put_department_by_id_api_key(self, case, http, expect, login, create_and_delete_department):
        login_info = login
        initial_department = create_and_delete_department
        site_id = ManageGlobalData().get_site_id()
        get_response = test_api_basic_auth_request(
            login_info['dashUrl'] + http['path'].replace('$id$', initial_department['id']).replace('$siteId$',str(site_id)),http['method'], http['body'])
        commonResponseAssert(get_response, expect)

    @pytest.mark.parametrize('case, http, expect', list(parameters_oauth_token), ids=cases_oauth_token)
    @pytest.mark.globalapi
    @pytest.mark.mila
    @pytest.mark.smoke
    def test_put_department_by_id_oauth_token(self, case, http, expect, login, create_and_delete_department):
        login_info = login
        initial_department = create_and_delete_department
        site_id = ManageGlobalData().get_site_id()
        get_response = test_api_request(login_info['dashUrl'] + http['path'].replace('$id$', initial_department['id']).replace('$siteId$', str(site_id)), http['method'], login_info['oauth_header'],
                                        http['body'])
        commonResponseAssert(get_response, expect)

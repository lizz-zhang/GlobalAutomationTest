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
cases_oauth_token, parameters_oauth_token = readfile.get_businessTests_data()


class TestPutRolePermissions:
    @pytest.mark.globalapi
    @pytest.mark.permission
    @pytest.mark.bella
    @pytest.mark.parametrize('case, http, expect', list(parameters), ids=cases)
    @pytest.mark.parametrize('initial_data', ['roles'] , indirect=True)
    def test_put_role_permissions(self, case, http, expect, login, initial_data):
        login_info = login
        initial_role_id = initial_data['id']
        get_response = test_api_request(login_info['dashUrl'] + http['path'].replace('$roleId$', str(initial_role_id)), http['method'], login_info['commonHeader'], http['body'])
        commonResponseAssert(get_response, expect)



    @pytest.mark.globalapi
    @pytest.mark.permission
    @pytest.mark.bella
    @pytest.mark.parametrize('case, http, expect', list(parameters_oauth_token), ids=cases_oauth_token)
    @pytest.mark.parametrize('initial_data', ['roles'] , indirect=True)
    def test_put_role_permissions_oauth_token(self, case, http, expect, login, initial_data):
        login_info = login
        initial_role_id = initial_data['id']
        get_response = test_api_request(login_info['dashUrl'] + http['path'].replace('$roleId$', str(initial_role_id)),http['method'], login_info['commonHeader'], http['body'])
        commonResponseAssert(get_response, expect)



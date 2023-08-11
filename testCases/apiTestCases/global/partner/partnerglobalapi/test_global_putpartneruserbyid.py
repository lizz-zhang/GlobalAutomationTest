import pytest
import allure
import os
from autoUtils.assertFactory import commonResponseAssert
from autoUtils.requestFactory import test_api_request
from autoUtils.ymlLib import ReadFile
from autoUtils.fileReader import read_config_file
from autoUtils.optionUtil import change_to_random_string, replace_dict_value,ifItemInKeysAndValueNotNone
import json



basedir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))))
fileName = basedir + '\\apiTestData\\global\\partner\\partnerglobalapi\\' + os.path.basename(__file__).split('.')[0] + '.yml'
readfile = ReadFile(fileName)
cases, parameters = readfile.get_businessTests_data()
cases_oauth_token, parameters_oauth_token = readfile.get_businessTests_data()
illegal_cases, illegal_parameters = readfile.get_illegalInputTests_data()

for i in range(len(cases_oauth_token)):
    cases_oauth_token[i] = cases_oauth_token[i] + '[oauth_token]'

@allure.feature('put partner user by id')
class TestPutPartnerUserById:
    @pytest.mark.parametrize('case, http, expect', list(parameters), ids=cases)
    @pytest.mark.parametrize('initial_data', ['partnreagents'], indirect=True)
    @pytest.mark.globaltest
    @pytest.mark.oden
    @pytest.mark.smoke
    @pytest.mark.partnerglobalapi
    def test_put_partner_user_by_id(self, case, http, expect, partnerLogin, initial_data):
        login_info = partnerLogin
        initial_user = initial_data
        http['body'] = change_to_random_string(http['body'])
        if ifItemInKeysAndValueNotNone('email', expect['responseitemcheck']):
            expect['responseitemcheck']['email'] = http['body']['email']

        config_data_json_dict = read_config_file('global_test_data.json')
        role_path = login_info['partnerUrl'] + config_data_json_dict['partnreagents']['getAdminRoleIdPath']
        role_method = config_data_json_dict['partnreagents']['getAdminRoleIdMethod']
        get_role_response = test_api_request(role_path, role_method, login_info['partnerCommonHeader'], None)
        admin_role_id = json.loads(get_role_response.content)[0]['id']
        http['body'] = replace_dict_value(http['body'], '$role_id$', admin_role_id)

        get_response = test_api_request(login_info['partnerUrl'] + http['path'].replace('$id$', str(initial_user['id'])), http['method'], login_info['partnerCommonHeader'],
                                        http['body'])
        commonResponseAssert(get_response, expect)


    @pytest.mark.parametrize('case, http, expect', list(parameters_oauth_token), ids=cases_oauth_token)
    @pytest.mark.parametrize('initial_data', ['partnreagents'], indirect=True)
    @pytest.mark.globaltest
    @pytest.mark.oden
    @pytest.mark.smoke
    @pytest.mark.partnerglobalapi
    def test_put_partner_user_by_id_auth_token(self, case, http, expect, partnerLogin, initial_data):
        login_info = partnerLogin
        initial_user = initial_data
        http['body'] = change_to_random_string(http['body'])
        if ifItemInKeysAndValueNotNone('email', expect['responseitemcheck']):
            expect['responseitemcheck']['email'] = http['body']['email']

        config_data_json_dict = read_config_file('global_test_data.json')
        role_path = login_info['partnerUrl'] + config_data_json_dict['partnreagents']['getAdminRoleIdPath']
        role_method = config_data_json_dict['partnreagents']['getAdminRoleIdMethod']
        get_role_response = test_api_request(role_path, role_method, login_info['partnerCommonHeader'], None)
        admin_role_id = json.loads(get_role_response.content)[0]['id']
        http['body'] = replace_dict_value(http['body'], '$role_id$', admin_role_id)

        get_response = test_api_request(login_info['partnerUrl'] + http['path'].replace('$id$', str(initial_user['id'])), http['method'], login_info['partner_oauth_header'],
                                        http['body'])
        commonResponseAssert(get_response, expect)


    @pytest.mark.parametrize('case, http, expect', list(illegal_parameters), ids=illegal_cases)
    @pytest.mark.parametrize('initial_data', ['partnreagents'], indirect=True)
    @pytest.mark.globaltest
    @pytest.mark.oden
    @pytest.mark.smoke
    def test_put_partner_user_by_id_illegal(self, case, http, expect, partnerLogin, initial_data):
        login_info = partnerLogin
        initial_user = initial_data
        http['body'] = change_to_random_string(http['body'])
        if ifItemInKeysAndValueNotNone('email', expect['responseitemcheck']):
            expect['responseitemcheck']['email'] = http['body']['email']

        config_data_json_dict = read_config_file('global_test_data.json')
        role_path = login_info['partnerUrl'] + config_data_json_dict['partnreagents']['getAdminRoleIdPath']
        role_method = config_data_json_dict['partnreagents']['getAdminRoleIdMethod']
        get_role_response = test_api_request(role_path, role_method, login_info['partnerCommonHeader'], None)
        admin_role_id = json.loads(get_role_response.content)[0]['id']
        http['body'] = replace_dict_value(http['body'], '$role_id$', admin_role_id)

        get_response = test_api_request(login_info['partnerUrl'] + http['path'].replace('$id$', str(initial_user['id'])), http['method'], login_info['partnerCommonHeader'],
                                        http['body'])
        commonResponseAssert(get_response, expect)
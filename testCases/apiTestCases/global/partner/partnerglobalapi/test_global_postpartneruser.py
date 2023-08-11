import pytest
import allure
import os
from autoUtils.assertFactory import commonResponseAssert, afterCaseActionAndAssert
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


for i in range(len(cases_oauth_token)):
    cases_oauth_token[i] = cases_oauth_token[i] + '[oauth_token]'

@allure.feature('post partner user ')
class TestPostPartnerUser:
    @pytest.mark.parametrize('case, http, expect', list(parameters), ids=cases)
    @pytest.mark.globaltest
    @pytest.mark.oden
    @pytest.mark.smoke
    @pytest.mark.partnerglobalapi
    def test_post_partner_user(self, case, http, expect, partnerLogin):
        login_info = partnerLogin
        http['body'] = change_to_random_string(http['body'])
        if ifItemInKeysAndValueNotNone('confirmEmail', http['body']):
            http['body']['confirmEmail'] = http['body']['email']

        config_data_json_dict = read_config_file('global_test_data.json')
        role_path = login_info['partnerUrl'] + config_data_json_dict['partnreagents']['getAdminRoleIdPath']
        role_method = config_data_json_dict['partnreagents']['getAdminRoleIdMethod']
        get_role_response = test_api_request(role_path, role_method, login_info['partnerCommonHeader'], None)
        admin_role_id = json.loads(get_role_response.content)[0]['id']
        http['body'] = replace_dict_value(http['body'], '$role_id$', admin_role_id)

        get_response = test_api_request(login_info['partnerUrl'] + http['path'], http['method'], login_info['partnerCommonHeader'],
                                        http['body'])
        commonResponseAssert(get_response, expect)
        afterCaseActionAndAssert(login_info['partnerUrl'], login_info['partnerCommonHeader'], get_response, expect)


    @pytest.mark.parametrize('case, http, expect', list(parameters_oauth_token), ids=cases_oauth_token)
    @pytest.mark.globaltest
    @pytest.mark.oden
    @pytest.mark.smoke
    @pytest.mark.partnerglobalapi
    def test_post_partner_user_auth_token(self, case, http, expect, partnerLogin):
        login_info = partnerLogin
        http['body'] = change_to_random_string(http['body'])
        if ifItemInKeysAndValueNotNone('confirmEmail', http['body']):
            http['body']['confirmEmail'] = http['body']['email']

        config_data_json_dict = read_config_file('global_test_data.json')
        role_path = login_info['partnerUrl'] + config_data_json_dict['partnreagents']['getAdminRoleIdPath']
        role_method = config_data_json_dict['partnreagents']['getAdminRoleIdMethod']
        get_role_response = test_api_request(role_path, role_method, login_info['partnerCommonHeader'], None)
        admin_role_id = json.loads(get_role_response.content)[0]['id']
        http['body'] = replace_dict_value(http['body'], '$role_id$', admin_role_id)

        get_response = test_api_request(login_info['partnerUrl'] + http['path'], http['method'], login_info['partner_oauth_header'],
                                        http['body'])
        commonResponseAssert(get_response, expect)
        afterCaseActionAndAssert(login_info['partnerUrl'], login_info['partner_oauth_header'], get_response, expect)
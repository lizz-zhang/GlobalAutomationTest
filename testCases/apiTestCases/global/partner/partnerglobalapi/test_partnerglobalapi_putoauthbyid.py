import pytest
import allure
import os
from autoUtils.assertFactory import commonResponseAssert
from autoUtils.manage_global_data import ManageGlobalData
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

@allure.feature('put partner oauth by id')
class TestPutPartnerOauthById:
    @pytest.mark.parametrize('case, http, expect', list(parameters), ids=cases)
    @pytest.mark.partnerglobalapi
    @pytest.mark.mila
    @pytest.mark.smoke
    def test_put_partner_oauth_by_id(self, case, http, expect, partnerLogin, create_and_delete_partner_oauth):
        login_info = partnerLogin
        initial_oauth_partner = create_and_delete_partner_oauth
        partner_id = ManageGlobalData().get_partner_id()
        get_response = test_api_request(login_info['partnerUrl'] + http['path'].replace('$id$', initial_oauth_partner['id']).replace('$partnerId$', str(partner_id)), http['method'], login_info['partnerCommonHeader'], http['body'])
        commonResponseAssert(get_response, expect)


    @pytest.mark.parametrize('case, http, expect', list(parameters_oauth_token), ids=cases_oauth_token)
    @pytest.mark.partnerglobalapi
    @pytest.mark.mila
    @pytest.mark.smoke
    def test_put_partner_user_by_id_auth_token(self, case, http, expect, partnerLogin, create_and_delete_partner_oauth):
        login_info = partnerLogin
        initial_oauth_partner = create_and_delete_partner_oauth
        partner_id = ManageGlobalData().get_partner_id()
        get_response = test_api_request(login_info['partnerUrl'] + http['path'].replace('$id$', initial_oauth_partner['id']).replace('$partnerId$',str(partner_id)),http['method'], login_info['partner_oauth_header'], http['body'])
        commonResponseAssert(get_response, expect)

    @pytest.mark.parametrize('case, http, expect', list(illegal_parameters), ids=illegal_cases)
    @pytest.mark.partnerglobalapi
    @pytest.mark.mila
    @pytest.mark.smoke
    def test_put_partner_oauth_by_id_illegal(self, case, http, expect, partnerLogin, create_and_delete_partner_oauth):
        login_info = partnerLogin
        initial_oauth_partner = create_and_delete_partner_oauth
        partner_id = ManageGlobalData().get_partner_id()
        get_response = test_api_request(
            login_info['partnerUrl'] + http['path'].replace('$id$', initial_oauth_partner['id']).replace('$partnerId$', str(partner_id)), http['method'], login_info['partnerCommonHeader'], http['body'])
        commonResponseAssert(get_response, expect)

import pdb

import pytest
import allure
import os
from autoUtils.assertFactory import commonResponseAssert, afterCaseActionAndAssert
from autoUtils.manage_global_data import ManageGlobalData
from autoUtils.requestFactory import test_api_request
from autoUtils.ymlLib import ReadFile
from autoUtils.fileReader import read_config_file
from autoUtils.optionUtil import change_to_random_string, replace_dict_value,ifItemInKeysAndValueNotNone
import json



basedir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))))
fileName = basedir + '\\apiTestData\\global\\partner\\childpartnerapi\\' + os.path.basename(__file__).split('.')[0] + '.yml'
readfile = ReadFile(fileName)
cases, parameters = readfile.get_businessTests_data()
cases_oauth_token, parameters_oauth_token = readfile.get_businessTests_data()


for i in range(len(cases_oauth_token)):
    cases_oauth_token[i] = cases_oauth_token[i] + '[oauth_token]'

@allure.feature('post child partner ')
class TestPostChildPartner:
    @pytest.mark.parametrize('case, http, expect', list(parameters), ids=cases)
    @pytest.mark.childpartnerapi
    @pytest.mark.mila
    @pytest.mark.smoke
    def test_post_childpartner(self, case, http, expect, partnerLogin):
        login_info = partnerLogin
        partner_id = ManageGlobalData().get_partner_id()
        body = change_to_random_string(http['body'])
        # pdb.set_trace()
        body['partnerUsers'][0]['confirmEmail'] = str(body['partnerUsers'][0]['email'])
        get_response = test_api_request(login_info['partnerUrl'] + http['path'].replace('$partnerId$', str(partner_id)),http['method'], login_info['partnerCommonHeader'], body)

        commonResponseAssert(get_response, expect)
        afterCaseActionAndAssert(login_info['partnerUrl'], login_info['partnerCommonHeader'], get_response, expect)

    @pytest.mark.parametrize('case, http, expect', list(parameters_oauth_token), ids=cases_oauth_token)
    @pytest.mark.childpartnerapi
    @pytest.mark.mila
    @pytest.mark.smoke
    def test_post_childpartner_oauth_token(self, case, http, expect, partnerLogin):
        login_info = partnerLogin
        partner_id = ManageGlobalData().get_partner_id()
        body = change_to_random_string(http['body'])
        # pdb.set_trace()
        body['partnerUsers'][0]['confirmEmail'] = str(body['partnerUsers'][0]['email'])
        get_response = test_api_request(login_info['partnerUrl'] + http['path'].replace('$partnerId$', str(partner_id)), http['method'], login_info['partner_oauth_header'], body)

        commonResponseAssert(get_response, expect)
        afterCaseActionAndAssert(login_info['partnerUrl'], login_info['partner_oauth_header'], get_response, expect)

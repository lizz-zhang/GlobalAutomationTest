import logging

import pytest
import allure
import os
from autoUtils.assertFactory import commonResponseAssert
from autoUtils.requestFactory import test_api_request
from autoUtils.ymlLib import ReadFile
from autoUtils.manage_global_data import ManageGlobalData
import pdb


basedir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))))
fileName = basedir + '\\apiTestData\\global\\partner\\partnerglobalapi\\' + os.path.basename(__file__).split('.')[0] + '.yml'
readfile = ReadFile(fileName)
cases, parameters = readfile.get_businessTests_data()
cases_oauth_token, parameters_oauth_token = readfile.get_businessTests_data()

for i in range(len(cases_oauth_token)):
    cases_oauth_token[i] = cases_oauth_token[i] + '[oauth_token]'

@allure.feature('get partner oauth')
class TestGetPartnerOauth:
    @pytest.mark.parametrize('case, http, expect', list(parameters), ids=cases)
    @pytest.mark.partnerglobalapi
    @pytest.mark.mila
    @pytest.mark.smoke
    def test_get_partner_oauth(self, case, http, expect, partnerLogin, create_and_delete_partner_oauth):
        login_info = partnerLogin
        partner_id = ManageGlobalData().get_partner_id()
        get_response = test_api_request(login_info['partnerUrl'] + http['path'].replace('$partnerId$', str(partner_id)), http['method'], login_info['partnerCommonHeader'],
                                        None)
        commonResponseAssert(get_response, expect)


    @pytest.mark.parametrize('case, http, expect', list(parameters_oauth_token), ids=cases_oauth_token)
    @pytest.mark.partnerglobalapi
    @pytest.mark.mila
    @pytest.mark.smoke
    def test_get_partner_oauth_oauth_token(self, case, http, expect, partnerLogin, create_and_delete_partner_oauth):
        login_info = partnerLogin
        partner_id = ManageGlobalData().get_partner_id()
        get_response = test_api_request(login_info['partnerUrl'] + http['path'].replace('$partnerId$', str(partner_id)), http['method'], login_info['partner_oauth_header'],
                                        None)
        commonResponseAssert(get_response, expect)

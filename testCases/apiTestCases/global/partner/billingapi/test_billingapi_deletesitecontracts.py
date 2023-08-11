import pytest
import allure
import os
from autoUtils.assertFactory import commonResponseAssert
from autoUtils.requestFactory import test_api_request, test_api_basic_auth_request
from autoUtils.ymlLib import ReadFile
from autoUtils.manage_global_data import ManageGlobalData
from autoUtils.optionUtil import ifItemInKeysAndValueNotNone



basedir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))))
fileName = basedir + '\\apiTestData\\global\\partner\\billingapi\\' + os.path.basename(__file__).split('.')[0] + '.yml'
readfile = ReadFile(fileName)
cases, parameters = readfile.get_businessTests_data()
cases_oauth_token, parameters_oauth_token = readfile.get_businessTests_data()


class TestDeleteSiteContractById:
    @pytest.mark.billingapi
    @pytest.mark.sitecontract
    @pytest.mark.bella
    @pytest.mark.parametrize('case, http, expect', list(parameters), ids=cases)
    def test_delete_sitecontractbyid(self, case, http, expect, partnerLogin,every_function_create_and_delete_site_contract):
        partnerLogin_info = partnerLogin
        initial_contract_id = every_function_create_and_delete_site_contract['id']
        get_response = test_api_request(partnerLogin_info['partnerUrl'] + http['path'].replace('$id$', str(initial_contract_id)), http['method'], partnerLogin_info['partnerCommonHeader'], None)
        commonResponseAssert(get_response, expect)

    @pytest.mark.billingapi
    @pytest.mark.sitecontract
    @pytest.mark.bella
    @pytest.mark.parametrize('case, http, expect', list(parameters_oauth_token), ids=cases_oauth_token)
    def test_delete_sitecontractbyid_oauth_token(self, case, http, expect, partnerLogin, every_function_create_and_delete_site_contract):
        partnerLogin_info = partnerLogin
        initial_contract_id = every_function_create_and_delete_site_contract['id']
        get_response = test_api_request(partnerLogin_info['partnerUrl'] + http['path'].replace('$id$', str(initial_contract_id)), http['method'], partnerLogin_info['partnerCommonHeader'], None)
        commonResponseAssert(get_response, expect)

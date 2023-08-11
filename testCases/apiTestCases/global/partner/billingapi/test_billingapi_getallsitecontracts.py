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


class TestGetAllSiteContracts:
    @pytest.mark.billingapi
    @pytest.mark.sitecontract
    @pytest.mark.parametrize('case, http, expect', list(parameters), ids=cases)
    def test_get_allsitecontracts(self, case, http, expect, partnerLogin):
        partnerLogin_info = partnerLogin
        get_response = test_api_request(partnerLogin_info['partnerUrl'] + http['path'], http['method'], partnerLogin_info['partnerCommonHeader'], None)
        commonResponseAssert(get_response, expect)
        get_response_oauth_token = test_api_request(partnerLogin_info['partnerUrl'] + http['path'], http['method'], partnerLogin_info['partner_oauth_header'], None)
        commonResponseAssert(get_response_oauth_token, expect)
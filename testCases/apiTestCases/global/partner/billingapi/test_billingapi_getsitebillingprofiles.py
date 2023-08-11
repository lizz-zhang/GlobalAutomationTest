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


class TestGetSiteBillingProfile:
    @pytest.mark.billingapi
    @pytest.mark.billingprofile
    @pytest.mark.bella
    @pytest.mark.parametrize('case, http, expect', list(parameters), ids=cases)
    def test_get_sitebillingprofile_by_siteid(self, case, http, expect, partnerLogin):
        partnerLogin_info = partnerLogin
        trial_site_id = ManageGlobalData().get_partner_trialsiteid()
        paid_site_id = ManageGlobalData().get_partner_paidsiteid()
        if case == 'Get Site BillingProfile Failed. Because the Site Billing Profile does not Exist':
            get_response = test_api_request(partnerLogin_info['partnerUrl'] + http['path'].replace('$siteId$', str(trial_site_id)), http['method'], partnerLogin_info['partnerCommonHeader'], None)
            get_response_oauth_token = test_api_request(partnerLogin_info['partnerUrl'] + http['path'].replace('$siteId$', str(trial_site_id)), http['method'],partnerLogin_info['partner_oauth_header'], None)
        else:
            get_response = test_api_request(partnerLogin_info['partnerUrl'] + http['path'].replace('$siteId$', str(paid_site_id)), http['method'],partnerLogin_info['partnerCommonHeader'], None)
            get_response_oauth_token = test_api_request(partnerLogin_info['partnerUrl'] + http['path'].replace('$siteId$', str(paid_site_id)), http['method'],partnerLogin_info['partner_oauth_header'], None)
        if ifItemInKeysAndValueNotNone('siteId', expect['responseitemcheck']):
            expect['responseitemcheck']['siteId'] = paid_site_id
        commonResponseAssert(get_response, expect)
        commonResponseAssert(get_response_oauth_token, expect)



import pytest
import allure
import os
from autoUtils.assertFactory import commonResponseAssert, afterCaseActionAndAssert
from autoUtils.requestFactory import test_api_request, test_api_basic_auth_request
from autoUtils.ymlLib import ReadFile
from autoUtils.manage_global_data import ManageGlobalData
from autoUtils.optionUtil import ifItemInKeysAndValueNotNone



basedir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))))
fileName = basedir + '\\apiTestData\\global\\partner\\billingapi\\' + os.path.basename(__file__).split('.')[0] + '.yml'
readfile = ReadFile(fileName)
cases, parameters = readfile.get_businessTests_data()
cases_oauth_token, parameters_oauth_token = readfile.get_businessTests_data()



class TestPostSiteBillingPeriod:
    @pytest.mark.billingapi
    @pytest.mark.billingperiod
    @pytest.mark.bella
    @pytest.mark.parametrize('case, http, expect', list(parameters), ids=cases)
    def test_update_sitebillingperiod(self, case, http, expect, partnerLogin):
        partnerLogin_info = partnerLogin
        trial_site_id = ManageGlobalData().get_partner_trialsiteid()
        paid_site_id = ManageGlobalData().get_partner_paidsiteid()
        if case == 'Post Change BillingPeriod Failed. Because the Site is not Trial Status':
            if http['body']['siteId'] == '$siteId$':
                http['body']['siteId'] = paid_site_id
        else:
            if http['body']['siteId'] == '$siteId$':
                http['body']['siteId'] = trial_site_id
        get_response = test_api_request(partnerLogin_info['partnerUrl'] + http['path'], http['method'], partnerLogin_info['partnerCommonHeader'], http['body'])
        commonResponseAssert(get_response, expect)

        if ifItemInKeysAndValueNotNone('aftercaseaction', expect):
            if expect['aftercasebody']['siteId'] == '$siteId$':
                expect['aftercasebody']['siteId'] = trial_site_id
            afterCaseActionAndAssert(partnerLogin_info['partnerUrl'], partnerLogin_info['partnerCommonHeader'], get_response, expect)

    @pytest.mark.billingapi
    @pytest.mark.billingperiod
    @pytest.mark.bella
    @pytest.mark.parametrize('case, http, expect', list(parameters_oauth_token), ids=cases_oauth_token)
    def test_update_sitebillingperiod_oauth_token(self, case, http, expect, partnerLogin):
        partnerLogin_info = partnerLogin
        trial_site_id = ManageGlobalData().get_partner_trialsiteid()
        paid_site_id = ManageGlobalData().get_partner_paidsiteid()
        if case == 'Post Change BillingPeriod Failed. Because the Site is not Trial Status':
            if http['body']['siteId'] == '$siteId$':
                http['body']['siteId'] = paid_site_id
        else:
            if http['body']['siteId'] == '$siteId$':
                http['body']['siteId'] = trial_site_id
        get_response = test_api_request(partnerLogin_info['partnerUrl'] + http['path'], http['method'], partnerLogin_info['partner_oauth_header'], http['body'])
        commonResponseAssert(get_response, expect)

        if ifItemInKeysAndValueNotNone('aftercaseaction', expect):
            if expect['aftercasebody']['siteId'] == '$siteId$':
                expect['aftercasebody']['siteId'] = trial_site_id
            afterCaseActionAndAssert(partnerLogin_info['partnerUrl'], partnerLogin_info['partner_oauth_header'], get_response, expect)

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
illegal_cases, illegal_parameters = readfile.get_illegalInputTests_data()


class TestUpdateSiteBillingProfile:
    @pytest.mark.billingapi
    @pytest.mark.billingprofile
    @pytest.mark.bella
    @pytest.mark.parametrize('case, http, expect', list(parameters), ids=cases)
    def test_update_sitebillingprofile_by_siteid(self, case, http, expect, partnerLogin):
        partnerLogin_info = partnerLogin
        site_id = ManageGlobalData().get_partner_paidsiteid()
        http['path'] = http['path'].replace('$siteId$', str(site_id))
        get_response = test_api_request(partnerLogin_info['partnerUrl'] + http['path'], http['method'], partnerLogin_info['partnerCommonHeader'], http['body'])
        if ifItemInKeysAndValueNotNone('siteId', expect['responseitemcheck']):
            expect['responseitemcheck']['siteId'] = site_id
        commonResponseAssert(get_response, expect)

        if ifItemInKeysAndValueNotNone('aftercaseaction', expect):
            expect['aftercasepath'] = expect['aftercasepath'].replace('$siteId$', str(site_id))
            afterCaseActionAndAssert(partnerLogin_info['partnerUrl'], partnerLogin_info['partnerCommonHeader'], get_response, expect)


    @pytest.mark.billingapi
    @pytest.mark.billingprofile
    @pytest.mark.bella
    @pytest.mark.parametrize('case, http, expect', list(parameters_oauth_token), ids=cases_oauth_token)
    def test_update_sitebillingconfig_by_siteid_oauth_token(self, case, http, expect, partnerLogin):
        partnerLogin_info = partnerLogin
        site_id = ManageGlobalData().get_partner_paidsiteid()
        http['path'] = http['path'].replace('$siteId$', str(site_id))
        get_response = test_api_request(partnerLogin_info['partnerUrl'] + http['path'], http['method'], partnerLogin_info['partner_oauth_header'], http['body'])
        if ifItemInKeysAndValueNotNone('siteId', expect['responseitemcheck']):
            expect['responseitemcheck']['siteId'] = site_id
        commonResponseAssert(get_response, expect)

        if ifItemInKeysAndValueNotNone('aftercaseaction', expect):
            expect['aftercasepath'] = expect['aftercasepath'].replace('$siteId$', str(site_id))
            afterCaseActionAndAssert(partnerLogin_info['partnerUrl'], partnerLogin_info['partner_oauth_header'], get_response, expect)


    @pytest.mark.parametrize('case, http, expect', list(illegal_parameters), ids=illegal_cases)
    @pytest.mark.billingapi
    @pytest.mark.billingprofile
    @pytest.mark.bella
    def test_update_sitebillingconfig_by_siteid_illegal(self, case, http, expect, partnerLogin):
        partnerLogin_info = partnerLogin
        site_id = ManageGlobalData().get_partner_paidsiteid()
        http['path'] = http['path'].replace('$siteId$', str(site_id))
        get_response = test_api_request(partnerLogin_info['partnerUrl'] + http['path'], http['method'], partnerLogin_info['partnerCommonHeader'], http['body'])
        commonResponseAssert(get_response, expect)
        get_response_oauth_token = test_api_request(partnerLogin_info['partnerUrl'] + http['path'], http['method'], partnerLogin_info['partner_oauth_header'], http['body'])
        commonResponseAssert(get_response_oauth_token, expect)



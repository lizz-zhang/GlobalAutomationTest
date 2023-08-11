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

class TestUpdateSiteBillingConfig:
    @pytest.mark.billingapi
    @pytest.mark.billingconfig
    @pytest.mark.parametrize('case, http, expect', list(parameters), ids=cases)
    def test_update_sitebillingconfig_by_siteid(self, case, http, expect, partnerLogin):
        partnerLogin_info = partnerLogin
        site_id = ManageGlobalData().get_partner_paidsiteid()
        get_response = test_api_request(partnerLogin_info['partnerUrl'] + http['path'].replace('$siteId$', str(site_id)), http['method'], partnerLogin_info['partnerCommonHeader'], http['body'])
        if ifItemInKeysAndValueNotNone('siteId', expect['responseitemcheck']):
            expect['responseitemcheck']['siteId'] = site_id
        commonResponseAssert(get_response, expect)
        expect['aftercasepath'] = expect['aftercasepath'].replace('$siteId$', str(site_id))
        afterCaseActionAndAssert(partnerLogin_info['partnerUrl'], partnerLogin_info['partnerCommonHeader'], get_response, expect)


    @pytest.mark.billingapi
    @pytest.mark.billingconfig
    @pytest.mark.parametrize('case, http, expect', list(parameters_oauth_token), ids=cases_oauth_token,)
    def test_update_sitebillingconfig_by_siteid_oauth_token(self, case, http, expect, partnerLogin):
        partnerLogin_info = partnerLogin
        site_id = ManageGlobalData().get_partner_paidsiteid()
        get_response = test_api_request(partnerLogin_info['partnerUrl'] + http['path'].replace('$siteId$', str(site_id)), http['method'], partnerLogin_info['partner_oauth_header'], http['body'])
        if ifItemInKeysAndValueNotNone('siteId', expect['responseitemcheck']):
            expect['responseitemcheck']['siteId'] = site_id
        commonResponseAssert(get_response, expect)
        expect['aftercasepath'] = expect['aftercasepath'].replace('$siteId$', str(site_id))
        afterCaseActionAndAssert(partnerLogin_info['partnerUrl'], partnerLogin_info['partnerCommonHeader'], get_response, expect)






import pytest
import allure
import os
from autoUtils.assertFactory import commonResponseAssert, afterCaseActionAndAssert
from autoUtils.requestFactory import test_api_request, test_api_basic_auth_request
from autoUtils.ymlLib import ReadFile
from autoUtils.manage_global_data import ManageGlobalData
import logging
from autoUtils.optionUtil import ifItemInKeysAndValueNotNone


logger = logging.getLogger(__name__)

basedir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))))
fileName = basedir + '\\apiTestData\\global\\partner\\site\\' + os.path.basename(__file__).split('.')[0] + '.yml'
readfile = ReadFile(fileName)
cases, parameters = readfile.get_businessTests_data()
cases_oauth_token, parameters_oauth_token = readfile.get_businessTests_data()

for i in range(len(cases_oauth_token)):
    cases_oauth_token[i] = cases_oauth_token[i] + '[oauth_token]'


@allure.feature('switch site status')
class TestSwitchSite:
    @pytest.mark.parametrize('case, http, expect', list(parameters), ids=cases)
    @pytest.mark.globaltest
    @pytest.mark.oden
    @pytest.mark.smoke
    @pytest.mark.billingapi
    def test_switch_site(self, case, http, expect, partnerLogin):
        login_info = partnerLogin
        site_id = ManageGlobalData().get_site_id()
        partner_id = ManageGlobalData().get_partner_id()

        if '$siteId$' in http['body']['siteId']:
            http['body']['siteId'] = site_id
        get_response = test_api_request(login_info['partnerUrl'] + http['path'].replace('$partnerId$', str(partner_id)), http['method'], login_info['partnerCommonHeader'],
                                        http['body'])
        commonResponseAssert(get_response, expect)

        if ifItemInKeysAndValueNotNone('aftercaseaction', expect):
            expect['aftercasepath'] = expect['aftercasepath'].replace('$partnerId$', str(partner_id))
            if '$siteId$' in expect['aftercasebody']['siteId']:
                expect['aftercasebody']['siteId'] = site_id
            afterCaseActionAndAssert(login_info['partnerUrl'], login_info['partnerCommonHeader'], get_response, expect)

    @pytest.mark.parametrize('case, http, expect', list(parameters_oauth_token), ids=cases_oauth_token)
    @pytest.mark.globaltest
    @pytest.mark.oden
    @pytest.mark.smoke
    @pytest.mark.billingapi
    def test_switch_site_auto_token(self, case, http, expect, partnerLogin):
        login_info = partnerLogin
        site_id = ManageGlobalData().get_site_id()
        partner_id = ManageGlobalData().get_partner_id()

        if '$siteId$' in http['body']['siteId']:
            http['body']['siteId'] = site_id
        get_response = test_api_request(login_info['partnerUrl'] + http['path'].replace('$partnerId$', str(partner_id)), http['method'], login_info['partner_oauth_header'],
                                        http['body'])
        commonResponseAssert(get_response, expect)

        if ifItemInKeysAndValueNotNone('aftercaseaction', expect):
            expect['aftercasepath'] = expect['aftercasepath'].replace('$partnerId$', str(partner_id))
            if '$siteId$' in expect['aftercasebody']['siteId']:
                expect['aftercasebody']['siteId'] = site_id
            afterCaseActionAndAssert(login_info['partnerUrl'], login_info['partnerCommonHeader'], get_response, expect)
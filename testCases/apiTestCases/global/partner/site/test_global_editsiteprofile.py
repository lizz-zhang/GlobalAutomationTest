import pytest
import allure
import os
from autoUtils.assertFactory import commonResponseAssert
from autoUtils.requestFactory import test_api_request, test_api_basic_auth_request
from autoUtils.ymlLib import ReadFile
from autoUtils.manage_global_data import ManageGlobalData
from autoUtils.optionUtil import replace_dict_value
import logging



logger = logging.getLogger(__name__)

basedir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))))
fileName = basedir + '\\apiTestData\\global\\partner\\site\\' + os.path.basename(__file__).split('.')[0] + '.yml'
readfile = ReadFile(fileName)
cases, parameters = readfile.get_businessTests_data()
cases_oauth_token, parameters_oauth_token = readfile.get_businessTests_data()
illegal_cases, illegal_parameters = readfile.get_illegalInputTests_data()

for i in range(len(cases_oauth_token)):
    cases_oauth_token[i] = cases_oauth_token[i] + '[oauth_token]'

@allure.feature('edit site profile')
class TestUpdateSiteProfile:
    @pytest.mark.parametrize('case, http, expect', list(parameters), ids=cases)
    @pytest.mark.globaltest
    @pytest.mark.oden
    @pytest.mark.smoke
    @pytest.mark.billingapi
    def test_update_site_profile(self, case, http, expect, partnerLogin):
        login_info = partnerLogin
        site_id = ManageGlobalData().get_site_id()
        partner_id = ManageGlobalData().get_partner_id()
        agent_email = ManageGlobalData().get_agent_email()
        http['body'] = replace_dict_value(http['body'], '$siteId$', site_id)
        http['body'] = replace_dict_value(http['body'], '$partnerId$', partner_id)
        http['body'] = replace_dict_value(http['body'], '$email$', agent_email)
        get_response = test_api_request(login_info['partnerUrl'] + http['path'].replace('$siteId$', str(site_id)).replace('$partnerId$', str(partner_id)),
                                        http['method'], login_info['partnerCommonHeader'],
                                        http['body'])
        commonResponseAssert(get_response, expect)


    @pytest.mark.parametrize('case, http, expect', list(parameters_oauth_token), ids=cases_oauth_token)
    @pytest.mark.globaltest
    @pytest.mark.oden
    @pytest.mark.smoke
    @pytest.mark.billingapi
    def test_update_site_profile_auth_token(self, case, http, expect, partnerLogin):
        login_info = partnerLogin
        site_id = ManageGlobalData().get_site_id()
        partner_id = ManageGlobalData().get_partner_id()
        agent_email = ManageGlobalData().get_agent_email()
        http['body'] = replace_dict_value(http['body'], '$siteId$', site_id)
        http['body'] = replace_dict_value(http['body'], '$partnerId$', partner_id)
        http['body'] = replace_dict_value(http['body'], '$email$', agent_email)
        get_response = test_api_request(login_info['partnerUrl'] + http['path'].replace('$siteId$', str(site_id)).replace('$partnerId$', str(partner_id)),
                                        http['method'], login_info['partner_oauth_header'],
                                        http['body'])
        commonResponseAssert(get_response, expect)


    @pytest.mark.parametrize('case, http, expect', list(illegal_parameters), ids=illegal_cases)
    @pytest.mark.globaltest
    @pytest.mark.oden
    @pytest.mark.smoke
    @pytest.mark.billingapi
    def test_update_site_profile_illegal(self, case, http, expect, partnerLogin):
        login_info = partnerLogin
        site_id = ManageGlobalData().get_site_id()
        partner_id = ManageGlobalData().get_partner_id()
        agent_email = ManageGlobalData().get_agent_email()
        http['body'] = replace_dict_value(http['body'], '$siteId$', site_id)
        http['body'] = replace_dict_value(http['body'], '$partnerId$', partner_id)
        http['body'] = replace_dict_value(http['body'], '$email$', agent_email)
        get_response = test_api_request(login_info['partnerUrl'] + http['path'].replace('$siteId$', str(site_id)).replace('$partnerId$', str(partner_id)),
                                        http['method'], login_info['partnerCommonHeader'],
                                        http['body'])
        commonResponseAssert(get_response, expect)
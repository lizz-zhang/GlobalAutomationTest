import pytest
import allure
import os
from autoUtils.assertFactory import commonResponseAssert
from autoUtils.requestFactory import test_api_request
from autoUtils.ymlLib import ReadFile


basedir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))))
fileName = basedir + '\\apiTestData\\global\\partner\\partnerglobalapi\\' + os.path.basename(__file__).split('.')[0] + '.yml'
readfile = ReadFile(fileName)
cases, parameters = readfile.get_businessTests_data()
cases_oauth_token, parameters_oauth_token = readfile.get_businessTests_data()

for i in range(len(cases_oauth_token)):
    cases_oauth_token[i] = cases_oauth_token[i] + '[oauth_token]'

@allure.feature('get partner roles')
class TestGetPartnerRoles:
    @pytest.mark.parametrize('case, http, expect', list(parameters), ids=cases)
    @pytest.mark.globaltest
    @pytest.mark.oden
    @pytest.mark.smoke
    @pytest.mark.partnerglobalapi
    def test_get_partner_roles(self, case, http, expect, partnerLogin):
        login_info = partnerLogin
        get_response = test_api_request(login_info['partnerUrl'] + http['path'], http['method'], login_info['partnerCommonHeader'],
                                        None)
        commonResponseAssert(get_response, expect)


    @pytest.mark.parametrize('case, http, expect', list(parameters_oauth_token), ids=cases_oauth_token)
    @pytest.mark.globaltest
    @pytest.mark.oden
    @pytest.mark.smoke
    @pytest.mark.partnerglobalapi
    def test_get_partner_roles_oauth_token(self, case, http, expect, partnerLogin):
        login_info = partnerLogin
        get_response = test_api_request(login_info['partnerUrl'] + http['path'], http['method'], login_info['partner_oauth_header'],
                                        None)
        commonResponseAssert(get_response, expect)

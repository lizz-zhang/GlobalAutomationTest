import pytest
import allure
import os
from autoUtils.assertFactory import commonResponseAssert
from autoUtils.requestFactory import test_api_request, test_api_basic_auth_request
from autoUtils.ymlLib import ReadFile
from autoUtils.manage_global_data import ManageGlobalData
import pdb


basedir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))))
fileName = basedir + '\\apiTestData\\global\\platform\\contactapi\\' + os.path.basename(__file__).split('.')[0] + '.yml'
readfile = ReadFile(fileName)
cases, parameters = readfile.get_businessTests_data()
cases_api_key, parameters_api_key = readfile.get_businessTests_data()
cases_oauth_token, parameters_oauth_token = readfile.get_businessTests_data()
for i in range(len(cases_api_key)):
    cases_api_key[i] = cases_api_key[i]+'[api_key]'
for i in range(len(cases_oauth_token)):
    cases_oauth_token[i] = cases_oauth_token[i] + '[oauth_token]'

@allure.feature('get contacts:query')
class TestPostContactsQuery:
    @pytest.mark.parametrize('case, http, expect', list(parameters), ids=cases)
    @pytest.mark.parametrize('initial_data', ['contacts_new'], indirect=True)
    @pytest.mark.contactapi
    @pytest.mark.mila
    @pytest.mark.smoke
    def test_post_contacts_query(self, case, http, expect, login, initial_data):
        # pdb.set_trace
        login_info = login
        # pdb.set_trace
        site_id = ManageGlobalData().get_site_id()
        # pdb.set_trace
        get_response = test_api_request(login_info['dashUrl'] + http['path'].replace('$siteId$', str(site_id)), http['method'], login_info['commonHeader'], http['body'])
       
        commonResponseAssert(get_response, expect)


    @pytest.mark.parametrize('case, http, expect', list(parameters_api_key), ids=cases_api_key)
    @pytest.mark.parametrize('initial_data', ['contacts_new'], indirect=True)
    @pytest.mark.contactapi
    @pytest.mark.mila
    @pytest.mark.smoke
    def test_post_contacts_query_api_key(self, case, http, expect, login, initial_data):
        login_info = login
        site_id = ManageGlobalData().get_site_id()
        get_response = test_api_basic_auth_request(login_info['dashUrl'] + http['path'].replace('$siteId$', str(site_id)), http['method'], http['body'])
        commonResponseAssert(get_response, expect)

    @pytest.mark.parametrize('case, http, expect', list(parameters_oauth_token), ids=cases_oauth_token)
    @pytest.mark.parametrize('initial_data', ['contacts_new'], indirect=True)
    @pytest.mark.contactapi
    @pytest.mark.mila
    @pytest.mark.smoke
    def test_post_contacts_query_oauth_token(self, case, http, expect, login, initial_data):
        login_info = login
        site_id = ManageGlobalData().get_site_id()
        get_response = test_api_request(login_info['dashUrl'] + http['path'].replace('$siteId$', str(site_id)), http['method'], login_info['oauth_header'], http['body'])
        commonResponseAssert(get_response, expect)

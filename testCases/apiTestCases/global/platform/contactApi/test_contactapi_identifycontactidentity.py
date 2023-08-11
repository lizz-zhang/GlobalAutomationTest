import pytest
import allure
import os
from autoUtils.assertFactory import commonResponseAssert, afterCaseActionAndAssert
from autoUtils.requestFactory import test_api_request, test_api_basic_auth_request
from autoUtils.ymlLib import ReadFile
from autoUtils.manage_global_data import ManageGlobalData
import logging
from autoUtils.optionUtil import upload_file, replace_dict_value
import json

logger = logging.getLogger(__name__)
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



@allure.feature('identify contact identity')
class TestIdentifyContactIdentity:
    @pytest.mark.parametrize('case, http, expect', list(parameters), ids=cases)
    @pytest.mark.parametrize('initial_data', ['contacts_new'], indirect=True)
    @pytest.mark.contactapi
    @pytest.mark.oden
    @pytest.mark.smoke
    def test_identify_contact(self, case, http, expect, login, initial_data):
        login_info = login
        site_id = ManageGlobalData().get_site_id()
        initial_contact = initial_data
        if initial_contact['contactIdentities'][0]['contactIdentityType'] == 'Email':
            email_value = initial_contact['contactIdentities'][0]['value']
        else:
            email_value = initial_contact['contactIdentities'][1]['id']
        get_response = test_api_request(login_info['dashUrl'] + http['path'].replace('$siteId$', str(site_id)).replace('$value$', email_value),
                                        http['method'], login_info['commonHeader'], None)
        commonResponseAssert(get_response, expect)


    @pytest.mark.parametrize('case, http, expect', list(parameters_api_key), ids=cases_api_key)
    @pytest.mark.parametrize('initial_data', ['contacts_new'], indirect=True)
    @pytest.mark.contactapi
    @pytest.mark.oden
    @pytest.mark.smoke
    def test_identify_contact_api_key(self, case, http, expect, login, initial_data):
        login_info = login
        site_id = ManageGlobalData().get_site_id()
        initial_contact = initial_data
        if initial_contact['contactIdentities'][0]['contactIdentityType'] == 'Email':
            email_value = initial_contact['contactIdentities'][0]['value']
        else:
            email_value = initial_contact['contactIdentities'][1]['id']
        get_response = test_api_basic_auth_request(login_info['dashUrl'] + http['path'].replace('$siteId$', str(site_id)).replace('$value$', email_value),
                                        http['method'], None)
        commonResponseAssert(get_response, expect)

    @pytest.mark.parametrize('case, http, expect', list(parameters_oauth_token), ids=cases_oauth_token)
    @pytest.mark.parametrize('initial_data', ['contacts_new'], indirect=True)
    @pytest.mark.contactapi
    @pytest.mark.oden
    @pytest.mark.smoke
    def test_identify_contact_auth_token(self, case, http, expect, login, initial_data):
        login_info = login
        site_id = ManageGlobalData().get_site_id()
        initial_contact = initial_data
        if initial_contact['contactIdentities'][0]['contactIdentityType'] == 'Email':
            email_value = initial_contact['contactIdentities'][0]['value']
        else:
            email_value = initial_contact['contactIdentities'][1]['id']
        get_response = test_api_request(login_info['dashUrl'] + http['path'].replace('$siteId$', str(site_id)).replace('$value$', email_value),
                                        http['method'], login_info['oauth_header'], None)
        commonResponseAssert(get_response, expect)

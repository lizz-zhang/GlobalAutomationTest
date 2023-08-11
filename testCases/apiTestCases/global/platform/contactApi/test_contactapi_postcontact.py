from copy import deepcopy

import pytest
import allure
import os
from autoUtils.assertFactory import commonResponseAssert, afterCaseActionAndAssert
from autoUtils.requestFactory import test_api_request, test_api_basic_auth_request
from autoUtils.ymlLib import ReadFile
from autoUtils.manage_global_data import ManageGlobalData
from autoUtils.optionUtil import change_to_random_string, change_to_random_int
import logging
import pdb


logger = logging.getLogger(__name__)
basedir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))))
fileName = basedir + '\\apiTestData\\global\\platform\\contactApi\\' + os.path.basename(__file__).split('.')[0] + '.yml'
readfile = ReadFile(fileName)
cases, parameters = readfile.get_businessTests_data()
cases_api_key, parameters_api_key = readfile.get_businessTests_data()
cases_oauth_token, parameters_oauth_token = readfile.get_businessTests_data()
cases_illegal, parameters_illegal = readfile.get_illegalInputTests_data()
for i in range(len(cases_api_key)):
    cases_api_key[i] = cases_api_key[i]+'[api_key]'
for i in range(len(cases_oauth_token)):
    cases_oauth_token[i] = cases_oauth_token[i] + '[oauth_token]'



@allure.feature('post a contact ')
class TestPostContact:
    @pytest.mark.parametrize('case, http, expect', list(parameters), ids=cases)
    @pytest.mark.contactapi
    @pytest.mark.mila
    @pytest.mark.smoke
    def test_post_contact_by_id(self, case, http, expect, login):
        login_info = login
        site_id = ManageGlobalData().get_site_id()
        body1 = deepcopy(http['body'])
        body2 = deepcopy(http['body'])
        body1 = change_to_random_string(body1)
        body1 = change_to_random_int(body1)
        # pdb.set_trace()
        body2 = change_to_random_string(body2)
        body2 = change_to_random_int(body2)

        get_response1 = test_api_request(login_info['dashUrl'] + http['path'].replace('$siteId$', str(site_id)),
                                         http['method'], login_info['commonHeader'], body1)

        get_response2 = test_api_request(login_info['dashUrl'] + http['path'].replace('$siteId$', str(site_id)),http['method'], login_info['commonHeader'],body2)
        # pdb.set_trace
        commonResponseAssert(get_response2, expect)
        afterCaseActionAndAssert(login_info['dashUrl'], login_info['commonHeader'], get_response1, expect)
        afterCaseActionAndAssert(login_info['dashUrl'], login_info['commonHeader'], get_response2, expect)

    @pytest.mark.parametrize('case, http, expect', list(parameters_api_key), ids=cases_api_key)
    @pytest.mark.contactapi
    @pytest.mark.mila
    @pytest.mark.smoke
    def test_post_contact_api_key(self, case, http, expect, login):
        login_info = login
        site_id = ManageGlobalData().get_site_id()
        body1 = deepcopy(http['body'])
        body2 = deepcopy(http['body'])
        body1 = change_to_random_string(body1)
        body1 = change_to_random_int(body1)
        # pdb.set_trace()
        body2 = change_to_random_string(body2)
        body2 = change_to_random_int(body2)

        get_response1 = test_api_basic_auth_request(login_info['dashUrl'] + http['path'].replace('$siteId$', str(site_id)),http['method'], body1)

        get_response2 = test_api_basic_auth_request(login_info['dashUrl'] + http['path'].replace('$siteId$', str(site_id)),http['method'],body2)
        # pdb.set_trace
        commonResponseAssert(get_response2, expect)
        afterCaseActionAndAssert(login_info['dashUrl'], login_info['commonHeader'], get_response1, expect)
        afterCaseActionAndAssert(login_info['dashUrl'], login_info['commonHeader'], get_response2, expect)

    @pytest.mark.parametrize('case, http, expect', list(parameters_oauth_token), ids=cases_oauth_token)
    @pytest.mark.contactapi
    @pytest.mark.mila
    @pytest.mark.smoke
    def test_post_contact_oauth_token(self, case, http, expect, login):
        login_info = login
        site_id = ManageGlobalData().get_site_id()
        body1 = deepcopy(http['body'])
        body2 = deepcopy(http['body'])
        body1 = change_to_random_string(body1)
        body1 = change_to_random_int(body1)
        # pdb.set_trace()
        body2 = change_to_random_string(body2)
        body2 = change_to_random_int(body2)

        get_response1 = test_api_request(login_info['dashUrl'] + http['path'].replace('$siteId$', str(site_id)),http['method'], login_info['oauth_header'], body1)

        get_response2 = test_api_request(login_info['dashUrl'] + http['path'].replace('$siteId$', str(site_id)),http['method'], login_info['oauth_header'], body2)
        # pdb.set_trace
        commonResponseAssert(get_response2, expect)
        afterCaseActionAndAssert(login_info['dashUrl'], login_info['oauth_header'], get_response1, expect)
        afterCaseActionAndAssert(login_info['dashUrl'], login_info['oauth_header'], get_response2, expect)


    @pytest.mark.parametrize('case, http, expect', list(parameters_illegal), ids=cases_illegal)
    @pytest.mark.contactapi
    @pytest.mark.mila
    @pytest.mark.smoke
    def test_post_contact_illegal(self, case, http, expect, login):
        login_info = login
        site_id = ManageGlobalData().get_site_id()
        get_response = test_api_request(login_info['dashUrl'] + http['path'].replace('$siteId$', str(site_id)), http['method'], login_info['oauth_header'],change_to_random_string(http['body']))

        afterCaseActionAndAssert(login_info['dashUrl'], login_info['commonHeader'], get_response, expect)

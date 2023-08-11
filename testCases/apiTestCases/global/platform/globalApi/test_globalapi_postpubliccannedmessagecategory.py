import pytest
import allure
import os
from autoUtils.assertFactory import commonResponseAssert, afterCaseActionAndAssert
from autoUtils.requestFactory import test_api_request, test_api_basic_auth_request
from autoUtils.ymlLib import ReadFile
from autoUtils.manage_global_data import ManageGlobalData
from autoUtils.optionUtil import get_public_canned_message_rootcategory, ifItemInKeysAndValueNotNone


basedir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))))
fileName = basedir + '\\apiTestData\\global\\platform\\globalapi\\' + os.path.basename(__file__).split('.')[0] + '.yml'
readfile = ReadFile(fileName)
cases, parameters = readfile.get_businessTests_data()
cases_api_key, parameters_api_key = readfile.get_businessTests_data()
cases_oauth_token, parameters_oauth_token = readfile.get_businessTests_data()
illegal_cases, illegal_parameters = readfile.get_illegalInputTests_data()
illegal_cases_oauth_token, illegal_parameters_oauth_token = readfile.get_illegalInputTests_data()

class TestPostPublicCannedMessageCategory:
    @pytest.mark.globalapi
    @pytest.mark.cannedmessages
    @pytest.mark.bella
    @pytest.mark.parametrize('case, http, expect', list(parameters), ids=cases)
    def test_post_public_cannedmessage_category(self, case, http, expect, login):
        login_info = login
        rootcategory_Id = get_public_canned_message_rootcategory(login)
        http['body']['parentId'] = http['body']['parentId'].replace('$parentId$', str(rootcategory_Id))
        get_response = test_api_request(login_info['dashUrl'] + http['path'], http['method'], login_info['commonHeader'], http['body'])
        commonResponseAssert(get_response, expect)

        if ifItemInKeysAndValueNotNone('aftercaseaction', expect):
            afterCaseActionAndAssert(login_info['dashUrl'], login_info['commonHeader'], get_response, expect)

    @pytest.mark.globalapi
    @pytest.mark.cannedmessages
    @pytest.mark.bella
    @pytest.mark.parametrize('case, http, expect', list(parameters_oauth_token), ids=cases_oauth_token)
    def test_post__public_cannedmessage_categoriey_oauth_token(self, case, http, expect, login):
        login_info = login
        rootcategory_Id = get_public_canned_message_rootcategory(login)
        http['body']['parentId'] = http['body']['parentId'].replace('$parentId$', str(rootcategory_Id))
        get_response_oauth_token = test_api_request(login_info['dashUrl'] + http['path'], http['method'], login_info['oauth_header'], http['body'])
        commonResponseAssert(get_response_oauth_token, expect)

        if ifItemInKeysAndValueNotNone('aftercaseaction', expect):
            afterCaseActionAndAssert(login_info['dashUrl'], login_info['commonHeader'], get_response_oauth_token, expect)


    @pytest.mark.parametrize('case, http, expect', list(illegal_parameters), ids=illegal_cases)
    @pytest.mark.globalapi
    @pytest.mark.cannedmessages
    @pytest.mark.bella
    def test_post__public_cannedmessage_categoriey_illegal(self, case, http, expect, login):
        login_info = login
        rootcategory_Id = get_public_canned_message_rootcategory(login)
        if ifItemInKeysAndValueNotNone('parentId', http['body']):
            http['body']['parentId'] = http['body']['parentId'].replace('$parentId$', str(rootcategory_Id))
        get_response = test_api_request(login_info['dashUrl'] + http['path'], http['method'], login_info['commonHeader'], http['body'])
        commonResponseAssert(get_response, expect)

    @pytest.mark.parametrize('case, http, expect', list(illegal_parameters_oauth_token), ids=illegal_cases_oauth_token)
    @pytest.mark.globalapi
    @pytest.mark.cannedmessages
    @pytest.mark.bella
    def test_post__public_cannedmessage_categoriey_illegal_oauth_token(self, case, http, expect, login):
        login_info = login
        rootcategory_Id = get_public_canned_message_rootcategory(login)
        if ifItemInKeysAndValueNotNone('parentId', http['body']):
            http['body']['parentId'] = http['body']['parentId'].replace('$parentId$', str(rootcategory_Id))
        get_responsee_oauth_token = test_api_request(login_info['dashUrl'] + http['path'], http['method'], login_info['oauth_header'], http['body'])
        commonResponseAssert(get_responsee_oauth_token, expect)
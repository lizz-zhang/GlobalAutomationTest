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


class TestPutPublicCannedMessageCategory:
    @pytest.mark.globalapi
    @pytest.mark.cannedmessages
    @pytest.mark.bella
    @pytest.mark.parametrize('case, http, expect', list(parameters), ids=cases)
    @pytest.mark.parametrize('initial_data', ['publiccannedmessagecategory'] , indirect=True)
    def test_put_public_cannedmessage_category(self, case, http, expect, login, initial_data):
        login_info = login
        initial_public_canned_message_categoryid = initial_data['id']
        get_response = test_api_request(login_info['dashUrl'] + http['path'].replace('$id$', str(initial_public_canned_message_categoryid)), http['method'], login_info['commonHeader'], http['body'])
        commonResponseAssert(get_response, expect)

        if ifItemInKeysAndValueNotNone('aftercaseaction', expect):
            expect['aftercasepath'] = expect['aftercasepath'].replace('$id$', str(initial_public_canned_message_categoryid))
            afterCaseActionAndAssert(login_info['dashUrl'], login_info['commonHeader'], get_response, expect)

    @pytest.mark.globalapi
    @pytest.mark.cannedmessages
    @pytest.mark.bella
    @pytest.mark.parametrize('case, http, expect', list(parameters_oauth_token), ids=cases_oauth_token)
    @pytest.mark.parametrize('initial_data', ['publiccannedmessagecategory'] , indirect=True)
    def test_put__public_cannedmessage_category_oauth_token(self, case, http, expect, login, initial_data):
        login_info = login
        initial_public_canned_message_categoryid = initial_data['id']
        get_response_oauth_token = test_api_request(login_info['dashUrl'] + http['path'].replace('$id$', str(initial_public_canned_message_categoryid)), http['method'], login_info['oauth_header'], http['body'])
        commonResponseAssert(get_response_oauth_token, expect)

        if ifItemInKeysAndValueNotNone('aftercaseaction', expect):
            expect['aftercasepath'] = expect['aftercasepath'].replace('$id$', str(initial_public_canned_message_categoryid))
            afterCaseActionAndAssert(login_info['dashUrl'], login_info['commonHeader'], get_response_oauth_token, expect)
import json

import pytest
import allure
import os
from autoUtils.assertFactory import commonResponseAssert
from autoUtils.fileReader import read_config_file
from autoUtils.optionUtil import change_to_random_string, change_to_random_int, replace_dict_value
from autoUtils.requestFactory import test_api_request, test_api_basic_auth_request
from autoUtils.ymlLib import ReadFile
from autoUtils.manage_global_data import ManageGlobalData
import logging
import pdb

logger = logging.getLogger(__name__)
basedir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))))
fileName = basedir + '\\apiTestData\\global\\platform\\contactApi\\' + os.path.basename(__file__).split('.')[0] + '.yml'
readfile = ReadFile(fileName)
cases, parameters = readfile.get_businessTests_data()
cases_api_key, parameters_api_key = readfile.get_businessTests_data()
cases_oauth_token, parameters_oauth_token = readfile.get_businessTests_data()
for i in range(len(cases_api_key)):
    cases_api_key[i] = cases_api_key[i] + '[api_key]'
for i in range(len(cases_oauth_token)):
    cases_oauth_token[i] = cases_oauth_token[i] + '[oauth_token]'


@allure.feature('batch delete contact by ids')
class TestBatchDeleteContactById:
    @pytest.mark.parametrize('case, http, expect', list(parameters), ids=cases)
    @pytest.mark.parametrize('function_initial_data', ['contacts_new'], indirect=True)
    @pytest.mark.contactapi
    @pytest.mark.mila
    @pytest.mark.smoke
    def test_batch_delete_contact_by_id(self, case, http, expect, login, function_initial_data):
        login_info = login
        site_id = ManageGlobalData().get_site_id()

        initial_contact1 = function_initial_data
        # pdb.set_trace()
        global_test_data = read_config_file('global_test_data.json')
        body = global_test_data['contacts_visitor']['body']
        body = change_to_random_string(body)
        body = change_to_random_int(body)
        method = global_test_data['contacts_visitor']['createMethod']
        url = login_info['dashUrl'] + global_test_data['contacts_visitor']['createPath']
        create_contact = test_api_request(url, method, login_info['commonHeader'], body)
        if create_contact.status_code == 201:
            logger.info('contacts_new data initial success')
        else:
            logger.info('contacts_new data initial failed,please retry')
        initial_contact2 = json.loads(create_contact.content)
        lists = ['$id1$', '$id2$']
        replace_dict = {'$id1$': initial_contact1['id'], "$id2$": initial_contact2['id']}
        new_lists = [replace_dict[i] if i in replace_dict else i for i in lists]
        # body1 = json.parse(body)
        # pdb.set_trace()
        get_response = test_api_request(login_info['dashUrl'] + http['path'].replace('$siteId$', str(site_id)), http['method'], login_info['commonHeader'],new_lists)
        commonResponseAssert(get_response, expect)

    @pytest.mark.parametrize('case, http, expect', list(parameters_api_key), ids=cases_api_key)
    @pytest.mark.parametrize('function_initial_data', ['contacts_new'], indirect=True)
    @pytest.mark.contactapi
    @pytest.mark.mila
    @pytest.mark.smoke
    @pytest.mark.apikey
    def test_batch_delete_contact_by_id_apikey(self, case, http, expect, login, function_initial_data):
        login_info = login
        site_id = ManageGlobalData().get_site_id()

        initial_contact1 = function_initial_data
        # pdb.set_trace()
        global_test_data = read_config_file('global_test_data.json')
        body = global_test_data['contacts_visitor']['body']
        body = change_to_random_string(body)
        body = change_to_random_int(body)
        method = global_test_data['contacts_visitor']['createMethod']
        url = login_info['dashUrl'] + global_test_data['contacts_visitor']['createPath']
        create_contact = test_api_request(url, method, login_info['commonHeader'], body)
        if create_contact.status_code == 201:
            logger.info('contacts_new data initial success')
        else:
            logger.info('contacts_new data initial failed,please retry')
        initial_contact2 = json.loads(create_contact.content)
        lists = ['$id1$', '$id2$']
        replace_dict = {'$id1$': initial_contact1['id'], "$id2$": initial_contact2['id']}
        new_lists = [replace_dict[i] if i in replace_dict else i for i in lists]
        # body1 = json.parse(body)
        # pdb.set_trace()
        get_response = test_api_basic_auth_request(login_info['dashUrl'] + http['path'].replace('$siteId$', str(site_id)), http['method'], new_lists)
        commonResponseAssert(get_response, expect)


    @pytest.mark.parametrize('case, http, expect', list(parameters_oauth_token), ids=cases_oauth_token)
    @pytest.mark.parametrize('function_initial_data', ['contacts_new'], indirect=True)
    @pytest.mark.contactapi
    @pytest.mark.mila
    @pytest.mark.smoke
    def test_batch_delete_contact_by_id_oauth_token(self, case, http, expect, login, function_initial_data):
        login_info = login
        site_id = ManageGlobalData().get_site_id()

        initial_contact1 = function_initial_data
        # pdb.set_trace()
        global_test_data = read_config_file('global_test_data.json')
        body = global_test_data['contacts_visitor']['body']
        body = change_to_random_string(body)
        body = change_to_random_int(body)
        method = global_test_data['contacts_visitor']['createMethod']
        url = login_info['dashUrl'] + global_test_data['contacts_visitor']['createPath']
        create_contact = test_api_request(url, method, login_info['commonHeader'], body)
        if create_contact.status_code == 201:
            logger.info('contacts_new data initial success')
        else:
            logger.info('contacts_new data initial failed,please retry')
        initial_contact2 = json.loads(create_contact.content)
        lists = ['$id1$', '$id2$']
        replace_dict = {'$id1$': initial_contact1['id'], "$id2$": initial_contact2['id']}
        new_lists = [replace_dict[i] if i in replace_dict else i for i in lists]
        # body1 = json.parse(body)
        # pdb.set_trace()
        get_response = test_api_request(
            login_info['dashUrl'] + http['path'].replace('$siteId$', str(site_id)), http['method'],
            login_info['oauth_header'], new_lists)
        commonResponseAssert(get_response, expect)

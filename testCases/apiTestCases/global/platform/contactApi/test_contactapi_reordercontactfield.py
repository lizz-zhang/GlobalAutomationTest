import json
import pdb

import pytest
import allure
import os
from autoUtils.assertFactory import commonResponseAssert, afterCaseActionAndAssert
from autoUtils.fileReader import read_config_file
from autoUtils.requestFactory import test_api_request, test_api_basic_auth_request
from autoUtils.ymlLib import ReadFile
from autoUtils.manage_global_data import ManageGlobalData
from autoUtils.optionUtil import change_to_random_string, change_to_random_int
import logging



logger = logging.getLogger(__name__)
basedir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))))
fileName = basedir + '\\apiTestData\\global\\platform\\contactApi\\' + os.path.basename(__file__).split('.')[0] + '.yml'
readfile = ReadFile(fileName)

cases, parameters = readfile.get_businessTests_data()
cases_api_key, parameters_api_key = readfile.get_businessTests_data()
cases_oauth_token, parameters_oauth_token = readfile.get_businessTests_data()
for i in range(len(cases_api_key)):
    cases_api_key[i] = cases_api_key[i]+'[api_key]'
for i in range(len(cases_oauth_token)):
    cases_oauth_token[i] = cases_oauth_token[i] + '[oauth_token]'



@allure.feature('reorder a contact field ')
class TestReorderContactField:
    @pytest.mark.parametrize('case, http, expect', list(parameters), ids=cases)
    @pytest.mark.parametrize('initial_data', ['contact_fields'], indirect=True)
    @pytest.mark.contactapi
    @pytest.mark.mila
    @pytest.mark.smoke
    def test_reorder_contact_field(self, case, http, expect, login, initial_data):
        login_info = login
        site_id = ManageGlobalData().get_site_id()

        initial_contact_field1 = initial_data
        # pdb.set_trace()
        global_test_data = read_config_file('global_test_data.json')
        body = global_test_data['contact_fields_reorder']['body']
        body = change_to_random_string(body)
        body = change_to_random_int(body)
        method = global_test_data['contact_fields_reorder']['createMethod']
        url = login_info['dashUrl'] + global_test_data['contact_fields_reorder']['createPath']

        create_contact_field = test_api_request(url, method, login_info['commonHeader'], body)
        if create_contact_field.status_code == 201:
            logger.info('create_contact_field data initial success')
        else:
            logger.info('create_contact_field data initial failed,please retry')
        initial_contact_field2 = json.loads(create_contact_field.content)

        body_list = list(http['body'])
        id1 = body_list[0]
        id2 = body_list[1]
        lists = [id1, id2]

        # pdb.set_trace()
        replace_dict = {'$id1$': initial_contact_field1['id'], "$id2$": initial_contact_field2['id']}
        new_lists = [replace_dict[i] if i in replace_dict else i for i in lists]
        a = login_info['dashUrl'] + http['path'].replace('$siteId$', str(site_id))
        b = new_lists
        get_response = test_api_request(login_info['dashUrl'] + http['path'].replace('$siteId$', str(site_id)), http['method'], login_info['commonHeader'], new_lists)
        commonResponseAssert(get_response, expect)
        # pdb.set_trace()
        delete_url = login_info['dashUrl'] + expect['aftercasepath'].replace('$id$', initial_contact_field2['id']).replace('$siteId$', str(site_id))
        delete_response = test_api_request(delete_url, expect['aftercaseaction'], login_info['commonHeader'],None)
        if delete_response.status_code == 204:
            logger.info('delete contact_field data success')
        else:
            logger.info('delete contact_field data failed')

    @pytest.mark.parametrize('case, http, expect', list(parameters_api_key), ids=cases_api_key)
    @pytest.mark.parametrize('initial_data', ['contact_fields'], indirect=True)
    @pytest.mark.contactapi
    @pytest.mark.mila
    @pytest.mark.smoke
    def test_reorder_contact_field_api_key(self, case, http, expect, login, initial_data):
        login_info = login
        site_id = ManageGlobalData().get_site_id()

        initial_contact_field1 = initial_data
        # pdb.set_trace()
        global_test_data = read_config_file('global_test_data.json')
        body = global_test_data['contact_fields_reorder']['body']
        body = change_to_random_string(body)
        body = change_to_random_int(body)
        method = global_test_data['contact_fields_reorder']['createMethod']
        url = login_info['dashUrl'] + global_test_data['contact_fields_reorder']['createPath']
        create_contact_field = test_api_request(url, method, login_info['commonHeader'], body)
        if create_contact_field.status_code == 201:
            logger.info('create_contact_field data initial success')
        else:
            logger.info('create_contact_field data initial failed,please retry')
        initial_contact_field2 = json.loads(create_contact_field.content)

        body_list = list(http['body'])
        id1 = body_list[0]
        id2 = body_list[1]
        lists = [id1, id2]

        replace_dict = {'$id1$': initial_contact_field1['id'], "$id2$": initial_contact_field2['id']}
        new_lists = [replace_dict[i] if i in replace_dict else i for i in lists]
        get_response = test_api_basic_auth_request(login_info['dashUrl'] + http['path'].replace('$siteId$', str(site_id)),http['method'], new_lists)
        commonResponseAssert(get_response, expect)
        # pdb.set_trace()
        delete_url = login_info['dashUrl'] + expect['aftercasepath'].replace('$id$', initial_contact_field2['id']).replace('$siteId$', str(site_id))
        delete_response = test_api_request(delete_url, expect['aftercaseaction'], login_info['commonHeader'], None)
        if delete_response.status_code == 204:
            logger.info('delete contact_field data success')
        else:
            logger.info('delete contact_field data failed')


    @pytest.mark.parametrize('case, http, expect', list(parameters_oauth_token), ids=cases_oauth_token)
    @pytest.mark.parametrize('initial_data', ['contact_fields'], indirect=True)
    @pytest.mark.contactapi
    @pytest.mark.mila
    @pytest.mark.smoke
    def test_reorder_contact_field_oauth_token(self, case, http, expect, login, initial_data):
        login_info = login
        site_id = ManageGlobalData().get_site_id()

        initial_contact_field1 = initial_data
        # pdb.set_trace()
        global_test_data = read_config_file('global_test_data.json')
        body = global_test_data['contact_fields_reorder']['body']
        body = change_to_random_string(body)
        body = change_to_random_int(body)
        method = global_test_data['contact_fields_reorder']['createMethod']
        url = login_info['dashUrl'] + global_test_data['contact_fields_reorder']['createPath']
        create_contact_field = test_api_request(url, method, login_info['commonHeader'], body)
        if create_contact_field.status_code == 201:
            logger.info('create_contact_field data initial success')
        else:
            logger.info('create_contact_field data initial failed,please retry')
        initial_contact_field2 = json.loads(create_contact_field.content)

        body_list = list(http['body'])
        id1 = body_list[0]
        id2 = body_list[1]
        lists = [id1, id2]

        replace_dict = {'$id1$': initial_contact_field1['id'], "$id2$": initial_contact_field2['id']}
        new_lists = [replace_dict[i] if i in replace_dict else i for i in lists]
        get_response = test_api_request(login_info['dashUrl'] + http['path'].replace('$siteId$', str(site_id)),
                                        http['method'], login_info['oauth_header'], new_lists)
        commonResponseAssert(get_response, expect)
        # pdb.set_trace()
        delete_url = login_info['dashUrl'] + expect['aftercasepath'].replace('$id$',
                                                                             initial_contact_field2['id']).replace(
            '$siteId$', str(site_id))
        delete_response = test_api_request(delete_url, expect['aftercaseaction'], login_info['commonHeader'], None)
        if delete_response.status_code == 204:
            logger.info('delete contact_field data success')
        else:
            logger.info('delete contact_field data failed')

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
import time


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



@allure.feature('import contact')
class TestImportContact:
    @pytest.mark.parametrize('case, http, expect', list(parameters), ids=cases)
    @pytest.mark.contactapi
    @pytest.mark.oden
    @pytest.mark.smoke
    def test_import_contact(self, case, http, expect, login):

        filekey = upload_file('ContactFileServiceTokenPath', 'Import_Contacts.csv', 'platform')
        uploadFileURL = ManageGlobalData().get_file_url() + '//' + str(filekey)
        login_info = login
        site_id = ManageGlobalData().get_site_id()
        body = replace_dict_value(http['body'], '$file_url$', uploadFileURL)
        get_response = test_api_request(login_info['dashUrl'] + http['path'].replace('$siteId$', str(site_id)), http['method'], login_info['commonHeader'],
                                        body)
        commonResponseAssert(get_response, expect)

        time.sleep(5)
        get_contacts_response = test_api_request(login_info['dashUrl'] + '/api/contact/contacts/?siteid=$siteId$'.replace('$siteId$', str(site_id)), 'GET', login_info['commonHeader'],
                                        None)
        contacts = json.loads(get_contacts_response.content)
        contact_id = contacts['contacts'][0]['id']
        delete_response = test_api_request(
            login_info['dashUrl'] + '/api/contact/contacts/$id$?siteid=$siteId$'.replace('$siteId$', str(site_id)).replace('$id$', contact_id), 'DELETE',
            login_info['commonHeader'],
            None)
        if delete_response.status_code == '204':
            logger.info('delete contact data successful')
        else:
            logger.error("Delete failed,please manual delete contact data,Response Code is not correct,actual code: %s,content is %s" % (
             delete_response.status_code, delete_response.content))




    @pytest.mark.parametrize('case, http, expect', list(parameters_api_key), ids=cases_api_key)
    @pytest.mark.contactapi
    @pytest.mark.oden
    @pytest.mark.smoke
    def test_import_contact_api_key(self, case, http, expect, login):

        filekey = upload_file('ContactFileServiceTokenPath', 'Import_Contacts.csv', 'platform')
        uploadFileURL = ManageGlobalData().get_file_url() + '//' + str(filekey)
        login_info = login
        site_id = ManageGlobalData().get_site_id()
        body = replace_dict_value(http['body'], '$file_url$', uploadFileURL)
        get_response = test_api_basic_auth_request(login_info['dashUrl'] + http['path'].replace('$siteId$', str(site_id)), http['method'], body)
        commonResponseAssert(get_response, expect)

        time.sleep(5)
        get_contacts_response = test_api_request(login_info['dashUrl'] + '/api/contact/contacts/?siteid=$siteId$'.replace('$siteId$', str(site_id)), 'GET', login_info['commonHeader'],
                                        None)
        contacts = json.loads(get_contacts_response.content)
        contact_id = contacts['contacts'][0]['id']
        delete_response = test_api_request(
            login_info['dashUrl'] + '/api/contact/contacts/$id$?siteid=$siteId$'.replace('$siteId$', str(site_id)).replace('$id$', contact_id), 'DELETE',
            login_info['commonHeader'],
            None)
        if delete_response.status_code == '204':
            logger.info('delete contact data successful')
        else:
            logger.error("Delete failed,please manual delete contact data,Response Code is not correct,actual code: %s,content is %s" % (
             delete_response.status_code, delete_response.content))


    @pytest.mark.parametrize('case, http, expect', list(parameters_oauth_token), ids=cases_oauth_token)
    @pytest.mark.contactapi
    @pytest.mark.oden
    @pytest.mark.smoke
    def test_import_contact_oauth_token(self, case, http, expect, login):

        filekey = upload_file('ContactFileServiceTokenPath', 'Import_Contacts.csv', 'platform')
        uploadFileURL = ManageGlobalData().get_file_url() + '//' + str(filekey)
        login_info = login
        site_id = ManageGlobalData().get_site_id()
        body = replace_dict_value(http['body'], '$file_url$', uploadFileURL)
        get_response = test_api_request(login_info['dashUrl'] + http['path'].replace('$siteId$', str(site_id)), http['method'], login_info['oauth_header'],
                                        body)
        commonResponseAssert(get_response, expect)

        time.sleep(5)
        get_contacts_response = test_api_request(login_info['dashUrl'] + '/api/contact/contacts/?siteid=$siteId$'.replace('$siteId$', str(site_id)), 'GET', login_info['commonHeader'],
                                        None)
        contacts = json.loads(get_contacts_response.content)
        contact_id = contacts['contacts'][0]['id']
        delete_response = test_api_request(
            login_info['dashUrl'] + '/api/contact/contacts/$id$?siteid=$siteId$'.replace('$siteId$', str(site_id)).replace('$id$', contact_id), 'DELETE',
            login_info['commonHeader'],
            None)
        if delete_response.status_code == '204':
            logger.info('delete contact data successful')
        else:
            logger.error("Delete failed,please manual delete contact data,Response Code is not correct,actual code: %s,content is %s" % (
             delete_response.status_code, delete_response.content))


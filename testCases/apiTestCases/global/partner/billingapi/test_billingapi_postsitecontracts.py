import json
import pytest
import allure
import os
from autoUtils.assertFactory import commonResponseAssert, afterCaseActionAndAssert
from autoUtils.requestFactory import test_api_request, test_api_basic_auth_request
from autoUtils.ymlLib import ReadFile
from autoUtils.manage_global_data import ManageGlobalData
from autoUtils.optionUtil import ifItemInKeysAndValueNotNone, upload_file



basedir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))))
fileName = basedir + '\\apiTestData\\global\\partner\\billingapi\\' + os.path.basename(__file__).split('.')[0] + '.yml'
readfile = ReadFile(fileName)
cases, parameters = readfile.get_businessTests_data()
cases_oauth_token, parameters_oauth_token = readfile.get_businessTests_data()


class TestPostSiteContract:
    @pytest.mark.billingapi
    @pytest.mark.sitecontract
    @pytest.mark.bella
    @pytest.mark.parametrize('case, http, expect', list(parameters), ids=cases)
    def test_post_sitecontract(self, case, http, expect, partnerLogin):
        partnerLogin_info = partnerLogin
        paid_siteId = ManageGlobalData().get_partner_paidsiteid()
        http['body']['siteId'] = http['body']['siteId'].replace('$siteId$', str(paid_siteId))
        file_key = upload_file('partnerFileServiceTokenPath', 'test_jpg.jpg', 'partner')
        http['body']['siteContractAttachments'][0]['attachment'] = partnerLogin['fileServiceUrl'] + http['body']['siteContractAttachments'][0]['attachment'].replace('$fileKey$', file_key)
        get_response = test_api_request(partnerLogin_info['partnerUrl'] + http['path'], http['method'], partnerLogin_info['partnerCommonHeader'], http['body'])
        if ifItemInKeysAndValueNotNone('siteId', expect['responseitemcheck']):
            expect['responseitemcheck']['siteId'] = paid_siteId
        commonResponseAssert(get_response, expect)

        if ifItemInKeysAndValueNotNone('aftercaseaction', expect):
            afterCaseActionAndAssert(partnerLogin_info['partnerUrl'], partnerLogin_info['partnerCommonHeader'], get_response, expect)


    @pytest.mark.billingapi
    @pytest.mark.sitecontract
    @pytest.mark.bella
    @pytest.mark.parametrize('case, http, expect', list(parameters_oauth_token), ids=cases_oauth_token)
    def test_post_sitecontract_oauth_token(self, case, http, expect, partnerLogin):
        partnerLogin_info = partnerLogin
        paid_siteId = ManageGlobalData().get_partner_paidsiteid()
        http['body']['siteId'] = http['body']['siteId'].replace('$siteId$', str(paid_siteId))
        file_key = upload_file('partnerFileServiceTokenPath', 'test_jpg.jpg', 'partner')
        http['body']['siteContractAttachments'][0]['attachment'] = partnerLogin['fileServiceUrl'] + http['body']['siteContractAttachments'][0]['attachment'].replace('$fileKey$', file_key)
        get_response = test_api_request(partnerLogin_info['partnerUrl'] + http['path'], http['method'], partnerLogin_info['partner_oauth_header'], http['body'])
        if ifItemInKeysAndValueNotNone('siteId', expect['responseitemcheck']):
            expect['responseitemcheck']['siteId'] = paid_siteId
        commonResponseAssert(get_response, expect)

        if ifItemInKeysAndValueNotNone('aftercaseaction', expect):
            afterCaseActionAndAssert(partnerLogin_info['partnerUrl'], partnerLogin_info['partner_oauth_header'], get_response, expect)

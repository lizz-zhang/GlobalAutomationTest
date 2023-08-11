import pytest
import allure
import os
from autoUtils.assertFactory import commonResponseAssert
from autoUtils.requestFactory import test_api_request, test_api_basic_auth_request
from autoUtils.ymlLib import ReadFile
from autoUtils.manage_global_data import ManageGlobalData


basedir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))))
fileName = basedir + '\\testCases\\apiTestData\\global\\routeserver\\' + os.path.basename(__file__).split('.')[0] + '.yml'
readfile = ReadFile(fileName)
cases, parameters = readfile.get_businessTests_data()

@allure.feature('get site')
class TestGetSite:
    @pytest.mark.parametrize('case, http, expect', list(parameters), ids=cases)
    @pytest.mark.globaltest
    @pytest.mark.kyle
    @pytest.mark.routeserver
    @pytest.mark.smoke
    def test_get_site(self, case, http, expect, login):
        login_info = login
        global_data = ManageGlobalData()
        environment = global_data.get_global_value()
        site_id = ManageGlobalData().get_site_id()
        get_response = test_api_request(login_info['routeserverUrl'] + http['path'].replace('$siteId$', str(site_id)), http['method'], login_info['commonHeader'],
                                        None)
        commonResponseAssert(get_response, expect)


import pytest
import allure
import os
from autoUtils.assertFactory import commonResponseAssert
from autoUtils.requestFactory import test_api_request
from autoUtils.ymlLib import ReadFile
from autoUtils.manage_global_data import ManageGlobalData


basedir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))))
fileName = basedir + '\\testCases\\apiTestData\\global\\platformapi\\' + os.path.basename(__file__).split('.')[0] + '.yml'
readfile = ReadFile(fileName)
cases, parameters = readfile.get_businessTests_data()


@allure.feature('check eamil existed')
class TestCheckEmailExisted:
    @pytest.mark.parametrize('case, http, expect', list(parameters), ids=cases)
    @pytest.mark.globaltest
    @pytest.mark.kyle
    @pytest.mark.platformapi
    @pytest.mark.smoke
    def test_get_agents(self, case, http, expect, login):
        login_info = login
        global_data = ManageGlobalData()
        environment = global_data.get_global_value()
        site_email = ManageGlobalData().get_agent_email()
        header = {'Authorization': "apikey EBB97B32-60FE-4DE9-861E-40D0C2299D54"}
        get_response = test_api_request(login_info['apiUrl'] + http['path'].replace('$email$', str(site_email)), http['method'], header,
                                        None)
        commonResponseAssert(get_response, expect)
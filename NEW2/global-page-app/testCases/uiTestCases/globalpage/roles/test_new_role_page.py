from testCases.uiPages.globalpage.roles.new_role_page import (
    NewRolePage,
)
import pytest
import allure

@allure.feature("globalpage_new_role_page")
class TestNewRolePage:
    @pytest.fixture(scope="function")
    def init_page(self, login, page):
        new_role_page = NewRolePage(page)
        new_role_page.goto(
            prefix=login["dash_ui_url"], path=new_role_page.path, suffix=f""
        )
        return new_role_page

    @allure.story("new_role_page_check_title")
    @pytest.mark.smoke
    @pytest.mark.globalpage
    def test_new_role_page_check_title(self, init_page):
        init_page.check_both_titles("New Role")
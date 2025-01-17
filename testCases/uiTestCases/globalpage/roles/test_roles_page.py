from testCases.uiPages.globalpage.roles.roles_page import (
    RolesPage,
)
import pytest
import allure

@allure.feature("globalpage_roles_page")
class TestRolesPage:
    @pytest.fixture(scope="function")
    def init_page(self, login, page):
        roles_page = RolesPage(page)
        roles_page.goto(
            prefix=login["dash_ui_url"], path=roles_page.path, suffix=f""
        )
        return roles_page

    @allure.story("roles_page_check_title")
    @pytest.mark.smoke
    @pytest.mark.globalpage
    def test_roles_page_check_title(self, init_page):
        init_page.check_both_titles("Roles")
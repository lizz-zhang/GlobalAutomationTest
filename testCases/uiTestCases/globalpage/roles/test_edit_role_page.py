from testCases.uiPages.globalpage.roles.edit_role_page import (
    EditRolePage,
)
import pytest
import allure

@allure.feature("globalpage_edit_role_page")
class TestEditRolePage:
    @pytest.fixture(scope="function")
    def init_page(self, login, create_role, page):
        id = create_role.json()["id"]

        edit_role_page = EditRolePage(page)
        edit_role_page.goto(
            prefix=login["dash_ui_url"], path=edit_role_page.path, suffix=f"?roleid="+id
        )
        return edit_role_page

    @allure.story("edit_role_page_check_title")
    @pytest.mark.smoke
    @pytest.mark.globalpage
    def test_edit_role_page_check_title(self, init_page):
        init_page.check_both_titles("Edit Role")
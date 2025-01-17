from testCases.uiPages.globalpage.departments.new_department_page import (
    NewDepartmentsPage,
)
import pytest
import allure

@allure.feature("globalpage_new_department_page")
class TestNewDepartmentsPage:
    @pytest.fixture(scope="function")
    def init_page(self, login, page):
        new_department_page = NewDepartmentsPage(page)
        new_department_page.goto(
            prefix=login["dash_ui_url"], path=new_department_page.path, suffix=f""
        )
        return new_department_page

    @allure.story("new_department_page_check_title")
    @pytest.mark.smoke
    @pytest.mark.globalpage
    def test_new_department_page_check_title(self, init_page):
        init_page.check_both_titles("New Department")
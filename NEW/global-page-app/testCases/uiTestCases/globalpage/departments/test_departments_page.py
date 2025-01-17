from testCases.uiPages.globalpage.departments.departments_page import (
    DepartmentsPage,
)
import pytest
import allure

@allure.feature("globalpage_departments_page")
class TestDepartmentsPage:
    @pytest.fixture(scope="function")
    def init_page(self, login, page):
        departments_page = DepartmentsPage(page)
        departments_page.goto(
            prefix=login["dash_ui_url"], path=departments_page.path, suffix=f""
        )
        return departments_page

    @allure.story("departments_page_check_title")
    @pytest.mark.smoke
    @pytest.mark.globalpage
    def test_departments_page_check_title(self, init_page):
        init_page.check_both_titles("Departments")
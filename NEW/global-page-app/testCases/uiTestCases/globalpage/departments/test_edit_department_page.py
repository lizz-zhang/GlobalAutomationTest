from testCases.uiPages.globalpage.departments.edit_department_page import (
    EditDepartmentsPage,
)
import pytest
import allure

@allure.feature("globalpage_edit_department_page")
class TestEditDepartmentsPage:
    @pytest.fixture(scope="function")
    def init_page(self, login, create_department, page):
        id = create_department.json()["id"]

        edit_department_page = EditDepartmentsPage(page)
        edit_department_page.goto(
            prefix=login["dash_ui_url"], path=edit_department_page.path, suffix=f"?departmentid="+id
        )
        return edit_department_page

    @allure.story("edit_department_page_check_title")
    @pytest.mark.smoke
    @pytest.mark.globalpage
    def test_edit_department_page_check_title(self, init_page):
        init_page.check_both_titles("Edit Department")
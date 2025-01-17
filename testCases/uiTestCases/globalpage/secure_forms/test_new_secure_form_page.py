from testCases.uiPages.globalpage.secure_forms.new_secure_form_page import (
    NewSecureFormPage,
)
import pytest
import allure

@allure.feature("globalpage_new_secure_form_page")
class TestNewSecureFormPage:
    @pytest.fixture(scope="function")
    def init_page(self, login, page):
        new_secure_form_page = NewSecureFormPage(page)
        new_secure_form_page.goto(
            prefix=login["dash_ui_url"], path=new_secure_form_page.path, suffix=f""
        )
        return new_secure_form_page

    @allure.story("new_secure_form_page_check_title")
    @pytest.mark.smoke
    @pytest.mark.globalpage
    def test_new_secure_form_page_check_title(self, init_page):
        init_page.check_both_titles("New Secure Form")
from testCases.uiPages.globalpage.secure_forms.secure_forms_page import (
    SecureFormsPage,
)
import pytest
import allure

@allure.feature("globalpage_secure_forms_page")
class TestSecureFormsPage:
    @pytest.fixture(scope="function")
    def init_page(self, login, page):
        secure_forms_page = SecureFormsPage(page)
        secure_forms_page.goto(
            prefix=login["dash_ui_url"], path=secure_forms_page.path, suffix=f""
        )
        return secure_forms_page

    @allure.story("secure_forms_page_check_title")
    @pytest.mark.smoke
    @pytest.mark.globalpage
    def test_secure_forms_page_check_title(self, init_page):
        init_page.check_both_titles("Secure Forms")
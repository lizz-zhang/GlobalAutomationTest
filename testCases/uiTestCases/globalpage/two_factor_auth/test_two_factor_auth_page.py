from testCases.uiPages.globalpage.two_factor_auth.two_factor_auth_page import (
    TwoFactorAuthenticationPage,
)
import pytest
import allure

@allure.feature("globalpage_two_factor_auth_page")
class TestTwoFactorAuthenticationPage:
    @pytest.fixture(scope="function")
    def init_page(self, login, page):
        two_factor_auth_page = TwoFactorAuthenticationPage(page)
        two_factor_auth_page.goto(
            prefix=login["dash_ui_url"], path=two_factor_auth_page.path, suffix=f""
        )
        return two_factor_auth_page

    @allure.story("two_factor_auth_page_check_title")
    @pytest.mark.smoke
    @pytest.mark.globalpage
    def test_two_factor_auth_page_check_title(self, init_page):
        init_page.check_both_titles("Two-Factor Authentication")
from testCases.uiPages.login.dash_sign_in_with_sso.dash_sign_in_with_sso_page import (
    DashSignInWithSSOPage,
)
import pytest
import allure

@allure.feature("globalpage_dash_sign_in_with_sso_page")
class TestDashSignInWithSSOPage:
    @pytest.fixture(scope="function")
    def init_page(self, login, page):
        dash_sign_in_with_sso_page = DashSignInWithSSOPage(page)
        dash_sign_in_with_sso_page.goto(
            prefix=login["dash_ui_url"], path=dash_sign_in_with_sso_page.path, suffix=f""
        )
        return dash_sign_in_with_sso_page

    @allure.story("dash_sign_in_with_sso_page_check_title")
    @pytest.mark.smoke
    @pytest.mark.globalpage
    def test_dash_sign_in_with_sso_page_check_title(self, init_page):
        init_page.check_both_titles("Sign in with SSO")
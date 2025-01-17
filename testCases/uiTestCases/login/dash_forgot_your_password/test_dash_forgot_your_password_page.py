from testCases.uiPages.login.dash_forgot_your_password.dash_forgot_your_password_page import (
    DashForgotYourPasswordPage,
)
import pytest
import allure

@allure.feature("login_dash_forgot_your_password_page")
class TestDashForgotYourPasswordPage:
    @pytest.fixture(scope="function")
    def init_page(self, login, page):
        dash_forgot_your_password_page = DashForgotYourPasswordPage(page)
        dash_forgot_your_password_page.goto(
            prefix=login["dash_ui_url"], path=dash_forgot_your_password_page.path, suffix=f""
        )
        return dash_forgot_your_password_page

    @allure.story("dash_forgot_your_password_page_check_title")
    @pytest.mark.smoke
    @pytest.mark.login
    def test_dash_forgot_your_password_page_check_title(self, init_page):
        init_page.check_both_titles("Forgot your password?")
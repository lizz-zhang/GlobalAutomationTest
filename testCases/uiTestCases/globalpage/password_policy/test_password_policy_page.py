from testCases.uiPages.globalpage.password_policy.password_policy_page import (
    PasswordPolicyPage,
)
import pytest
import allure

@allure.feature("globalpage_password_policy_page")
class TestPasswordPolicyPage:
    @pytest.fixture(scope="function")
    def init_page(self, login, page):
        password_policy_page = PasswordPolicyPage(page)
        password_policy_page.goto(
            prefix=login["dash_ui_url"], path=password_policy_page.path, suffix=f""
        )
        return password_policy_page

    @allure.story("password_policy_page_check_title")
    @pytest.mark.smoke
    @pytest.mark.globalpage
    def test_password_policy_page_check_title(self, init_page):
        init_page.check_both_titles("Password Policy")
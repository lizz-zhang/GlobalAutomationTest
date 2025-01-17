from testCases.uiPages.login.dash_sign_in.dash_sign_in_page import DashSignInPage
from playwright.sync_api import expect
import re
import pytest
import allure


@allure.feature("login_dash_sign_in_page")
class TestDashSignInPage:
    @allure.story("dash_sign_in_page_check_title")
    @pytest.mark.smoke
    def test_dash_sign_in_page_check_title(self, page, login):
        dash_sign_in_page = DashSignInPage(page)
        dash_sign_in_page.goto(prefix=login["dash_url"], path=dash_sign_in_page.path, suffix="")

        expect(page).to_have_title("Comm100 User Sign In")

    @allure.story("dash_sign_in_with_empty_email_password")
    def test_dash_sign_in_with_empty_email_password(self, page, login):
        dash_sign_in_page = DashSignInPage(page)
        dash_sign_in_page.goto(prefix=login["dash_url"], path=dash_sign_in_page.path, suffix="")

        dash_sign_in_page.dash_sign_in_with_empty_email_password()

        expect(page.get_by_text("Email cannot be empty.")).to_be_visible()

    @allure.story("dash_sign_in_with_valid_email_password")
    @pytest.mark.smoke
    def test_dash_sign_in_with_valid_email_password(self, page, login):
        dash_sign_in_page = DashSignInPage(page)
        dash_sign_in_page.goto(prefix=login["dash_url"], path=dash_sign_in_page.path, suffix="")

        dash_sign_in_page.dash_sign_in_with_email_password(
            email=login["user_data"]["email"], password=login["user_data"]["password"]
        )

        page.wait_for_url(re.compile("dashboard"))
        expect(page).to_have_title("Dashboard", timeout=20000)

    @pytest.mark.parametrize(
        "email, password",
        [("henry@x2.com", "invalid_password"), ("invalid@comm100.com", "Aa000000")],
    )
    @allure.story("dash_sign_in_with_invalid_email_password")
    def test_dash_sign_in_with_invalid_email_password(self, page, login, email, password):
        dash_sign_in_page = DashSignInPage(page)
        dash_sign_in_page.goto(prefix=login["dash_url"], path=dash_sign_in_page.path, suffix="")

        dash_sign_in_page.dash_sign_in_with_email_password(email, password)

        expect(page.get_by_role("alert")).to_be_visible()
        expect(page.get_by_text("Email or password is incorrect.")).to_be_visible()

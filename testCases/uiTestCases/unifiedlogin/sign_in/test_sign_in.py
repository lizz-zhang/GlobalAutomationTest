from testCases.uiPages.exampleapp.sign_in.sign_in_page import SignInPage
from playwright.sync_api import expect
import re
import pytest
import allure


@allure.feature("exampleapp_sign_in_page")
class TestSignInPage:
    @allure.story("sign_in_page_check_title")
    @pytest.mark.smoke
    def test_check_title(self, page, login):
        sign_in_page = SignInPage(page)
        sign_in_page.goto(prefix=login["dash_url"], path=sign_in_page.path, suffix="")

        expect(page).to_have_title("Comm100 User Sign In")

    @allure.story("sign_in_with_empty_email_password")
    def test_sign_in_with_empty_email_password(self, page, login):
        sign_in_page = SignInPage(page)
        sign_in_page.goto(prefix=login["dash_url"], path=sign_in_page.path, suffix="")

        sign_in_page.sign_in_with_empty_email_password()

        expect(page.get_by_text("Email cannot be empty.")).to_be_visible()

    @allure.story("sign_in_with_valid_email_password")
    @pytest.mark.smoke
    def test_sign_in_with_valid_email_password(self, page, login):
        sign_in_page = SignInPage(page)
        sign_in_page.goto(prefix=login["dash_url"], path=sign_in_page.path, suffix="")

        sign_in_page.sign_in_with_email_password(
            email=login["user_data"]["email"], password=login["user_data"]["password"]
        )

        page.wait_for_url(re.compile("dashboard"))
        expect(page).to_have_title("Dashboard", timeout=20000)

    @pytest.mark.parametrize(
        "email, password",
        [("henry@x2.com", "invalid_password"), ("invalid@comm100.com", "Aa000000")],
    )
    @allure.story("sign_in_with_invalid_email_password")
    def test_sign_in_with_invalid_email_password(self, page, login, email, password):
        sign_in_page = SignInPage(page)
        sign_in_page.goto(prefix=login["dash_url"], path=sign_in_page.path, suffix="")

        sign_in_page.sign_in_with_email_password(email, password)

        expect(page.get_by_role("alert")).to_be_visible()
        expect(page.get_by_text("Email or password is incorrect.")).to_be_visible()

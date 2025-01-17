from testCases.uiPages.billing.billing_profile.billing_profile_page import (
    BillingProfilePage,
)
import pytest
import allure

@allure.feature("billing_billing_profile_page")
class TestBillingProfilePage:
    @pytest.fixture(scope="function")
    def init_page(self, login, page):
        billing_profile_page = BillingProfilePage(page)
        billing_profile_page.goto(
            prefix=login["dash_ui_url"], path=billing_profile_page.path, suffix=f""
        )
        return billing_profile_page

    @allure.story("billing_profile_page_check_title")
    @pytest.mark.smoke
    @pytest.mark.billing
    def test_billing_profile_page_check_title(self, init_page):
        init_page.check_both_titles("Billing Profile")
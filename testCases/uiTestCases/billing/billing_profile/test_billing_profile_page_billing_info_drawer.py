from testCases.uiPages.billing.billing_profile.billing_profile_page import (
    BillingProfilePage,
)
from testCases.uiPages.billing.billing_profile.billing_profile_page_billing_info_drawer import (
    BillingProfilePageBillingInfoDrawer,
)

import pytest
import allure


@allure.feature("billing_billing_profile_page_billing_info_drawer")
class TestBillingProfilePageBillingInfoDrawer:
    @pytest.fixture(scope="function")
    def init_page(self, login, page):
        billing_profile_page = BillingProfilePage(page)
        billing_profile_page.goto(
            prefix=login["dash_ui_url"],
            path=billing_profile_page.path,
        )
        return billing_profile_page

    @pytest.fixture(scope="function")
    def init_drawer(self, page, init_page):
        init_page.open_billing_info_drawer()
        billing_profile_page_billing_info_drawer = BillingProfilePageBillingInfoDrawer(page)

        return billing_profile_page_billing_info_drawer

    @allure.story("billing_profile_page_billing_info_drawer_check_title")
    @pytest.mark.smoke
    def test_billing_profile_page_billing_info_drawer_check_title(self, init_drawer):
        init_drawer.check_both_titles("Billing Info")
 
    @allure.story("billing_profile_page_billing_info_drawer_cancel")
    def test_billing_profile_page_billing_info_drawer_cancel(self, init_drawer):
        init_drawer.cancel()

        init_drawer.check_page_title("Billing Profile")
 
    @allure.story("billing_profile_page_billing_info_drawer_close")
    def test_billing_profile_page_billing_info_drawer_close(self, init_drawer):
        init_drawer.close_drawer()

        init_drawer.check_page_title("Billing Profile")
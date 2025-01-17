from testCases.uiPages.globalpage.subscriptions.subscriptions_page import (
    SubscriptionsPage,
)
import pytest
import allure

@allure.feature("globalpage_subscriptions_page")
class TestSubscriptionsPage:
    @pytest.fixture(scope="function")
    def init_page(self, login, page):
        subscriptions_page = SubscriptionsPage(page)
        subscriptions_page.goto(
            prefix=login["dash_ui_url"], path=subscriptions_page.path, suffix=f""
        )
        return subscriptions_page

    @allure.story("subscriptions_page_check_title")
    @pytest.mark.smoke
    @pytest.mark.globalpage
    def test_subscriptions_page_check_title(self, init_page):
        init_page.check_both_titles("Subscriptions")
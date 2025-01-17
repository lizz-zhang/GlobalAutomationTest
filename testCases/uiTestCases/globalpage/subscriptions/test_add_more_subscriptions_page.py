from testCases.uiPages.globalpage.subscriptions.add_more_subscriptions_page import (
    AddMoreSubscriptionsPage,
)
import pytest
import allure

@allure.feature("globalpage_add_more_subscriptions_page")
class TestAddMoreSubscriptionsPage:
    @pytest.fixture(scope="function")
    def init_page(self, login, page):
        add_more_subscriptions_page = AddMoreSubscriptionsPage(page)
        add_more_subscriptions_page.goto(
            prefix=login["dash_ui_url"], path=add_more_subscriptions_page.path, suffix=f""
        )
        return add_more_subscriptions_page

    @allure.story("add_more_subscriptions_page_check_title")
    @pytest.mark.smoke
    @pytest.mark.globalpage
    def test_add_more_subscriptions_page_check_title(self, init_page):
        init_page.check_both_titles("Add More Subscriptions")
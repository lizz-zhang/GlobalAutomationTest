import pdb
import re
import pytest
import allure

from autoUtils.uiCommonAssertion import check_both_titles, check_not_visible, check_page_title, check_visible
from testCases.uiPages.bot_portal_dashboard import BotPortalDashboardPage


@allure.feature("Bot-Portal Dashboard page")
class TestBotPortalDashboardPage:
    @pytest.fixture(scope="function")
    def init_page(self, login, page):
        dashboard_page = BotPortalDashboardPage(page)
        dashboard_page.goto(
            prefix=login["dash_ui_url"], path=dashboard_page.path, suffix=""
        )
        return dashboard_page

    @allure.story("check_bot_portal_dashboard_page_element")
    def test_bot_portal_dashboard_page_items(self, init_page):
        check_both_titles(init_page, "Dashboard")
        elements = [
            init_page.chatbot_in_livechat_button,
            init_page.chatbot_in_ticket_button,
            init_page.new_tips,
            init_page.last_7_days
        ]
        check_visible(elements)
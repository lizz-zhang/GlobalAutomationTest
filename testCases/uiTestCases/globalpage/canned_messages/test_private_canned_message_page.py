from testCases.uiPages.globalpage.canned_messages.private_canned_message_page import (
    PrivateCannedMessagePage,
)
import pytest
import allure

@allure.feature("globalpage_private_canned_messages_page")
class TestPrivateCannedMessagePage:
    @pytest.fixture(scope="function")
    def init_page(self, login, page):
        private_canned_messages_page = PrivateCannedMessagePage(page)
        private_canned_messages_page.goto(
            prefix=login["dash_ui_url"], path=private_canned_messages_page.path, suffix=f""
        )
        return private_canned_messages_page

    @allure.story("private_canned_messages_page_check_title")
    @pytest.mark.smoke
    @pytest.mark.globalpage
    def test_private_canned_messages_page_check_title(self, init_page):
        init_page.check_both_titles("Private Canned Messages")
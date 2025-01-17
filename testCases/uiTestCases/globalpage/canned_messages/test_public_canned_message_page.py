from testCases.uiPages.globalpage.canned_messages.public_canned_message_page import (
    PublicCannedMessagePage,
)
import pytest
import allure

@allure.feature("globalpage_public_canned_messages_page")
class TestPublicCannedMessagePage:
    @pytest.fixture(scope="function")
    def init_page(self, login, page):
        public_canned_messages_page = PublicCannedMessagePage(page)
        public_canned_messages_page.goto(
            prefix=login["dash_ui_url"], path=public_canned_messages_page.path, suffix=f""
        )
        return public_canned_messages_page

    @allure.story("public_canned_messages_page_check_title")
    @pytest.mark.smoke
    @pytest.mark.globalpage
    def test_public_canned_messages_page_check_title(self, init_page):
        init_page.check_both_titles("Public Canned Messages")
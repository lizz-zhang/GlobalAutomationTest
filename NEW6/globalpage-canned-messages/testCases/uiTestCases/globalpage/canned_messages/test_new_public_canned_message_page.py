from testCases.uiPages.globalpage.canned_messages.new_public_canned_message_page import (
    NewPublicCannedMessagePage,
)
import pytest
import allure

@allure.feature("globalpage_new_public_canned_message_page")
class TestNewPublicCannedMessagePage:
    @pytest.fixture(scope="function")
    def init_page(self, login, page):
        new_public_canned_message_page = NewPublicCannedMessagePage(page)
        new_public_canned_message_page.goto(
            prefix=login["dash_ui_url"], path=new_public_canned_message_page.path, suffix=f""
        )
        return new_public_canned_message_page  

    @allure.story("new_public_canned_message_page_check_title")
    @pytest.mark.smoke
    @pytest.mark.globalpage
    def test_new_public_canned_message_page_check_title(self, init_page):
        init_page.check_both_titles("New Public Canned Message")
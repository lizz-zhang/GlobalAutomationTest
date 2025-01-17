from testCases.uiPages.globalpage.canned_messages.new_private_canned_message_page import (
    NewPrivateCannedMessagePage,
)
import pytest
import allure

@allure.feature("globalpage_new_private_canned_message_page")
class TestNewPrivateCannedMessagePage:
    @pytest.fixture(scope="function")
    def init_page(self, login, page):
        new_private_canned_message_page = NewPrivateCannedMessagePage(page)
        new_private_canned_message_page.goto(
            prefix=login["dash_ui_url"], path=new_private_canned_message_page.path, suffix=f""
        )
        return new_private_canned_message_page  

    @allure.story("new_private_canned_message_page_check_title")
    @pytest.mark.smoke
    @pytest.mark.globalpage
    def test_new_private_canned_message_page_check_title(self, init_page):
        init_page.check_both_titles("New Private Canned Message")
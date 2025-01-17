from testCases.uiPages.globalpage.private_canned_messages.edit_private_canned_message_page import (
    EditPrivateCannedMessagePage,
)
import pytest
import allure

@allure.feature("globalpage_edit_private_canned_message_page")
class TestEditPrivateCannedMessagePage:
    @pytest.fixture(scope="function")
    def init_page(self, login, create_private_canned_message, page):
        id = create_private_canned_message.json()["id"]

        edit_private_canned_message_page = EditPrivateCannedMessagePage(page)
        edit_private_canned_message_page.goto(
            prefix=login["dash_ui_url"], path=edit_private_canned_message_page.path, suffix=f"?privatecannedmessageid="+id
        )
        return edit_private_canned_message_page

    @allure.story("edit_private_canned_message_page_check_title")
    @pytest.mark.smoke
    @pytest.mark.globalpage
    def test_edit_private_canned_message_page_check_title(self, init_page):
        init_page.check_both_titles("Edit Private Canned Message")
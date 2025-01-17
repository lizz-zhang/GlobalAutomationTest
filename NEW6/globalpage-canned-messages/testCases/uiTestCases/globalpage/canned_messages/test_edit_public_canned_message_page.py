from testCases.uiPages.globalpage.canned_messages.edit_public_canned_message_page import (
    EditPublicCannedMessagePage,
)
import pytest
import allure

@allure.feature("globalpage_edit_public_canned_message_page")
class TestEditPublicCannedMessagePage:
    @pytest.fixture(scope="function")
    def init_page(self, login, create_public_canned_message, page):
        id = create_public_canned_message.json()["id"]

        edit_public_canned_message_page = EditPublicCannedMessagePage(page)
        edit_public_canned_message_page.goto(
            prefix=login["dash_ui_url"], path=edit_public_canned_message_page.path, suffix=f"?publiccannedmessageid="+id
        )
        return edit_public_canned_message_page

    @allure.story("edit_public_canned_message_page_check_title")
    @pytest.mark.smoke
    @pytest.mark.globalpage
    def test_edit_public_canned_message_page_check_title(self, init_page):
        init_page.check_both_titles("Edit Public Canned Message")
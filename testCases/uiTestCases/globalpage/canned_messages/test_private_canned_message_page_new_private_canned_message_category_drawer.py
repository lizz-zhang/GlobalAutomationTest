from testCases.uiPages.globalpage.canned_messages.private_canned_message_page import (
        PrivateCannedMessagePage,
)
from testCases.uiPages.globalpage.canned_messages.private_canned_message_page_new_private_canned_message_category_drawer import (
    PrivateCannedMessagePageNewPrivateCannedMessageCategoryDrawer,
)

import pytest
import allure


@allure.feature("globalpage_private_canned_message_page_new_private_canned_message_category_drawer")
class TestPrivateCannedMessagePageNewPrivateCannedMessageCategoryDrawer:
    @pytest.fixture(scope="function")
    def init_page(self, login, page):
        private_canned_message_page = PrivateCannedMessagePage(page)
        private_canned_message_page.goto(
            prefix=login["dash_ui_url"],
            path=private_canned_message_page.path,
        )
        return private_canned_message_page

    @pytest.fixture(scope="function")
    def init_drawer(self, page, init_page):
        init_page.open_edit_private_canned_message_category_drawer()
        private_canned_message_page_new_private_canned_message_category_drawer = PrivateCannedMessagePageNewPrivateCannedMessageCategoryDrawer(page)

        return private_canned_message_page_new_private_canned_message_category_drawer

    @allure.story("private_canned_message_page_new_private_canned_message_category_drawer_check_title")
    @pytest.mark.smoke
    def test_private_canned_message_page_new_private_canned_message_category_drawer_check_title(self, init_drawer):
        init_drawer.check_both_titles("New Private Canned Message Category")
 
    @allure.story("private_canned_message_page_new_private_canned_message_category_drawer_cancel")
    def test_private_canned_message_page_new_private_canned_message_category_drawer_cancel(self, init_drawer):
        init_drawer.cancel()

        init_drawer.check_page_title("Canned Messages")

    @allure.story("private_canned_message_page_new_private_canned_message_category_drawer_close")
    def test_private_canned_message_page_new_private_canned_message_category_drawer_close(self, init_drawer):
        init_drawer.close_drawer()

        init_drawer.check_page_title("Canned Messages")
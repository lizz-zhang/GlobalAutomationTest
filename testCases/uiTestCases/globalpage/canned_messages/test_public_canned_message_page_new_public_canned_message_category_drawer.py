from testCases.uiPages.globalpage.canned_messages.public_canned_message_page import (
        PublicCannedMessagePage,
)
from testCases.uiPages.globalpage.canned_messages.public_canned_message_page_new_public_canned_message_category_drawer import (
    PublicCannedMessagePageNewPublicCannedMessageCategoryDrawer,
)

import pytest
import allure


@allure.feature("globalpage_public_canned_message_page_new_public_canned_message_category_drawer")
class TestPublicCannedMessagePageNewPublicCannedMessageCategoryDrawer:
    @pytest.fixture(scope="function")
    def init_page(self, login, page):
        public_canned_message_page = PublicCannedMessagePage(page)
        public_canned_message_page.goto(
            prefix=login["dash_ui_url"],
            path=public_canned_message_page.path,
        )
        return public_canned_message_page

    @pytest.fixture(scope="function")
    def init_drawer(self, page, init_page):
        init_page.open_edit_public_canned_message_category_drawer()
        public_canned_message_page_new_public_canned_message_category_drawer = PublicCannedMessagePageNewPublicCannedMessageCategoryDrawer(page)

        return public_canned_message_page_new_public_canned_message_category_drawer

    @allure.story("public_canned_message_page_new_public_canned_message_category_drawer_check_title")
    @pytest.mark.smoke
    def test_public_canned_message_page_new_public_canned_message_category_drawer_check_title(self, init_drawer):
        init_drawer.check_both_titles("New Public Canned Message Category")
 
    @allure.story("public_canned_message_page_new_public_canned_message_category_drawer_cancel")
    def test_public_canned_message_page_new_public_canned_message_category_drawer_cancel(self, init_drawer):
        init_drawer.cancel()

        init_drawer.check_page_title("Canned Messages")

    @allure.story("public_canned_message_page_new_public_canned_message_category_drawer_close")
    def test_public_canned_message_page_new_public_canned_message_category_drawer_close(self, init_drawer):
        init_drawer.close_drawer()

        init_drawer.check_page_title("Canned Messages")
from testCases.uiPages.module_name.menu_name.edit_banned_ip_page import (
    EditBannedIPPage,
)
import pytest
import allure

@pytest.fixture
def init_page():
    page = EditBannedIPPage(page="edit_banned_ip")
    page.navigate_to_page()
    return page

@allure.feature("Edit Banned IP Page")
class TestEditBannedIPPage:
    @allure.story("Check Page Title")
    def test_edit_banned_ip_page_check_title(self, init_page):
        assert init_page.get_title() == "Expected Title"  # Replace with the actual expected title
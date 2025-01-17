from uiPages.base_page import BasePage

class EditBannedIPPage(BasePage):
    def __init__(self, page):
        super().__init__(page)
        self.path = "/livechat/settings/banlist/bannedip/edit"

from uiPages.base_page import BasePage

class CookieRestrictionPage(BasePage):
    def __init__(self, page):
        super().__init__(page)
        self.path = "/livechat/settings/cookierestriction/"

from testCases.uiPages.module_name.menu_name.edit_banned_ip_page import EditBannedIPPage
import pytest
import allure

@pytest.fixture
def init_page():
    page = EditBannedIPPage("edit_banned_ip")
    page.navigate()
    return page

def test_edit_banned_ip_page_check_title(init_page):
    assert init_page.get_title() == "Edit Banned IP"

from testCases.uiPages.module_name.menu_name.cookie_restriction_page import CookieRestrictionPage
import pytest
import allure

@pytest.fixture
def init_page():
    page = CookieRestrictionPage("cookie_restriction")
    page.navigate()
    return page

def test_cookie_restriction_page_check_title(init_page):
    assert init_page.get_title() == "Cookie Restriction"
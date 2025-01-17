from testCases.uiPages.module_name.menu_name.cookie_restriction_page import (
    CookieRestrictionPage,
)
import pytest
import allure

@pytest.fixture
def init_page():
    page = CookieRestrictionPage("cookie_restriction")
    page.navigate()
    return page

@allure.feature("Cookie Restriction Page")
class TestCookieRestrictionPage:
    @allure.story("Check Page Title")
    def test_cookie_restriction_page_check_title(self, init_page):
        assert init_page.get_title() == "Expected Title"  # Replace with the actual expected title
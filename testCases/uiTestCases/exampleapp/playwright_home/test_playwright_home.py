from testCases.uiPages.exampleapp.playwright_home.playwright_home_page import (
    PlaywrightHomePage,
)
from playwright.sync_api import expect
import re
import pytest
import allure


@allure.feature("exampleapp_playwright_home_page")
class TestPlaywrightSanityPage:
    @pytest.mark.smoke
    @allure.story("check_title")
    def test_check_title(self, page):
        playwright_home_page = PlaywrightHomePage(page)

        expect(page).to_have_title(re.compile("Playwright"))

    @allure.story("click_get_started_link")
    def test_click_get_started_link(self, page):
        playwright_home_page = PlaywrightHomePage(page)
        playwright_home_page.click_get_started_link()

        expect(page).to_have_title(re.compile(r"Installation"))
        expect(page.get_by_role("heading", name="Installation")).to_be_visible()

from testCases.uiPages.exampleapp.playwright_home.playwright_home_example_page import (
    PlaywrightHomeExamplePage,
)
from playwright.sync_api import expect
import re
import pytest
import allure


@allure.feature("playwright_home_page")
class TestPlaywrightHomePage:
    @pytest.mark.smoke
    @allure.story("playwright_home_page_check_title")
    def test_check_title(self, page):
        playwright_home_page = PlaywrightHomeExamplePage(page)

        expect(page).to_have_title(re.compile("Playwright"))

    @allure.story("playwright_home_page_click_get_started_link")
    def test_click_get_started_link(self, page):
        playwright_home_page = PlaywrightHomeExamplePage(page)
        playwright_home_page.click_get_started_link()

        expect(page).to_have_title(re.compile(r"Installation"))
        expect(page.get_by_role("heading", name="Installation")).to_be_visible()

from testCases.uiPages.exampleapp.playwright_home.playwright_home_example_page import (
    PlaywrightHomeExamplePage,
)
from playwright.sync_api import expect
import re


def test_check_title(page):
    playwright_home_page = PlaywrightHomeExamplePage(page)

    expect(page).to_have_title(re.compile("Playwright"))


def test_click_get_started_link(page):
    playwright_home_page = PlaywrightHomeExamplePage(page)
    playwright_home_page.click_get_started_link()

    expect(page).to_have_title(re.compile(r"Installation"))
    expect(page.get_by_role("heading", name="Installation")).to_be_visible()

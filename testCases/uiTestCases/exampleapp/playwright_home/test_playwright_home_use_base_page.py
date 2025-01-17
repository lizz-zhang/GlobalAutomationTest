from testCases.uiPages.exampleapp.playwright_home.playwright_home_page_use_base_page import (
    PlaywrightHomePage,
)
from playwright.sync_api import expect
import re


def test_click_get_started_link(page):
    playwright_home_page = PlaywrightHomePage(page)
    playwright_home_page.click_get_started_link()

    expect(page).to_have_title(re.compile(r"Installation"))
    expect(page.get_by_role("heading", name="Installation")).to_be_visible()

    # page.wait_for_element_visible("h1", timeout=10000)
    # assert page.get_text("h1") == "Installation"
    # page.take_screenshot("get_started_link.png")

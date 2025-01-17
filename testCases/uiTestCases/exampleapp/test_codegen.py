import re
from playwright.sync_api import Page, expect
from time import sleep


def test_codegen(page: Page) -> None:
    page.goto("https://demo.playwright.dev/todomvc/")
    page.goto("https://demo.playwright.dev/todomvc/#/")
    page.get_by_placeholder("What needs to be done?").click()
    page.get_by_placeholder("What needs to be done?").fill("buy milk")
    page.get_by_placeholder("What needs to be done?").press("Enter")
    sleep(5)

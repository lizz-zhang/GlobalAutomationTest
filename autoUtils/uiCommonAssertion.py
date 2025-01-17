# -*- coding: utf-8 -*-
"""
======================
@author:nash
@time:12/31/2024 14:18:23 PM
@email:nash.xiang@comm100.com
======================
"""

from playwright.sync_api import Page, expect

def check_both_titles(page: Page, title: str):
    expect(page.page).to_have_title(title)
    expect(page.function_title).to_have_text(title)

def check_page_title(page: Page, title: str):
    expect(page.page).to_have_title(title)

def check_function_title(page: Page, title: str):
    expect(page.function_title).to_have_text(title)

def check_visible(elements):
    """used for checking if a specific element is visible."""
    for element in elements:
        expect(element).to_be_visible()

def check_not_visible(elements):
    for element in elements:
        expect(element).not_to_be_visible()

def check_feature_switched_on(page: Page):
    expect(page.feature_switch).to_be_checked()
    expect(page.feature_enable_message).to_be_visible()

def check_feature_switched_off(page: Page):
    expect(page.feature_switch).not_to_be_checked()
    expect(page.feature_disable_message).to_be_visible()

def check_change_saved(page: Page):
    """used for 1. save changes on the same page 2. save when you edit an entity."""
    expect(page.save_success_message).to_be_visible()

def check_change_cancelled(page: Page):
    """used for cancel changes on the same page."""
    expect(page.cancel_button).to_be_disabled()

def check_no_records(page: Page):
    expect(page.no_records_text).to_be_visible()

def goto(page: Page, url: str):
    page.page.goto(url)

def refresh(page: Page):
    """Refresh the current page."""
    page.page.reload()

def wait_for_element_visible(page: Page, selector: str, timeout: int = 30000):
    """Wait for an element to be visible."""
    page.page.wait_for_selector(selector, state="visible", timeout=timeout)

def wait_for_element_clickable(page: Page, selector: str, timeout: int = 30000):
    """Wait for an element to be clickable."""
    element = page.page.wait_for_selector(
        selector, state="visible", timeout=timeout
    )
    expect(element).to_be_enabled()

def click(page: Page, selector: str):
    """Click an element."""
    # page.wait_for_element_clickable(selector)
    page.page.click(selector)

def fill(page: Page, selector: str, text: str):
    """Fill an input field with text."""
    page.wait_for_element_visible(selector)
    page.page.fill(selector, text)

def get_text(page: Page, selector: str) -> str:
    """Get text from an element."""
    page.wait_for_element_visible(selector)
    return page.inner_text(selector)

def take_screenshot(page: Page, path: str):
    """Take a screenshot of the current page."""
    page.page.screenshot(path=path)

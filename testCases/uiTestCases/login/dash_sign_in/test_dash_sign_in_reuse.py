import re
from playwright.sync_api import Page, expect, sync_playwright
from playwright.async_api import async_playwright


def test_dash_sign_in_reuse(browser_context, page: Page):
    page.goto("https://livechat3dash.testing.comm100dev.io/login")

    page.locator('input[name="email"]').fill("mj@livechat3.com")
    page.locator('input[name="password"]').fill("Aa00000000")
    page.get_by_role("button", name="Sign in").click()

    page.wait_for_url(re.compile("dashboard"))
    expect(page).to_have_title("Dashboard", timeout=20000)

    # Save storage state into the file.

    # save the state to the root directory\playwright\.auth\state.json file

    storage = browser_context.storage_state(path="playwright/.auth/state.json")
    print(storage)

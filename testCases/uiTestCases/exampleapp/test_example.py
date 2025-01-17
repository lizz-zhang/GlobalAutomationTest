import re
from playwright.sync_api import Page, expect, sync_playwright
from playwright.async_api import async_playwright


def test_has_title(page: Page):
    page.goto("https://playwright.dev/")

    # Expect a title "to contain" a substring.
    expect(page).to_have_title(re.compile("Playwright"))


def test_get_started_link(page: Page):
    page.goto("https://playwright.dev/")

    # Click the get started link.
    page.get_by_role("link", name="Get started").click()

    # Expects page to have a heading with the name of Installation.
    expect(page.get_by_role("heading", name="Installation")).to_be_visible()


async def test_has_title2(page: Page):

    async with async_playwright() as p:
        browser = await p.chromium.launch(
            headless=False, devtools=True
        )  # Run in headful mode
        context = browser.new_context(java_script_enabled=False)  # Disable JavaScript
        page = await context.new_page()
        try:
            await page.goto("https://www.comm100.com/", timeout=60000)
            print(page.title())
        except Exception as e:
            print(f"Error encountered: {e}")
        finally:
            await browser.close()

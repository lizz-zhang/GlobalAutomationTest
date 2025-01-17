# from uiPages.base_page import BasePage


class PlaywrightHomeExamplePage:
    def __init__(self, page):
        self.page = page
        self.page.goto("https://playwright.dev/")

        self.get_started_link = self.page.get_by_role("link", name="Get started")

    # def goto(self):
    #     self.page.goto("https://playwright.dev/")

    # def has_title(self):
    #     self.goto(self.url)
    #     self.page.expect_title().to_match("Playwright")

    def click_get_started_link(self):
        self.get_started_link.click()

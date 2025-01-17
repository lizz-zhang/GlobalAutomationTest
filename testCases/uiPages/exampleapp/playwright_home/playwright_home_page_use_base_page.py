from uiPages.base_page import BasePage


class PlaywrightHomePage(BasePage):
    def __init__(self, page):
        super().__init__(page)
        self.url = "https://playwright.dev/"
        self.get_started_link = page.get_by_role("link", name="Get started")

    # def goto(self):
    #     self.page.goto("https://playwright.dev/")

    # def has_title(self):
    #     self.goto(self.url)
    #     self.page.expect_title().to_match("Playwright")

    def click_get_started_link(self):
        self.goto(self.url)
        # self.click(self.get_started_link)
        self.get_started_link.click()

        # self.page.get_by_role("heading", name="Installation").expect_to_be_visible()

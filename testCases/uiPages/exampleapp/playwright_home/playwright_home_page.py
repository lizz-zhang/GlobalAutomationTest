class PlaywrightHomePage:
    def __init__(self, page):
        self.page = page
        self.page.goto("https://playwright.dev/")

        self.get_started_link = self.page.get_by_role("link", name="Get started")

    def click_get_started_link(self):
        self.get_started_link.click()

from playwright.sync_api import Page, expect
from uiPages.base_page import BasePage
import re


class BaseDrawer(BasePage):
    def __init__(self, page: Page):
        super().__init__(page)
        self.page = page

        # The following are common elements for a drawer. Please note what BasePage has is not listed here.
        self.function_title = self.page.get_by_role("heading")

        self.close_button = self.page.get_by_role("button", name="Close")

    # The following are common action functions for a drawer. Please note what BasePage has is not listed here, such as Cancel action.
    def close_drawer(self):
        self.close_button.click()

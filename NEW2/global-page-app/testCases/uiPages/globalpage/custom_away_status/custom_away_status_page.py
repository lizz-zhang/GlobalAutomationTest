from uiPages.base_page import BasePage

class CustomAwayStatusPage(BasePage):
    def __init__(self, page):
        super().__init__(page)
        self.path = "/global/people/customawaystatus/"
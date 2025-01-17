from uiPages.base_page import BasePage

class NewAwayStatusPage(BasePage):
    def __init__(self, page):
        super().__init__(page)
        self.path = "/global/people/customawaystatus/new"
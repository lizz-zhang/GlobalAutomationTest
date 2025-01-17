from uiPages.base_page import BasePage

class EditOAuthClientPage(BasePage):
    def __init__(self, page):
        super().__init__(page)
        self.path = "/global/security/apitoken/edit"
from uiPages.base_page import BasePage

class NewSecureFormPage(BasePage):
    def __init__(self, page):
        super().__init__(page)
        self.path = "/global/security/secureforms/new"
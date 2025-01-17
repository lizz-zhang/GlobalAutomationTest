from uiPages.base_page import BasePage

class DashSignInWithSSOPage(BasePage):
    def __init__(self, page):
        super().__init__(page)
        self.path = "/login/sso"
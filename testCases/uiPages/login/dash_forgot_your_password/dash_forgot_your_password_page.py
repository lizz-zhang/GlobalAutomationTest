from uiPages.base_page import BasePage

class DashForgotYourPasswordPage(BasePage):
    def __init__(self, page):
        super().__init__(page)
        self.path = "/login/forgotpassword"
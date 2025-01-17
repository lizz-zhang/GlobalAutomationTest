from uiPages.base_page import BasePage

class TwoFactorAuthenticationPage(BasePage):
    def __init__(self, page):
        super().__init__(page)
        self.path = "/global/security/twofactorauth/"
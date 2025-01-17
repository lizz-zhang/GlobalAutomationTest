from uiPages.base_page import BasePage

class CookieRestrictionPage(BasePage):
    def __init__(self, page):
        super().__init__(page)
        self.path = "/livechat/settings/cookierestriction/"
from uiPages.base_page import BasePage

class EditBannedIPPage(BasePage):
    def __init__(self, page):
        super().__init__(page)
        self.path = "/livechat/settings/banlist/bannedip/edit"
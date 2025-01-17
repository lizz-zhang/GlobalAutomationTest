from uiPages.base_page import BasePage

class NewPrivateCannedMessagePage(BasePage):
    def __init__(self, page):
        super().__init__(page)
        self.path = "/global/cannedmessages/privatecannedmessage/new"
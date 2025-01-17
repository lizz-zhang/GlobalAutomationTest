from uiPages.base_page import BasePage

class EditPrivateCannedMessagePage(BasePage):
    def __init__(self, page):
        super().__init__(page)
        self.path = "/global/cannedmessages/privatecannedmessage/edit"
from uiPages.base_page import BasePage

class EditCustomSMTPServerPage(BasePage):
    def __init__(self, page):
        super().__init__(page)
        self.path = "/global/site/customSmtpServers/edit"
from uiPages.base_page import BasePage

class NewCustomSMTPServerPage(BasePage):
    def __init__(self, page):
        super().__init__(page)
        self.path = "/global/site/customSmtpServers/new"
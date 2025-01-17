from uiPages.base_page import BasePage

class AddMoreSubscriptionsPage(BasePage):
    def __init__(self, page):
        super().__init__(page)
        self.path = "/global/subscriptions/addmore/"
from uiPages.base_page import BasePage

class EditAgentPage(BasePage):
    def __init__(self, page):
        super().__init__(page)
        self.path = "/global/people/agents/edit"
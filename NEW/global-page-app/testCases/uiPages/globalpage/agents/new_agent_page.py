from uiPages.base_page import BasePage

class NewAgentPage(BasePage):
    def __init__(self, page):
        super().__init__(page)
        self.path = "/global/people/agents/new"
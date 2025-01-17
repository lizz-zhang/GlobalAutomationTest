from uiPages.base_page import BasePage

class EditRolePage(BasePage):
    def __init__(self, page):
        super().__init__(page)
        self.path = "/global/people/roles/edit"
from uiPages.base_page import BasePage

class EditDepartmentsPage(BasePage):
    def __init__(self, page):
        super().__init__(page)
        self.path = "/global/people/departments/edit"
from uiPages.base_page import BasePage

class EditSkillPage(BasePage):
    def __init__(self, page):
        super().__init__(page)
        self.path = "/global/people/skills/edit"
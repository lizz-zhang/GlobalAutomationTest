from testCases.uiPages.globalpage.skills.new_skill_page import (
    NewSkillPage,
)
import pytest
import allure

@allure.feature("globalpage_new_skill_page")
class TestNewSkillPage:
    @pytest.fixture(scope="function")
    def init_page(self, login, page):
        new_skill_page = NewSkillPage(page)
        new_skill_page.goto(
            prefix=login["dash_ui_url"], path=new_skill_page.path, suffix=f""
        )
        return new_skill_page  

    @allure.story("new_skill_page_check_title")
    @pytest.mark.smoke
    @pytest.mark.globalpage
    def test_new_skill_page_check_title(self, init_page):
        init_page.check_both_titles("New Skill")
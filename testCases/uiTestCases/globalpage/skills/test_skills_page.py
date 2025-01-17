from testCases.uiPages.globalpage.skills.skills_page import (
    SkillsPage,
)
import pytest
import allure

@allure.feature("globalpage_skills_page")
class TestSkillsPage:
    @pytest.fixture(scope="function")
    def init_page(self, login, page):
        skills_page = SkillsPage(page)
        skills_page.goto(
            prefix=login["dash_ui_url"], path=skills_page.path, suffix=f""
        )
        return skills_page

    @allure.story("skills_page_check_title")
    @pytest.mark.smoke
    @pytest.mark.globalpage
    def test_skills_page_check_title(self, init_page):
        init_page.check_both_titles("Skills")
from testCases.uiPages.globalpage.skills.edit_skill_page import (
    EditSkillPage,
)
import pytest
import allure

@allure.feature("globalpage_edit_skill_page")
class TestEditSkillPage:
    @pytest.fixture(scope="function")
    def init_page(self, login, create_skill_id, page):
        id = create_skill_id.json()["id"]

        edit_skill_page = EditSkillPage(page)
        edit_skill_page.goto(
            prefix=login["dash_ui_url"], path=edit_skill_page.path, suffix=f"?skillid="+id
        )
        return edit_skill_page

    @allure.story("edit_skill_page_check_title")
    @pytest.mark.smoke
    @pytest.mark.globalpage
    def test_edit_skill_page_check_title(self, init_page):
        init_page.check_both_titles("Edit Skill")
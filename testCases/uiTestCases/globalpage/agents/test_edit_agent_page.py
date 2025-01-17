from testCases.uiPages.globalpage.agents.edit_agent_page import (
    EditAgentPage,
)
import pytest
import allure

@allure.feature("globalpage_edit_agent_page")
class TestEditAgentPage:
    @pytest.fixture(scope="function")
    def init_page(self, login, create_agent_id, page):
        id = create_agent_id.json()["id"]

        edit_agent_page = EditAgentPage(page)
        edit_agent_page.goto(
            prefix=login["dash_ui_url"], path=edit_agent_page.path, suffix=f"?agentid="+id
        )
        return edit_agent_page

    @allure.story("edit_agent_page_check_title")
    @pytest.mark.smoke
    @pytest.mark.globalpage
    def test_edit_agent_page_check_title(self, init_page):
        init_page.check_both_titles("Edit Agent")
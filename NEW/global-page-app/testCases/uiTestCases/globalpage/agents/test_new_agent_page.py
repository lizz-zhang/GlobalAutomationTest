from testCases.uiPages.globalpage.agents.new_agent_page import (
    NewAgentPage,
)
import pytest
import allure

@allure.feature("globalpage_new_agent_page")
class TestNewAgentPage:
    @pytest.fixture(scope="function")
    def init_page(self, login, page):
        new_agent_page = NewAgentPage(page)
        new_agent_page.goto(
            prefix=login["dash_ui_url"], path=new_agent_page.path, suffix=f""
        )
        return new_agent_page

    @allure.story("new_agent_page_check_title")
    @pytest.mark.smoke
    @pytest.mark.globalpage
    def test_new_agent_page_check_title(self, init_page):
        init_page.check_both_titles("New Agent")
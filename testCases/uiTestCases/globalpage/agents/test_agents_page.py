from testCases.uiPages.globalpage.agents.agents_page import (
    AgentsPage,
)
import pytest
import allure

@allure.feature("globalpage_agents_page")
class TestAgentsPage:
    @pytest.fixture(scope="function")
    def init_page(self, login, page):
        agents_page = AgentsPage(page)
        agents_page.goto(
            prefix=login["dash_ui_url"], path=agents_page.path, suffix=f""
        )
        return agents_page

    @allure.story("agents_page_check_title")
    @pytest.mark.smoke
    @pytest.mark.globalpage
    def test_agents_page_check_title(self, init_page):
        init_page.check_both_titles("Agents")
from testCases.uiPages.globalpage.agent_single_sign_on.agent_single_sign_on_page import (
    AgentSingleSignOnPage,
)
import pytest
import allure

@allure.feature("globalpage_agent_single_sign_on_page")
class TestAgentSingleSignOnPage:
    @pytest.fixture(scope="function")
    def init_page(self, login, page):
        agent_single_sign_on_page = AgentSingleSignOnPage(page)
        agent_single_sign_on_page.goto(
            prefix=login["dash_ui_url"], path=agent_single_sign_on_page.path, suffix=f""
        )
        return agent_single_sign_on_page

    @allure.story("agent_single_sign_on_page_check_title")
    @pytest.mark.smoke
    @pytest.mark.globalpage
    def test_agent_single_sign_on_page_check_title(self, init_page):
        init_page.check_both_titles("Agent Single Sign-On")
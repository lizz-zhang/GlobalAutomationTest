from testCases.uiPages.globalpage.agent_chats.agent_chats_page import (
    AgentChatsPage,
)
import pytest
import allure

@allure.feature("globalpage_agent_chats_page")
class TestAgentChatsPage:
    @pytest.fixture(scope="function")
    def init_page(self, login, page):
        agent_chats_page = AgentChatsPage(page)
        agent_chats_page.goto(
            prefix=login["dash_ui_url"], path=agent_chats_page.path, suffix=f""
        )
        return agent_chats_page

    @allure.story("agent_chats_page_check_title")
    @pytest.mark.smoke
    @pytest.mark.globalpage
    def test_agent_chats_page_check_title(self, init_page):
        init_page.check_both_titles("Agent Chats")
from testCases.uiPages.globalpage.agent_chats.agent_chats_page import (
    AgentChatsPage,
)
from testCases.uiPages.globalpage.agent_chats.agent_chats_page_agent_chats_details_drawer import (
    AgentChatsPageAgentChatDetailsDrawer,
)

import pytest
import allure


@allure.feature("globalpage_agent_chats_page_agent_chats_details_drawer")
class TestAgentChatsPageAgentChatDetailsDrawer:
    @pytest.fixture(scope="function")
    def init_page(self, login, page):
        agent_chats_page = AgentChatsPage(page)
        agent_chats_page.goto(
            prefix=login["dash_ui_url"],
            path=agent_chats_page.path,
        )
        return agent_chats_page

    @pytest.fixture(scope="function")
    def init_drawer(self, page, init_page):
        init_page.open_agent_chats_details_drawer()
        agent_chats_page_agent_chats_details_drawer = AgentChatsPageAgentChatDetailsDrawer(page)

        return agent_chats_page_agent_chats_details_drawer

    @allure.story("agent_chats_page_agent_chats_details_drawer_check_title")
    @pytest.mark.smoke
    def test_agent_chats_page_agent_chats_details_drawer_check_title(self, init_drawer):
        init_drawer.check_both_titles("Agent Chat Details")

    @allure.story("agent_chats_page_agent_chats_details_drawer_close")
    def test_agent_chats_page_agent_chats_details_drawer_close(self, init_drawer):
        init_drawer.close_drawer()

        init_drawer.check_page_title("Agent Chats")
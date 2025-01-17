from testCases.uiPages.globalpage.agents.edit_agent_page import (
    EditAgentPage,
)
from testCases.uiPages.globalpage.agents.edit_agent_page_change_avatar_drawer import (
    EditAgentPageChangeAvatardDrawer,
)

import pytest
import allure


@allure.feature("globalpage_edit_agent_page_change_avatar_drawer")
class TestEditAgentPageChangeAvatardDrawer:
    @pytest.fixture(scope="function")
    def init_page(self, login, page, init_agents):
        id = init_agents.json()["agentid"]
        edit_agent_page = EditAgentPage(page)
        edit_agent_page.goto(
            prefix=login["dash_ui_url"],
            path=edit_agent_page.path,
            suffix=f"?agentid={id}",
        )
        return edit_agent_page

    @pytest.fixture(scope="function")
    def init_drawer(self, page, init_page):
        init_page.open_change_avatar_drawer()
        edit_agent_page_change_avatar_drawer = EditAgentPageChangeAvatardDrawer(page)

        return edit_agent_page_change_avatar_drawer

    @allure.story("edit_agent_page_change_avatar_drawer_check_title")
    @pytest.mark.smoke
    def test_edit_agent_page_change_avatar_drawer_check_title(self, init_drawer):
        init_drawer.check_both_titles("Change Avatar")

    @allure.story("edit_agent_page_change_avatar_drawer_cancel")
    def test_edit_agent_page_change_avatar_drawer_cancel(self, init_drawer):
        init_drawer.cancel()

        init_drawer.check_page_title("Edit Agent")

    @allure.story("edit_agent_page_change_avatar_drawer_close")
    def test_edit_agent_page_change_avatar_drawer_close(self, init_drawer):
        init_drawer.close_drawer()

        init_drawer.check_page_title("Edit Agent")
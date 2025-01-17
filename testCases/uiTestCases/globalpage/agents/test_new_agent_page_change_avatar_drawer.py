from testCases.uiPages.globalpage.agents.new_agent_page import (
    NewAgentPage,
)
from testCases.uiPages.globalpage.agents.new_agent_page_change_avatar_drawer import (
    NewAgentPageChangeAvatardDrawer,
)

import pytest
import allure


@allure.feature("globalpage_new_agent_page_change_avatar_drawer")
class TestNewAgentPageChangeAvatardDrawer:
    @pytest.fixture(scope="function")
    def init_page(self, login, page):
        new_agent_page = NewAgentPage(page)
        new_agent_page.goto(
            prefix=login["dash_ui_url"],
            path=new_agent_page.path,
        )
        return new_agent_page

    @pytest.fixture(scope="function")
    def init_drawer(self, page, init_page):
        init_page.open_change_avatar_drawer()
        new_agent_page_change_avatar_drawer = NewAgentPageChangeAvatardDrawer(page)

        return new_agent_page_change_avatar_drawer

    @allure.story("new_agent_page_change_avatar_drawer_check_title")
    @pytest.mark.smoke
    def test_new_agent_page_change_avatar_drawer_check_title(self, init_drawer):
        init_drawer.check_both_titles("Change Avatar")

    @allure.story("new_agent_page_change_avatar_drawer_cancel")
    def test_new_agent_page_change_avatar_drawer_cancel(self, init_drawer):
        init_drawer.cancel()

        init_drawer.check_page_title("New Agent")

    @allure.story("new_agent_page_change_avatar_drawer_close")
    def test_new_agent_page_change_avatar_drawer_close(self, init_drawer):
        init_drawer.close_drawer()

        init_drawer.check_page_title("New Agent")

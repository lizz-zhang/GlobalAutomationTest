from testCases.uiPages.globalpage.agents.agents_page import (
    AgentsPage,
)
from testCases.uiPages.globalpage.agents.agents_page_reset_password_drawer import (
    AgentsPageResetPasswordDrawer,
)

import pytest
import allure


@allure.feature("globalpage_agents_page_reset_password_drawer")
class TestAgentsPageResetPasswordDrawer:
    @pytest.fixture(scope="function")
    def init_page(self, login, page):
        agents_page = AgentsPage(page)
        agents_page.goto(
            prefix=login["dash_ui_url"],
            path=agents_page.path,
        )
        return agents_page

    @pytest.fixture(scope="function")
    def init_drawer(self, page, init_page):
        init_page.open_reset_password_drawer()
        agents_page_reset_password_drawer = AgentsPageResetPasswordDrawer(page)

        return agents_page_reset_password_drawer

    @allure.story("agents_page_reset_password_drawer_check_title")
    @pytest.mark.smoke
    def test_agents_page_reset_password_drawer_check_title(self, init_drawer):
        init_drawer.check_both_titles("Reset Password")

    @allure.story("agents_page_reset_password_drawer_cancel")
    def test_agents_page_reset_password_drawer_cancel(self, init_drawer):
        init_drawer.cancel()

        init_drawer.check_page_title("Agents")

    @allure.story("agents_page_reset_password_drawer_close")
    def test_agents_page_reset_password_drawer_close(self, init_drawer):
        init_drawer.close_drawer()

        init_drawer.check_page_title("Agents")
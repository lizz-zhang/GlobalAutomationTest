from testCases.uiPages.globalpage.roles.roles_page import (
    RolesPage,
)
from testCases.uiPages.globalpage.roles.roles_page_agent_role_permission_settings_drawer import (
    RolesPageAgentRolePermissionSettingsDrawer,
)

import pytest
import allure


@allure.feature("globalpage_roles_page_agent_role_permission_settings_drawer")
class TestRolesPageAgentRolePermissionSettingsDrawer:
    @pytest.fixture(scope="function")
    def init_page(self, login, page):
        roles_page = RolesPage(page)
        roles_page.goto(
            prefix=login["dash_ui_url"],
            path=roles_page.path,
        )
        return roles_page

    @pytest.fixture(scope="function")
    def init_drawer(self, page, init_page):
        init_page.open_agent_role_permission_settings_drawer()
        roles_page_agent_role_permission_settings_drawer = RolesPageAgentRolePermissionSettingsDrawer(page)

        return roles_page_agent_role_permission_settings_drawer

    @allure.story("roles_page_agent_role_permission_settings_drawer_check_title")
    @pytest.mark.smoke
    def test_roles_page_agent_role_permission_settings_drawer_check_title(self, init_drawer):
        init_drawer.check_both_titles("Permission Settings of Agent Role")

    @allure.story("roles_page_agent_role_permission_settings_drawer_cancel")
    def test_roles_page_agent_role_permission_settings_drawer_cancel(self, init_drawer):
        init_drawer.cancel()

        init_drawer.check_page_title("Roles")

    @allure.story("roles_page_agent_role_permission_settings_drawer_close")
    def test_roles_page_agent_role_permission_settings_drawer_close(self, init_drawer):
        init_drawer.close_drawer()

        init_drawer.check_page_title("Roles")
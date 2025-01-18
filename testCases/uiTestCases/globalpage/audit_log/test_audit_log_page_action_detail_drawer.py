from testCases.uiPages.globalpage.audit_log.audit_log_page import (
    AuditLogPage,
)
from testCases.uiPages.globalpage.audit_log.audit_log_page_action_detail_drawer import (
    AuditLogPageActionDetailDrawer,
)

import pytest
import allure


@allure.feature("globalpage_audit_log_page_action_detail_drawer")
class TestAuditLogPageActionDetailDrawer:
    @pytest.fixture(scope="function")
    def init_page(self, login, page):
        audit_log_page = AuditLogPage(page)
        audit_log_page.goto(
            prefix=login["dash_ui_url"],
            path=audit_log_page.path,
        )
        return audit_log_page

    @pytest.fixture(scope="function")
    def init_drawer(self, page, init_page):
        init_page.open_agent_chat_details_drawer()
        audit_log_page_action_detail_drawer = AuditLogPageActionDetailDrawer(page)

        return audit_log_page_action_detail_drawer

    @allure.story("audit_log_page_action_detail_drawer_check_title")
    @pytest.mark.smoke
    def test_audit_log_page_action_detail_drawer_check_title(self, init_drawer):
        init_drawer.check_both_titles("Action Detail")

    @allure.story("audit_log_page_action_detail_drawer_close")
    def test_audit_log_page_action_detail_drawer_close(self, init_drawer):
        init_drawer.close_drawer()

        init_drawer.check_page_title("Audit Log")
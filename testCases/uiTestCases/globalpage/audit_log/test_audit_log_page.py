from testCases.uiPages.globalpage.audit_log.audit_log_page import (
    AuditLogPage,
)
import pytest
import allure

@allure.feature("globalpage_audit_log_page")
class TestAuditLogPage:
    @pytest.fixture(scope="function")
    def init_page(self, login, page):
        audit_log_page = AuditLogPage(page)
        audit_log_page.goto(
            prefix=login["dash_ui_url"], path=audit_log_page.path, suffix=f""
        )
        return audit_log_page

    @allure.story("audit_log_page_check_title")
    @pytest.mark.smoke
    @pytest.mark.globalpage
    def test_audit_log_page_check_title(self, init_page):
        init_page.check_both_titles("Audit Log")
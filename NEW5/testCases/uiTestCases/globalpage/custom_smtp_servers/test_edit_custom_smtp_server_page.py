from testCases.uiPages.globalpage.custom_smtp_servers.edit_custom_smtp_server_page import (
    EditCustomSMTPServerPage,
)
import pytest
import allure

@allure.feature("globalpage_edit_custom_smtp_server_page")
class TestEditCustomSMTPServerPage:
    @pytest.fixture(scope="function")
    def init_page(self, login, create_custom_smtp_server, page):
        id = create_custom_smtp_server.json()["id"]

        edit_custom_smtp_server_page = EditCustomSMTPServerPage(page)
        edit_custom_smtp_server_page.goto(
            prefix=login["dash_ui_url"], path=edit_custom_smtp_server_page.path, suffix=f"?customsmtpserverid="+id
        )
        return edit_custom_smtp_server_page

    @allure.story("edit_custom_smtp_server_page_check_title")
    @pytest.mark.smoke
    @pytest.mark.globalpage
    def test_edit_custom_smtp_server_page_check_title(self, init_page):
        init_page.check_both_titles("Edit Custom SMTP Server")
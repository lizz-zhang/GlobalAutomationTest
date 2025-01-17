from testCases.uiPages.globalpage.custom_smtp_servers.new_custom_smtp_server_page import (
    NewCustomSMTPServerPage,
)
import pytest
import allure

@allure.feature("globalpage_new_custom_smtp_server_page")
class TestNewCustomSMTPServerPage:
    @pytest.fixture(scope="function")
    def init_page(self, login, page):
        new_custom_smtp_server_page = NewCustomSMTPServerPage(page)
        new_custom_smtp_server_page.goto(
            prefix=login["dash_ui_url"], path=new_custom_smtp_server_page.path, suffix=f""
        )
        return new_custom_smtp_server_page

    @allure.story("new_custom_smtp_server_page_check_title")
    @pytest.mark.smoke
    @pytest.mark.globalpage
    def test_new_custom_smtp_server_page_check_title(self, init_page):
        init_page.check_both_titles("New Custom SMTP Server")
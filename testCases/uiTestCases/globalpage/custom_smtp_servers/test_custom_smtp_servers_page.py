from testCases.uiPages.globalpage.custom_smtp_servers.custom_smtp_servers_page import (
    CustomSMTPServersPage,
)
import pytest
import allure

@allure.feature("globalpage_custom_smtp_servers_page")
class TestCustomSMTPServersPage:
    @pytest.fixture(scope="function")
    def init_page(self, login, page):
        custom_smtp_servers_page = CustomSMTPServersPage(page)
        custom_smtp_servers_page.goto(
            prefix=login["dash_ui_url"], path=custom_smtp_servers_page.path, suffix=f""
        )
        return custom_smtp_servers_page

    @allure.story("custom_smtp_servers_page_check_title")
    @pytest.mark.smoke
    @pytest.mark.globalpage
    def test_custom_smtp_servers_page_check_title(self, init_page):
        init_page.check_both_titles("Custom SMTP Servers")
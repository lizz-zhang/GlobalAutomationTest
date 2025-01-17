from testCases.uiPages.globalpage.oauth_client.new_oauth_client_page import (
    NewOAuthClientPage,
)
import pytest
import allure

@allure.feature("globalpage_new_oauth_client_page")
class TestNewOAuthClientPage:
    @pytest.fixture(scope="function")
    def init_page(self, login, page):
        new_oauth_client_page = NewOAuthClientPage(page)
        new_oauth_client_page.goto(
            prefix=login["dash_ui_url"], path=new_oauth_client_page.path, suffix=f""
        )
        return new_oauth_client_page

    @allure.story("new_oauth_client_page_check_title")
    @pytest.mark.smoke
    @pytest.mark.globalpage
    def test_new_oauth_client_page_check_title(self, init_page):
        init_page.check_both_titles("New OAuth Client")
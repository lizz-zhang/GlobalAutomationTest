from testCases.uiPages.globalpage.oauth_client.oauth_client_page import (
    OAuthClientPage,
)
import pytest
import allure

@allure.feature("globalpage_oauth_client_page")
class TestOAuthClientPage:
    @pytest.fixture(scope="function")
    def init_page(self, login, page):
        oauth_client_page = OAuthClientPage(page)
        oauth_client_page.goto(
            prefix=login["dash_ui_url"], path=oauth_client_page.path, suffix=f""
        )
        return oauth_client_page

    @allure.story("oauth_client_page_check_title")
    @pytest.mark.smoke
    @pytest.mark.globalpage
    def test_oauth_client_page_check_title(self, init_page):
        init_page.check_both_titles("OAuth Client")
from testCases.uiPages.globalpage.oauth_client.edit_oauth_client_page import (
    EditOAuthClientPage,
)
import pytest
import allure

@allure.feature("globalpage_edit_oauth_client_page")
class TestEditOAuthClientPage:
    @pytest.fixture(scope="function")
    def init_page(self, login, create_oauth_client, page):
        id = create_oauth_client.json()["id"]

        edit_oauth_client_page = EditOAuthClientPage(page)
        edit_oauth_client_page.goto(
            prefix=login["dash_ui_url"], path=edit_oauth_client_page.path, suffix=f"?oauthclientid="+id
        )
        return edit_oauth_client_page

    @allure.story("edit_oauth_client_page_check_title")
    @pytest.mark.smoke
    @pytest.mark.globalpage
    def test_edit_oauth_client_page_check_title(self, init_page):
        init_page.check_both_titles("Edit OAuth Client")
from testCases.uiPages.globalpage.custom_away_status.edit_away_status_page import (
    EditAwayStatusPage,
)
import pytest
import allure

@allure.feature("globalpage_edit_away_status_page")
class TestEditAwayStatusPage:
    @pytest.fixture(scope="function")
    def init_page(self, login, create_away_status, page):
        id = create_away_status.json()["id"]

        edit_away_status_page = EditAwayStatusPage(page)
        edit_away_status_page.goto(
            prefix=login["dash_ui_url"], path=edit_away_status_page.path, suffix=f"?agentawaystatusid="+id
        )
        return edit_away_status_page

    @allure.story("edit_away_status_page_check_title")
    @pytest.mark.smoke
    @pytest.mark.globalpage
    def test_edit_away_status_page_check_title(self, init_page):
        init_page.check_both_titles("Edit Away Status")
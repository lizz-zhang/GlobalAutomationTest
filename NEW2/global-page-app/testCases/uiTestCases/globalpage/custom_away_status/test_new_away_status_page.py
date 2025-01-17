from testCases.uiPages.globalpage.custom_away_status.new_away_status_page import (
    NewAwayStatusPage,
)
import pytest
import allure

@allure.feature("globalpage_new_away_status_page")
class TestNewAwayStatusPage:
    @pytest.fixture(scope="function")
    def init_page(self, login, page):
        new_away_status_page = NewAwayStatusPage(page)
        new_away_status_page.goto(
            prefix=login["dash_ui_url"], path=new_away_status_page.path, suffix=f""
        )
        return new_away_status_page  

    @allure.story("new_away_status_page_check_title")
    @pytest.mark.smoke
    @pytest.mark.globalpage
    def test_new_away_status_page_check_title(self, init_page):
        init_page.check_both_titles("New Away Status")
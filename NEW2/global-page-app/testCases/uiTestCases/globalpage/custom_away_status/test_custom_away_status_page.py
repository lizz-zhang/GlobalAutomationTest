from testCases.uiPages.globalpage.custom_away_status.custom_away_status_page import (
    CustomAwayStatusPage,
)
import pytest
import allure

@allure.feature("globalpage_custom_away_status_page")
class TestCustomAwayStatusPage:
    @pytest.fixture(scope="function")
    def init_page(self, login, page):
        custom_away_status_page = CustomAwayStatusPage(page)
        custom_away_status_page.goto(
            prefix=login["dash_ui_url"], path=custom_away_status_page.path, suffix=f""
        )
        return custom_away_status_page

    @allure.story("custom_away_status_page_check_title")
    @pytest.mark.smoke
    @pytest.mark.globalpage
    def test_custom_away_status_page_check_title(self, init_page):
        init_page.check_both_titles("Custom Away Status")
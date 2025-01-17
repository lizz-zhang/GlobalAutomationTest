from testCases.uiPages.globalpage.site_profile.site_profile_page import (
    SiteProfilePage,
)
import pytest
import allure

@allure.feature("globalpage_site_profile_page")
class TestSiteProfilePage:
    @pytest.fixture(scope="function")
    def init_page(self, login, page):
        site_profile_page = SiteProfilePage(page)
        site_profile_page.goto(
            prefix=login["dash_ui_url"], path=site_profile_page.path, suffix=f""
        )
        return site_profile_page

    @allure.story("site_profile_page_check_title")
    @pytest.mark.smoke
    @pytest.mark.globalpage
    def test_site_profile_page_check_title(self, init_page):
        init_page.check_both_titles("Site Profile")
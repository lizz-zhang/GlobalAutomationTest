from testCases.uiPages.globalpage.secure_forms.new_secure_form_page import (
    NewSecureFormPage,
)
from testCases.uiPages.globalpage.secure_forms.new_secure_form_page_new_field_drawer import (
    NewSecureFormPageNewFieldDrawer,
)

import pytest
import allure


@allure.feature("globalpage_new_secure_form_page_new_field_drawer_drawer")
class TestNewSecureFormPageNewFieldDrawer:
    @pytest.fixture(scope="function")
    def init_page(self, login, page):
        new_secure_form_page = NewSecureFormPage(page)
        new_secure_form_page.goto(
            prefix=login["dash_ui_url"],
            path=new_secure_form_page.path,
        )
        return new_secure_form_page

    @pytest.fixture(scope="function")
    def init_drawer(self, page, init_page):
        init_page.open_new_field_drawer()
        new_secure_form_page_new_field_drawer = NewSecureFormPageNewFieldDrawer(page)

        return new_secure_form_page_new_field_drawer

    @allure.story("new_secure_form_page_new_field_drawer_check_title")
    @pytest.mark.smoke
    def test_new_secure_form_page_new_field_drawer_check_title(self, init_drawer):
        init_drawer.check_both_titles("New Field")

    @allure.story("new_secure_form_page_new_field_drawer_cancel")
    def test_new_secure_form_page_new_field_drawer_cancel(self, init_drawer):
        init_drawer.cancel()

        init_drawer.check_page_title("New Secure Form")

    @allure.story("new_secure_form_page_new_field_drawer_close")
    def test_new_secure_form_page_new_field_drawer_close(self, init_drawer):
        init_drawer.close_drawer()

        init_drawer.check_page_title("New Secure Form")
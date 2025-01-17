from testCases.uiPages.globalpage.secure_forms.edit_secure_form_page import (
    EditSecureFormPage,
)
from testCases.uiPages.globalpage.secure_forms.edit_secure_form_page_new_field_drawer import (
    EditSecureFormPageNewFieldDrawer,
)

import pytest
import allure


@allure.feature("globalpage_edit_secure_form_page_new_field_drawer")
class TestEditSecureFormPageNewFieldDrawer:
    @pytest.fixture(scope="function")
    def init_page(self, login, page):
        edit_secure_form_page = EditSecureFormPage(page)
        edit_secure_form_page.goto(
            prefix=login["dash_ui_url"],
            path=edit_secure_form_page.path,
        )
        return edit_secure_form_page

    @pytest.fixture(scope="function")
    def init_drawer(self, page, init_page):
        init_page.open_new_field_drawer()
        edit_secure_form_page_new_field_drawer = EditSecureFormPageNewFieldDrawer(page)

        return edit_secure_form_page_new_field_drawer

    @allure.story("edit_secure_form_page_new_field_drawer_check_title")
    @pytest.mark.smoke
    def test_edit_secure_form_page_new_field_drawer_check_title(self, init_drawer):
        init_drawer.check_both_titles("New Field")

    @allure.story("edit_secure_form_page_new_field_drawer_cancel")
    def test_edit_secure_form_page_new_field_drawer_cancel(self, init_drawer):
        init_drawer.cancel()

        init_drawer.check_page_title("Edit Secure Form")

    @allure.story("edit_secure_form_page_new_field_drawer_close")
    def test_edit_secure_form_page_new_field_drawer_close(self, init_drawer):
        init_drawer.close_drawer()

        init_drawer.check_page_title("Edit Secure Form")
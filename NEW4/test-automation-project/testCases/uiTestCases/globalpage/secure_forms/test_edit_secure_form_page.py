from testCases.uiPages.globalpage.secure_forms.edit_secure_form_page import (
    EditSecureFormPage,
)
import pytest
import allure

@allure.feature("globalpage_edit_secure_form_page")
class TestEditSecureFormPage:
    @pytest.fixture(scope="function")
    def init_page(self, login, create_secure_form, page):
        id = create_secure_form.json()["id"]

        edit_secure_form_page = EditSecureFormPage(page)
        edit_secure_form_page.goto(
            prefix=login["dash_ui_url"], path=edit_secure_form_page.path, suffix=f"?secureformsid="+id
        )
        return edit_secure_form_page

    @allure.story("edit_secure_form_page_check_title")
    @pytest.mark.smoke
    @pytest.mark.globalpage
    def test_edit_secure_form_page_check_title(self, init_page):
        init_page.check_both_titles("Edit Secure Form")
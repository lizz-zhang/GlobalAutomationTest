from testCases.uiPages.billing.invoices.invoices_page import (
    InvoicesPage,
)
import pytest
import allure

@allure.feature("billing_invoices_page")
class TestInvoicesPage:
    @pytest.fixture(scope="function")
    def init_page(self, login, page):
        invoices_page = InvoicesPage(page)
        invoices_page.goto(
            prefix=login["dash_ui_url"], path=invoices_page.path, suffix=f""
        )
        return invoices_page

    @allure.story("invoices_page_check_title")
    @pytest.mark.smoke
    @pytest.mark.billing
    def test_invoices_page_check_title(self, init_page):
        init_page.check_both_titles("Invoices")
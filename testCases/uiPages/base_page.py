from playwright.sync_api import Page, expect
import re


class BasePage(Page):
    def __init__(self, page: Page):
        super().__init__(page)
        self.page = page

        # the following are common elements for a page
        self.page_title = self.page.title()
        self.function_title = self.page.locator('h3[data-tag="title"]')

        self.feature_switch = self.page.locator(
            'span[data-tag="featureSwitch"] input[type="checkbox"]'
        )

        self.save_button = self.page.get_by_role("button", name="Save")
        self.cancel_button = self.page.get_by_role("button", name="Cancel")
        self.back_button = self.page.get_by_role("button", name="Back")
        self.feature_enable_message = self.page.get_by_text(
            "Feature enabled successfully."
        )
        self.feature_disable_message = self.page.get_by_text(
            "Feature disabled successfully."
        )
        self.save_success_message = self.page.get_by_text("Changes saved successfully.")
        self.no_records_text = self.page.get_by_text("No records found.")

        self.first_edit_button_in_list = self.page.get_by_label("Edit").first
        self.first_delete_button_in_list = self.page.get_by_label("Delete").first
        self.select_all_checkbox = page.get_by_role("row").get_by_role("checkbox").first

        self.delete_confirm_button = self.page.get_by_role("button", name="Delete")
        self.delete_cancel_button = self.page.get_by_role("button", name="Cancel")
    
    def handle_dialog(self, dialog):
        if dialog.type == 'confirm':  # 确保是一个确认框（confirm）
            dialog.accept()  # 点击“是”按钮关闭弹窗 ,也可以通过dialog.dismiss() 来点击“否”
        elif dialog.type == 'alert': #确保是一个警告框（alert)
            dialog.accept() # 点击“是”按钮关闭弹窗
        elif dialog.type == 'prompt': #确保是一个提示框(prompt)
            dialog.accept('Test') #输入文本并点击“确定”,也可以通过dialog.dismiss() 来点击“否”
        else:
            pass
        
    ## the following is common action functions for a page
    def goto(self, prefix: str, path: str, suffix: str = ""):
        url = prefix + path + suffix
        self.page.goto(url)

        # make sure page is loaded
        expect(self.page).not_to_have_title(re.compile(r"Loading"), timeout=30000)
        # make sure the dialog is close.
        # For our system, some window is open but it's not dialog type. So we use the custom code to resolve it first. 
        dialog_div = self.page.locator('[role="dialog"]')
        if dialog_div.is_visible():
            # This locator also work
            # self.page.locator('div[role="dialog"] button')
            self.page.locator('button[aria-label="Close"]').click() 

        # if is the dialog type, then use dialog work flow to close it.
        self.page.on('dialog', self.handle_dialog)      

    def feature_switch_on(self):
        self.feature_switch.check()

    def feature_switch_off(self):
        self.feature_switch.uncheck()

    def save(self):
        self.save_button.click()

    def cancel(self):
        self.cancel_button.click()
    
    def back(self):
        self.back_button.click()
        
    def get_cell_by_name(self, name):
        return self.page.get_by_role("cell", name=name)

    def upload_file(self, file_path):
        self.page.locator('input[type="file"]').set_input_files(file_path)

    ## the following is common check functions for a page

    def check_both_titles(self, title: str):
        # increase timeout to 30s as some page's title might change after page is completely loaded.
        expect(self.page).to_have_title(title, timeout=30000)
        expect(self.function_title).to_have_text(title)

    def check_page_title(self, title: str):
        expect(self.page).to_have_title(title)

    def check_function_title(self, title: str):
        expect(self.function_title).to_have_text(title)

    def check_visible(self, element):
        """used for checking if a specific element is visible."""
        expect(element).to_be_visible()

    def check_feature_switched_on(self):
        expect(self.feature_switch).to_be_checked()
        expect(self.feature_enable_message).to_be_visible()

    def check_feature_switched_off(self):
        expect(self.feature_switch).not_to_be_checked()
        expect(self.feature_disable_message).to_be_visible()

    def check_change_saved(self):
        """used for 1. save changes on the same page 2. save when you edit an entity."""
        expect(self.save_success_message).to_be_visible()

    def check_change_cancelled(self):
        """used for cancel changes on the same page."""
        expect(self.cancel_button).to_be_disabled()

    def check_no_records(self):
        expect(self.no_records_text).to_be_visible()

    # def goto(self, url: str):
    #     self.page.goto(url)

    # def refresh(self):
    #     """Refresh the current page."""
    #     self.page.reload()

    # def wait_for_element_visible(self, selector: str, timeout: int = 30000):
    #     """Wait for an element to be visible."""
    #     self.page.wait_for_selector(selector, state="visible", timeout=timeout)

    # def wait_for_element_clickable(self, selector: str, timeout: int = 30000):
    #     """Wait for an element to be clickable."""
    #     element = self.page.wait_for_selector(
    #         selector, state="visible", timeout=timeout
    #     )
    #     expect(element).to_be_enabled()

    # def click(self, selector: str):
    #     """Click an element."""
    #     # self.wait_for_element_clickable(selector)
    #     self.page.click(selector)

    # def fill(self, selector: str, text: str):
    #     """Fill an input field with text."""
    #     self.wait_for_element_visible(selector)
    #     self.page.fill(selector, text)

    # def get_text(self, selector: str) -> str:
    #     """Get text from an element."""
    #     self.wait_for_element_visible(selector)
    #     return self.page.inner_text(selector)

    # def take_screenshot(self, path: str):
    #     """Take a screenshot of the current page."""
    #     self.page.screenshot(path=path)

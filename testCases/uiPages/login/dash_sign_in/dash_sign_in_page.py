from uiPages.base_page import BasePage


class DashSignInPage(BasePage):
    def __init__(self, page):
        super().__init__(page)
        self.path = "/login"
        # self.page.goto(prefix=prefix, path=self.path, suffix=suffix)

        self.email_input = self.page.locator('input[name="email"]')
        self.password_input = self.page.locator('input[name="password"]')
        self.sign_in_button = self.page.get_by_role("button", name="Sign in")

    # def navigate(self, prefix: str, suffix: str = ""):
    #     self.page.goto(prefix + self.path + suffix)

    def sign_in_with_empty_email_password(self):
        self.sign_in_button.click()

    def sign_in_with_email_password(self, email, password):
        self.email_input.fill(email)
        self.password_input.fill(password)
        self.sign_in_button.click()

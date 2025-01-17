You will be provided a list of {page_name} and other attributes for each page in a table format. Please create the following files in the current workspace based on the provided pages and attributes based on the examples. Please note you need to use the suffix_querystring_key and set_up_fixture attributes when provided.

### Page Object File

**Directory**: `testCases/uiPages/{module_name}/{menu_name}/`
**File Name**: `{page_name}_page.py`
**Content**:

```python
from uiPages.base_page import BasePage

class {PageName}Page(BasePage):
    def __init__(self, page):
        super().__init__(page)
        self.path = "{path}"
```

### Test Case File

**Directory**: `testCases/uiTestCases/{module_name}/{menu_name}/`
**File Name**: `test_{page_name}_page.py`
**Content**:

```python
from testCases.uiPages.{module_name}.{menu_name}.{page_name}_page import (
    {PageName}Page,
)
import pytest
import allure

@allure.feature("{module_name}_{page_name}_page")
class Test{PageName}Page:
    @pytest.fixture(scope="function")
    def init_page(self, login, {set_up_fixture}, page):
        # only when {set_up_fixture} is not empty, then add the following line of code and append the id to the suffix parameter below. Otherwise, ignore it.
        id = {set_up_fixture}.json()["id"]

        {page_name}_page = {PageName}Page(page)
        {page_name}_page.goto(
            prefix=login["dash_ui_url"], path={page_name}_page.path, suffix=f"{suffix_querystring_key}"+id
        )
        return {page_name}_page

    @allure.story("{page_name}_page_check_title")
    @pytest.mark.smoke
    @pytest.mark.login
    def test_{page_name}_page_check_title(self, init_page):
        init_page.check_both_titles("{page_title}")
```

### login

#### login: Dash Sign in with SSO Page

**Page Object File**: [`testCases/uiPages/login/dash_sign_in_with_sso/dash_sign_in_with_sso_page.py`]

```python
from uiPages.base_page import BasePage

class DashSignInWithSSOPage(BasePage):
    def __init__(self, page):
        super().__init__(page)
        self.path = "/login/sso"
```

**Test Case File**: [`testCases/uiTestCases/login/dash_sign_in_with_sso/test_dash_sign_in_with_sso_page.py`]

```python
from testCases.uiPages.login.dash_sign_in_with_sso.dash_sign_in_with_sso_page import (
    DashLoginPage,
)
import pytest
import allure

@allure.feature("login_dash_sign_in_with_sso_page")
class TestDashSignInWithSSOPage:
    @pytest.fixture(scope="function")
    def init_page(self, login, page):
        dash_sign_in_with_sso_page = DashSignInWithSSOPage(page)
        dash_sign_in_with_sso_page.goto(
            prefix=login["dash_ui_url"], path=dash_sign_in_with_sso_page.path, suffix=f""
        )
        return dash_sign_in_with_sso_page

    @allure.story("dash_sign_in_with_sso_page_check_title")
    @pytest.mark.smoke
    @pytest.mark.login
    def test_dash_sign_in_with_sso_page_check_title(self, init_page):
        init_page.check_both_titles("Comm100 Sign in with SSO")
```
#### login: Dash Forgot your password Page

**Page Object File**: [`testCases/uiPages/login/dash_forgot_your_password/dash_forgot_your_password_page.py`]

```python
from uiPages.base_page import BasePage

class DashForgotYourPasswordPage(BasePage):
    def __init__(self, page):
        super().__init__(page)
        self.path = "/login/forgotpassword"
```

**Test Case File**: [`testCases/uiTestCases/login/dash_forgot_your_password/test_dash_forgot_your_password_page.py`]

```python
from testCases.uiPages.login.dash_forgot_your_password.dash_forgot_your_password_page import (
    DashLoginPage,
)
import pytest
import allure

@allure.feature("login_dash_forgot_your_password_page")
class TestDashForgotYourPasswordPage:
    @pytest.fixture(scope="function")
    def init_page(self, login, page):
        dash_forgot_your_password_page = DashForgotYourPasswordPage(page)
        dash_forgot_your_password_page.goto(
            prefix=login["dash_ui_url"], path=dash_forgot_your_password_page.path, suffix=f""
        )
        return dash_forgot_your_password_page

    @allure.story("dash_forgot_your_password_page_check_title")
    @pytest.mark.smoke
    @pytest.mark.login
    def test_dash_forgot_your_password_page_check_title(self, init_page):
        init_page.check_both_titles("Comm100 Forgot your password?")
```

### Hints

1. For {page_title}, if it's empty, please use the value of {page_name}. If it's not empty, please use the value of {page_title}.
2. For {menu_name}, if it's empty, please use the value of {page_name}. If it's not empty, please use the value of {menu_name}. Either way, you need to convert it to snake_case and lower-case.

### This is the List of Pages and Attributes. You need to create the files for these pages.

| module_name  | menu_name | page_name          | page_title | path                                     | suffix_querystring_key | set_up_fixture   |
| ------------ | --------- | ------------------ | ---------- | ---------------------------------------- | ---------------------- | ---------------- |
| login | dash Sign in with SSO | Sign in with SSO |   | /login/sso  |       |                  |
| login | dash Forgot your password |Forgot your password?|  | /login/forgotpassword  |   |   |
 
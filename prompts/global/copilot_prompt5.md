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
    @pytest.mark.globalpage
    def test_{page_name}_page_check_title(self, init_page):
        init_page.check_both_titles("{page_title}")
```

### GlobalPage


#### GlobalPage: Password Policy Page

**Page Object File**: [`testCases/uiPages/globalpage/password_policy/password_policy_page.py`]

```python
from uiPages.base_page import BasePage

class PasswordPolicyPage(BasePage):
    def __init__(self, page):
        super().__init__(page)
        self.path = "/global/security/sitepasswordpolicy/"
```

**Test Case File**: [`testCases/uiTestCases/globalpage/password_policy/password_policy_page.py`]

```python
from testCases.uiPages.globalpage.password_policy.password_policy_page import (
    PasswordPolicyPage,
)
import pytest
import allure

@allure.feature("globalpage_password_policy_page")
class TestPasswordPolicyPage:
    @pytest.fixture(scope="function")
    def init_page(self, login, page):
        password_policy_page = PasswordPolicyPage(page)
        password_policy_page.goto(
            prefix=login["dash_ui_url"], path=password_policy_page.path, suffix=f""
        )
        return password_policy_page

    @allure.story("password_policy_page_check_title")
    @pytest.mark.smoke
    @pytest.mark.globalpage
    def test_password_policy_page_check_title(self, init_page):
        init_page.check_both_titles("Password Policy")
```
#### GlobalPage: Two-Factor Authentication Page

**Page Object File**: [`testCases/uiPages/globalpage/two_factor_auth/two_factor_auth_page.py`]

```python
from uiPages.base_page import BasePage

class TwoFactorAuthenticationPage(BasePage):
    def __init__(self, page):
        super().__init__(page)
        self.path = "/global/security/twofactorauth/"
```

**Test Case File**: [`testCases/uiTestCases/globalpage/two_factor_auth/two_factor_auth_page.py`]

```python
from testCases.uiPages.globalpage.two_factor_auth.two_factor_auth_page import (
    TwoFactorAuthenticationPage,
)
import pytest
import allure

@allure.feature("globalpage_two_factor_auth_page")
class TestTwoFactorAuthenticationPage:
    @pytest.fixture(scope="function")
    def init_page(self, login, page):
        two_factor_auth_page = TwoFactorAuthenticationPage(page)
        two_factor_auth_page.goto(
            prefix=login["dash_ui_url"], path=two_factor_auth_page.path, suffix=f""
        )
        return two_factor_auth_page

    @allure.story("two_factor_auth_page_check_title")
    @pytest.mark.smoke
    @pytest.mark.globalpage
    def test_two_factor_auth_page_check_title(self, init_page):
        init_page.check_both_titles("Two-Factor Authentication")
```
#### Billing: Billing Profile Page

**Page Object File**: [`testCases/uiPages/billing/billing_profile/billing_profile_page.py`]

```python
from uiPages.base_page import BasePage

class BillingProfilePage(BasePage):
    def __init__(self, page):
        super().__init__(page)
        self.path = "/global/billing/billingprofile/"
```

**Test Case File**: [`testCases/uiTestCases/billing/billing_profile/billing_profile_page.py`]

```python
from testCases.uiPages.billing.billing_profile.billing_profile_page import (
    BillingProfilePage,
)
import pytest
import allure

@allure.feature("globalpage_billing_profile_page")
class TestBillingProfilePage:
    @pytest.fixture(scope="function")
    def init_page(self, login, page):
        billing_profile_page = BillingProfilePage(page)
        billing_profile_page.goto(
            prefix=login["dash_ui_url"], path=billing_profile_page.path, suffix=f""
        )
        return billing_profile_page

    @allure.story("billing_profile_page_check_title")
    @pytest.mark.smoke
    @pytest.mark.billing
    def test_billing_profile_page_check_title(self, init_page):
        init_page.check_both_titles("Billing Profile")
```
#### Billing: Invoices Page

**Page Object File**: [`testCases/uiPages/billing/invoices/invoices_page.py`]

```python
from uiPages.base_page import BasePage

class InvoicesPage(BasePage):
    def __init__(self, page):
        super().__init__(page)
        self.path = "/global/billing/invoices/"
```

**Test Case File**: [`testCases/uiTestCases/billing/invoices/invoices_page.py`]

```python
from testCases.uiPages.billing.invoices.invoices_page import (
    InvoicesPage,
)
import pytest
import allure

@allure.feature("globalpage_invoices_page")
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
```

#### GlobalPage: Site Profile Page

**Page Object File**: [`testCases/uiPages/globalpage/site_profile/site_profile_page.py`]

```python
from uiPages.base_page import BasePage

class SiteProfilePage(BasePage):
    def __init__(self, page):
        super().__init__(page)
        self.path = "/global/site/profile/"
```

**Test Case File**: [`testCases/uiTestCases/globalpage/site_profile/site_profile_page.py`]

```python
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
```
#### GlobalPage: Custom SMTP Servers Page

**Page Object File**: [`testCases/uiPages/globalpage/custom_smtp_servers/custom_smtp_servers_page.py`]

```python
from uiPages.base_page import BasePage

class CustomSMTPServersPage(BasePage):
    def __init__(self, page):
        super().__init__(page)
        self.path = "/global/site/customSmtpServers/"
```

**Test Case File**: [`testCases/uiTestCases/globalpage/custom_smtp_servers/custom_smtp_servers_page.py`]

```python
from testCases.uiPages.globalpage.custom_smtp_servers.custom_smtp_servers_page import (
    CustomSMTPServersPage,
)
import pytest
import allure

@allure.feature("globalpage_custom_smtp_servers_page")
class TestCustomSMTPServersPage:
    @pytest.fixture(scope="function")
    def init_page(self, login, page):
        custom_smtp_servers_page = CustomSMTPServersPage(page)
        custom_smtp_servers_page.goto(
            prefix=login["dash_ui_url"], path=custom_smtp_servers_page.path, suffix=f""
        )
        return custom_smtp_servers_page

    @allure.story("custom_smtp_servers_page_check_title")
    @pytest.mark.smoke
    @pytest.mark.globalpage
    def test_custom_smtp_servers_page_check_title(self, init_page):
        init_page.check_both_titles("Custom SMTP Servers")
```
#### GlobalPage: New Custom SMTP Server Page

**Page Object File**: [`testCases/uiPages/globalpage/custom_smtp_servers/new_custom_smtp_server_page.py`]

```python
from uiPages.base_page import BasePage

class NewCustomSMTPServerPage(BasePage):
    def __init__(self, page):
        super().__init__(page)
        self.path = "/global/site/customSmtpServers/new"
```

**Test Case File**: [`testCases/uiTestCases/globalpage/custom_smtp_servers/new_custom_smtp_server_page.py`]

```python
from testCases.uiPages.globalpage.custom_smtp_servers.new_custom_smtp_server_page import (
    NewCustomSMTPServerPage,
)
import pytest
import allure

@allure.feature("globalpage_new_custom_smtp_server_page")
class TestNewCustomSMTPServerPage:
    @pytest.fixture(scope="function")
    def init_page(self, login, page):
        new_custom_smtp_server_page = NewCustomSMTPServerPage(page)
        new_custom_smtp_server_page.goto(
            prefix=login["dash_ui_url"], path=new_custom_smtp_server_page.path, suffix=f""
        )
        return new_custom_smtp_server_page

    @allure.story("new_custom_smtp_server_page_check_title")
    @pytest.mark.smoke
    @pytest.mark.globalpage
    def test_new_custom_smtp_server_page_check_title(self, init_page):
        init_page.check_both_titles("New Custom SMTP Server")
```
#### GlobalPage: Edit Custom SMTP Server Page

**Page Object File**: [`testCases/uiPages/globalpage/custom_smtp_servers/edit_custom_smtp_server_page.py`]

```python
from uiPages.base_page import BasePage

class EditCustomSMTPServerPage(BasePage):
    def __init__(self, page):
        super().__init__(page)
        self.path = "/global/site/customSmtpServers/edit"
```

**Test Case File**: [`testCases/uiTestCases/globalpage/custom_smtp_servers/edit_custom_smtp_server_page.py`]

```python
from testCases.uiPages.globalpage.custom_smtp_servers.edit_custom_smtp_server_page import (
    EditCustomSMTPServerPage,
)
import pytest
import allure

@allure.feature("globalpage_edit_custom_smtp_server_page")
class TestEditCustomSMTPServerPage:
    @pytest.fixture(scope="function")
    def init_page(self, login, create_custom_smtp_server, page):
        id = create_custom_smtp_server.json()["id"]

        edit_custom_smtp_server_page = EditCustomSMTPServerPage(page)
        edit_custom_smtp_server_page.goto(
            prefix=login["dash_ui_url"], path=edit_custom_smtp_server_page.path, suffix=f"?customsmtpserverid="+id
        )
        return edit_custom_smtp_server_page

    @allure.story("edit_custom_smtp_server_page_check_title")
    @pytest.mark.smoke
    @pytest.mark.globalpage
    def test_edit_custom_smtp_server_page_check_title(self, init_page):
        init_page.check_both_titles("Edit Custom SMTP Server")
```

### Hints

1. For {page_title}, if it's empty, please use the value of {page_name}. If it's not empty, please use the value of {page_title}.
2. For {menu_name}, if it's empty, please use the value of {page_name}. If it's not empty, please use the value of {menu_name}. Either way, you need to convert it to snake_case and lower-case.

### This is the List of Pages and Attributes. You need to create the files for these pages.

| module_name  | menu_name | page_name          | page_title | path                                     | suffix_querystring_key | set_up_fixture   |
| ------------ | --------- | ------------------ | ---------- | ---------------------------------------- | ---------------------- | ---------------- |
| globalpage | Password Policy | Password Policy | | /global/security/sitepasswordpolicy/ |  |    |
| globalpage | Two-Factor Authentication | Two-Factor Authentication | | /global/security/twofactorauth/ |  |    |
| globalpage | Profile | Site Profile | | /global/site/profile/ |  |    |
| globalpage | Custom SMTP Servers | Custom SMTP Servers | | /global/security/customSmtpServers/ |  |    |
| globalpage | Custom SMTP Servers | New Custom SMTP Server | | /global/security/customSmtpServers/new |  |    |
| globalpage | Custom SMTP Servers | Edit Custom SMTP Server | | /global/security/customSmtpServers/edit |?customsmtpserverid=  |create_customsmtpserver_id    |
| billing | Billing Profile | Billing Profile | | /global/billing/billingprofile/|  |    |
| billing | Invoices | Invoices | | /global/billing/invoices/ |  |    |

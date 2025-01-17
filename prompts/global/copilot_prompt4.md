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


#### GlobalPage: Agent Single Sign-On Page

**Page Object File**: [`testCases/uiPages/globalpage/agent_single_sign_on/agent_single_sign_on_page.py`]

```python
from uiPages.base_page import BasePage

class AgentSingleSignOnPage(BasePage):
    def __init__(self, page):
        super().__init__(page)
        self.path = "/global/security/agentsinglesignon/"
```

**Test Case File**: [`testCases/uiTestCases/globalpage/agent_single_sign_on/agent_single_sign_on_page.py`]

```python
from testCases.uiPages.globalpage.agent_single_sign_on.agent_single_sign_on_page import (
    AgentSingleSignOnPage,
)
import pytest
import allure

@allure.feature("globalpage_agent_single_sign_on_page")
class TestAgentSingleSignOnPage:
    @pytest.fixture(scope="function")
    def init_page(self, login, page):
        agent_single_sign_on_page = AgentSingleSignOnPage(page)
        agent_single_sign_on_page.goto(
            prefix=login["dash_ui_url"], path=agent_single_sign_on_page.path, suffix=f""
        )
        return agent_single_sign_on_page

    @allure.story("agent_single_sign_on_page_check_title")
    @pytest.mark.smoke
    @pytest.mark.globalpage
    def test_agent_single_sign_on_page_check_title(self, init_page):
        init_page.check_both_titles("Agent Single Sign-On")
```
#### GlobalPage: Audit Log Page

**Page Object File**: [`testCases/uiPages/globalpage/audit_log/audit_log_page.py`]

```python
from uiPages.base_page import BasePage

class AuditLogPage(BasePage):
    def __init__(self, page):
        super().__init__(page)
        self.path = "/global/security/auditlogmanage/"
```

**Test Case File**: [`testCases/uiTestCases/globalpage/audit_log/audit_log_page.py`]

```python
from testCases.uiPages.globalpage.audit_log.audit_log_page import (
    AuditLogPage,
)
import pytest
import allure

@allure.feature("globalpage_audit_log_page")
class TestAuditLogPage:
    @pytest.fixture(scope="function")
    def init_page(self, login, page):
        audit_log_page = AuditLogPage(page)
        audit_log_page.goto(
            prefix=login["dash_ui_url"], path=audit_log_page.path, suffix=f""
        )
        return audit_log_page

    @allure.story("audit_log_page_check_title")
    @pytest.mark.smoke
    @pytest.mark.globalpage
    def test_audit_log_page_check_title(self, init_page):
        init_page.check_both_titles("Audit Log")
```

#### GlobalPage: OAuth Client Page

**Page Object File**: [`testCases/uiPages/globalpage/oauth_client/oauth_client_page.py`]

```python
from uiPages.base_page import BasePage

class OAuthClientPage(BasePage):
    def __init__(self, page):
        super().__init__(page)
        self.path = "/global/security/apitoken/"
```

**Test Case File**: [`testCases/uiTestCases/globalpage/oauth_client/oauth_client_page.py`]

```python
from testCases.uiPages.globalpage.oauth_client.oauth_client_page import (
    OAuthClientPage,
)
import pytest
import allure

@allure.feature("globalpage_oauth_client_page")
class TestOAuthClientPage:
    @pytest.fixture(scope="function")
    def init_page(self, login, page):
        oauth_client_page = OAuthClientPage(page)
        oauth_client_page.goto(
            prefix=login["dash_ui_url"], path=oauth_client_page.path, suffix=f""
        )
        return oauth_client_page

    @allure.story("oauth_client_page_check_title")
    @pytest.mark.smoke
    @pytest.mark.globalpage
    def test_oauth_client_page_check_title(self, init_page):
        init_page.check_both_titles("OAuth Client")
```
#### GlobalPage: New OAuth Client Page

**Page Object File**: [`testCases/uiPages/globalpage/oauth_client/new_oauth_client_page.py`]

```python
from uiPages.base_page import BasePage

class NewOAuthClientPage(BasePage):
    def __init__(self, page):
        super().__init__(page)
        self.path = "/global/security/apitoken/new"
```

**Test Case File**: [`testCases/uiTestCases/globalpage/oauth_client/new_oauth_client_page.py`]

```python
from testCases.uiPages.globalpage.oauth_client.new_oauth_client_page import (
    NewOAuthClientPage,
)
import pytest
import allure

@allure.feature("globalpage_new_oauth_client_page")
class TestNewOAuthClientPage:
    @pytest.fixture(scope="function")
    def init_page(self, login, page):
        new_oauth_client_page = NewOAuthClientPage(page)
        new_oauth_client_page.goto(
            prefix=login["dash_ui_url"], path=new_oauth_client_page.path, suffix=f""
        )
        return new_oauth_client_page

    @allure.story("new_oauth_client_page_check_title")
    @pytest.mark.smoke
    @pytest.mark.globalpage
    def test_new_oauth_client_page_check_title(self, init_page):
        init_page.check_both_titles("New OAuth Client")
```
#### GlobalPage: Edit OAuth Client Page

**Page Object File**: [`testCases/uiPages/globalpage/oauth_client/edit_oauth_client_page.py`]

```python
from uiPages.base_page import BasePage

class EditOAuthClientPage(BasePage):
    def __init__(self, page):
        super().__init__(page)
        self.path = "/global/security/apitoken/edit"
```

**Test Case File**: [`testCases/uiTestCases/globalpage/oauth_client/edit_oauth_client_page.py`]

```python
from testCases.uiPages.globalpage.oauth_client.edit_oauth_client_page import (
    EditOAuthClientPage,
)
import pytest
import allure

@allure.feature("globalpage_edit_oauth_client_page")
class TestEditOAuthClientPage:
    @pytest.fixture(scope="function")
    def init_page(self, login, create_oauth_client, page):
        id = create_oauth_client.json()["id"]

        edit_oauth_client_page = EditOAuthClientPage(page)
        edit_oauth_client_page.goto(
            prefix=login["dash_ui_url"], path=edit_oauth_client_page.path, suffix=f"?oauthclientid="+id
        )
        return edit_oauth_client_page

    @allure.story("edit_oauth_client_page_check_title")
    @pytest.mark.smoke
    @pytest.mark.globalpage
    def test_edit_oauth_client_page_check_title(self, init_page):
        init_page.check_both_titles("Edit OAuth Client")
```

#### GlobalPage: Secure Forms Page

**Page Object File**: [`testCases/uiPages/globalpage/secure_forms/secure_forms_page.py`]

```python
from uiPages.base_page import BasePage

class SecureFormsPage(BasePage):
    def __init__(self, page):
        super().__init__(page)
        self.path = "/global/security/secureforms/"
```

**Test Case File**: [`testCases/uiTestCases/globalpage/secure_forms/secure_forms_page.py`]

```python
from testCases.uiPages.globalpage.secure_forms.secure_forms_page import (
    SecureFormsPage,
)
import pytest
import allure

@allure.feature("globalpage_secure_forms_page")
class TestSecureFormsPage:
    @pytest.fixture(scope="function")
    def init_page(self, login, page):
        secure_forms_page = SecureFormsPage(page)
        secure_forms_page.goto(
            prefix=login["dash_ui_url"], path=secure_forms_page.path, suffix=f""
        )
        return secure_forms_page

    @allure.story("secure_forms_page_check_title")
    @pytest.mark.smoke
    @pytest.mark.globalpage
    def test_secure_forms_page_check_title(self, init_page):
        init_page.check_both_titles("Secure Forms")
```
#### GlobalPage: New Secure Form Page

**Page Object File**: [`testCases/uiPages/globalpage/secure_forms/new_secure_form_page.py`]

```python
from uiPages.base_page import BasePage

class NewSecureFormPage(BasePage):
    def __init__(self, page):
        super().__init__(page)
        self.path = "/global/security/secureforms/new"
```

**Test Case File**: [`testCases/uiTestCases/globalpage/secure_forms/new_secure_form_page.py`]

```python
from testCases.uiPages.globalpage.secure_forms.new_secure_form_page import (
    NewSecureFormPage,
)
import pytest
import allure

@allure.feature("globalpage_new_secure_form_page")
class TestNewSecureFormPage:
    @pytest.fixture(scope="function")
    def init_page(self, login, page):
        new_secure_form_page = NewSecureFormPage(page)
        new_secure_form_page.goto(
            prefix=login["dash_ui_url"], path=new_secure_form_page.path, suffix=f""
        )
        return new_secure_form_page

    @allure.story("new_secure_form_page_check_title")
    @pytest.mark.smoke
    @pytest.mark.globalpage
    def test_new_secure_form_page_check_title(self, init_page):
        init_page.check_both_titles("New Secure Form")
```
#### GlobalPage: Edit Secure Form Page

**Page Object File**: [`testCases/uiPages/globalpage/secure_forms/edit_secure_form_page.py`]

```python
from uiPages.base_page import BasePage

class EditSecureFormPage(BasePage):
    def __init__(self, page):
        super().__init__(page)
        self.path = "/global/security/apitoken/edit"
```

**Test Case File**: [`testCases/uiTestCases/globalpage/secure_forms/edit_secure_form_page.py`]

```python
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
```


### Hints

1. For {page_title}, if it's empty, please use the value of {page_name}. If it's not empty, please use the value of {page_title}.
2. For {menu_name}, if it's empty, please use the value of {page_name}. If it's not empty, please use the value of {menu_name}. Either way, you need to convert it to snake_case and lower-case.

### This is the List of Pages and Attributes. You need to create the files for these pages.

| module_name  | menu_name | page_name          | page_title | path                                     | suffix_querystring_key | set_up_fixture   |
| ------------ | --------- | ------------------ | ---------- | ---------------------------------------- | ---------------------- | ---------------- |
| globalpage | Agent Single Sign-On | Agent Single Sign-On (SSO) | | /global/security/agentsinglesignon/ |  |    |
| globalpage | Audit Log | Audit Log | | /global/security/auditlogmanage/ |  |    |
| globalpage | OAuth Client | OAuth Client | | /global/security/apitoken/ |  |    |
| globalpage | OAuth Client | New OAuth Client | | /global/security/apitoken/new |  |    |
| globalpage | OAuth Client | Edit OAuth Client | | /global/security/apitoken/edit |?oauthclientid=  | create_oauthclient_id   |
| globalpage | Secure Forms | Secure Forms | | /global/security/secureforms/ |  |    |
| globalpage | Secure Forms | New Secure Form | | /global/security/secureforms/new |  |    |
| globalpage | Secure Forms | Edit Secure Form | | /global/security/secureforms/edit |?secureformsid=  | create_secureforms_id   |

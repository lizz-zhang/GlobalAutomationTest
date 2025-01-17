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

#### GlobalPage: Auto Translation Page

**Page Object File**: [`testCases/uiPages/globalpage/auto_translation/auto_translation_page.py`]

```python
from uiPages.base_page import BasePage

class AutoTranslationPage(BasePage):
    def __init__(self, page):
        super().__init__(page)
        self.path = "/global/autotranslation/"
```

**Test Case File**: [`testCases/uiTestCases/globalpage/auto_translation/auto_translation_page.py`]

```python
from testCases.uiPages.globalpage.auto_translation.auto_translation_page import (
    AutoTranslationPage,
)
import pytest
import allure

@allure.feature("globalpage_auto_translation_page")
class TestAutoTranslationPage:
    @pytest.fixture(scope="function")
    def init_page(self, login, page):
        auto_translation_page = AutoTranslationPage(page)
        auto_translation_page.goto(
            prefix=login["dash_ui_url"], path=auto_translation_page.path, suffix=f""
        )
        return auto_translation_page

    @allure.story("auto_translation_page_check_title")
    @pytest.mark.smoke
    @pytest.mark.globalpage
    def test_auto_translation_page_check_title(self, init_page):
        init_page.check_both_titles("Auto Translation")
```
#### GlobalPage: Restricted Words Page

**Page Object File**: [`testCases/uiPages/globalpage/restricted_words/restricted_words_page.py`]

```python
from uiPages.base_page import BasePage

class RestrictedWordsPage(BasePage):
    def __init__(self, page):
        super().__init__(page)
        self.path = "/global/security/restrictedwords/"
```

**Test Case File**: [`testCases/uiTestCases/globalpage/restricted_words/restricted_words_page.py`]

```python
from testCases.uiPages.globalpage.restricted_words.restricted_words_page import (
    RestrictedWordsPage,
)
import pytest
import allure

@allure.feature("globalpage_restricted_words_page")
class TestRestrictedWordsPage:
    @pytest.fixture(scope="function")
    def init_page(self, login, page):
        restricted_words_page = RestrictedWordsPage(page)
        restricted_words_page.goto(
            prefix=login["dash_ui_url"], path=restricted_words_page.path, suffix=f""
        )
        return restricted_words_page

    @allure.story("restricted_words_page_check_title")
    @pytest.mark.smoke
    @pytest.mark.globalpage
    def test_restricted_words_page_check_title(self, init_page):
        init_page.check_both_titles("Restricted Words")
```
#### GlobalPage: Credit Card Masking Page

**Page Object File**: [`testCases/uiPages/globalpage/credit_card_masking/credit_card_masking_page.py`]

```python
from uiPages.base_page import BasePage

class CreditCardMaskingPage(BasePage):
    def __init__(self, page):
        super().__init__(page)
        self.path = "/global/security/creditcardmasking/"
```

**Test Case File**: [`testCases/uiTestCases/globalpage/credit_card_masking/credit_card_masking_page.py`]

```python
from testCases.uiPages.globalpage.credit_card_masking.credit_card_masking_page import (
    CreditCardMaskingPage,
)
import pytest
import allure

@allure.feature("globalpage_credit_card_masking_page")
class TestCreditCardMaskingPage:
    @pytest.fixture(scope="function")
    def init_page(self, login, page):
        credit_card_masking_page = CreditCardMaskingPage(page)
        credit_card_masking_page.goto(
            prefix=login["dash_ui_url"], path=credit_card_masking_page.path, suffix=f""
        )
        return credit_card_masking_page

    @allure.story("credit_card_masking_page_check_title")
    @pytest.mark.smoke
    @pytest.mark.globalpage
    def test_credit_card_masking_page_check_title(self, init_page):
        init_page.check_both_titles("Credit Card Masking")
```

#### GlobalPage: IP Allowlist Page

**Page Object File**: [`testCases/uiPages/globalpage/ip_allowlist/login_ip_allowlist_page.py`]

```python
from uiPages.base_page import BasePage

class IPAllowlistPage(BasePage):
    def __init__(self, page):
        super().__init__(page)
        self.path = "/global/security/ipallowlist/loginipallowlist/"
```

**Test Case File**: [`testCases/uiTestCases/globalpage/ip_allowlist/login_ip_allowlist_page.py`]

```python
from testCases.uiPages.globalpage.ip_allowlist.login_ip_allowlist_page import (
    IPAllowlistPage,
)
import pytest
import allure

@allure.feature("globalpage_login_ip_allowlist_page")
class TestIPAllowlistPage:
    @pytest.fixture(scope="function")
    def init_page(self, login, page):
        login_ip_allowlist_page = IPAllowlistPage(page)
        login_ip_allowlist_page.goto(
            prefix=login["dash_ui_url"], path=login_ip_allowlist_page.path, suffix=f""
        )
        return login_ip_allowlist_page

    @allure.story("login_ip_allowlist_page_check_title")
    @pytest.mark.smoke
    @pytest.mark.globalpage
    def test_login_ip_allowlist_page_check_title(self, init_page):
        init_page.check_both_titles("IP Allowlist")
```
#### GlobalPage: IP Allowlist Advanced Page

**Page Object File**: [`testCases/uiPages/globalpage/ip_allowlist/login_ip_allowlist_advanced_page.py`]

```python
from uiPages.base_page import BasePage

class IPAllowlistAdvancedPage(BasePage):
    def __init__(self, page):
        super().__init__(page)
        self.path = "/global/security/ipallowlist/loginipallowlistconfig/"
```

**Test Case File**: [`testCases/uiTestCases/globalpage/ip_allowlist/login_ip_allowlist_advanced_page.py`]

```python
from testCases.uiPages.globalpage.ip_allowlist.login_ip_allowlist_advanced_page import (
    IPAllowlistAdvancedPage,
)
import pytest
import allure

@allure.feature("globalpage_login_ip_allowlist_advanced_page")
class TestIPAllowlistAdvancedPage:
    @pytest.fixture(scope="function")
    def init_page(self, login, page):
        login_ip_allowlist_advanced_page = IPAllowlistAdvancedPage(page)
        login_ip_allowlist_advanced_page.goto(
            prefix=login["dash_ui_url"], path=login_ip_allowlist_advanced_page.path, suffix=f""
        )
        return login_ip_allowlist_advanced_page

    @allure.story("login_ip_allowlist_advanced_page_check_title")
    @pytest.mark.smoke
    @pytest.mark.globalpage
    def test_login_ip_allowlist_advanced_page_check_title(self, init_page):
        init_page.check_both_titles("IP Allowlist Advanced")
```
#### GlobalPage: New IP Range Page

**Page Object File**: [`testCases/uiPages/globalpage/ip_allowlist/new_ip_range_page.py`]

```python
from uiPages.base_page import BasePage

class NewIPRangePage(BasePage):
    def __init__(self, page):
        super().__init__(page)
        self.path = "/global/security/ipallowlist/loginipallowlist/new"
```

**Test Case File**: [`testCases/uiTestCases/globalpage/ip_allowlist/new_ip_range_page.py`]

```python
from testCases.uiPages.globalpage.ip_allowlist.new_ip_range_page import (
    NewIPRangePage,
)
import pytest
import allure

@allure.feature("globalpage_new_ip_range_page")
class TestNewIPRangePage:
    @pytest.fixture(scope="function")
    def init_page(self, login, page):
        new_ip_range_page = NewIPRangePage(page)
        new_ip_range_page.goto(
            prefix=login["dash_ui_url"], path=new_ip_range_page.path, suffix=f""
        )
        return new_ip_range_page  

    @allure.story("new_ip_range_page_check_title")
    @pytest.mark.smoke
    @pytest.mark.globalpage
    def test_new_ip_range_page_check_title(self, init_page):
        init_page.check_both_titles("New IP Range")
```
#### GlobalPage: Edit IP Range Page

**Page Object File**: [`testCases/uiPages/globalpage/ip_allowlist/edit_ip_range_page.py`]

```python
from uiPages.base_page import BasePage

class EditIPRangePage(BasePage):
    def __init__(self, page):
        super().__init__(page)
        self.path = "/global/security/ipallowlist/loginipallowlist/edit"
```

**Test Case File**: [`testCases/uiTestCases/globalpage/ip_allowlist/edit_ip_range_page.py`]

```python
from testCases.uiPages.globalpage.ip_allowlist.edit_ip_range_page import (
    EditIPRangePage,
)
import pytest
import allure

@allure.feature("globalpage_edit_ip_range_page")
class TestEditIPRangePage:
    @pytest.fixture(scope="function")
    def init_page(self, login, create_ip_range, page):
        id = create_ip_range.json()["id"]

        edit_ip_range_page = EditIPRangePage(page)
        edit_ip_range_page.goto(
            prefix=login["dash_ui_url"], path=edit_ip_range_page.path, suffix=f"?loginipallowlistid="+id
        )
        return edit_ip_range_page

    @allure.story("edit_ip_range_page_check_title")
    @pytest.mark.smoke
    @pytest.mark.globalpage
    def test_edit_ip_range_page_check_title(self, init_page):
        init_page.check_both_titles("Edit IP Range")
```


### Hints

1. For {page_title}, if it's empty, please use the value of {page_name}. If it's not empty, please use the value of {page_title}.
2. For {menu_name}, if it's empty, please use the value of {page_name}. If it's not empty, please use the value of {menu_name}. Either way, you need to convert it to snake_case and lower-case.

### This is the List of Pages and Attributes. You need to create the files for these pages.

| module_name  | menu_name | page_name          | page_title | path                                     | suffix_querystring_key | set_up_fixture   |
| ------------ | --------- | ------------------ | ---------- | ---------------------------------------- | ---------------------- | ---------------- |
| globalpage | Auto Translation | Auto Translation | Auto Translation | /global/autotranslation/ |  |    |
| globalpage | Restricted Words | Restricted Words | Restricted Words | /global/security/restrictedwords/ |  |    |
| globalpage | Credit Card Masking | Credit Card Masking |  | /global/security/creditcardmasking/ |  |    |
| globalpage | IP Allowlist | IP Allowlist | | /global/security/ipallowlist/loginipallowlist/ |  |    |
| globalpage | IP Allowlist | IP Allowlist Advanced | | /global/security/ipallowlist/loginipallowlistconfig/ |  |    |
| globalpage | IP Allowlist | New IP Range | | /global/security/ipallowlist/loginipallowlist/new |  |    |
| globalpage | IP Allowlist | Edit IP Range | | /global/security/ipallowlist/loginipallowlist/edit | ?loginipallowlistid= |create_loginipallowlist_id    |

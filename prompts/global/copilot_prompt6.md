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

#### GlobalPage: Public Canned Messages Page

**Page Object File**: [`testCases/uiPages/globalpage/canned_messages/public_canned_messages_page.py`]

```python
from uiPages.base_page import BasePage

class PublicCannedMessagePage(BasePage):
    def __init__(self, page):
        super().__init__(page)
        self.path = "/global/cannedmessages/publiccannedmessage/"
```

**Test Case File**: [`testCases/uiTestCases/globalpage/canned_messages/public_canned_messages_page.py`]

```python
from testCases.uiPages.globalpage.public_canned_messages.public_canned_messages_page import (
    PublicCannedMessagePage,
)
import pytest
import allure

@allure.feature("globalpage_public_canned_messages_page")
class TestPublicCannedMessagePage:
    @pytest.fixture(scope="function")
    def init_page(self, login, page):
        public_canned_messages_page = PublicCannedMessagePage(page)
        public_canned_messages_page.goto(
            prefix=login["dash_ui_url"], path=public_canned_messages_page.path, suffix=f""
        )
        return public_canned_messages_page

    @allure.story("public_canned_messages_page_check_title")
    @pytest.mark.smoke
    @pytest.mark.globalpage
    def test_public_canned_messages_page_check_title(self, init_page):
        init_page.check_both_titles("Public Canned Messages")
```
#### GlobalPage: New Public Canned Message Page

**Page Object File**: [`testCases/uiPages/globalpage/canned_messages/new_public_canned_message_page.py`]

```python
from uiPages.base_page import BasePage

class NewPublicCannedMessagePage(BasePage):
    def __init__(self, page):
        super().__init__(page)
        self.path = "/global/cannedmessages/publiccannedmessage/new"
```

**Test Case File**: [`testCases/uiTestCases/globalpage/canned_messages/new_public_canned_message_page.py`]

```python
from testCases.uiPages.globalpage.custom_away_status.new_public_canned_message_page import (
    NewPublicCannedMessagePage,
)
import pytest
import allure

@allure.feature("globalpage_new_public_canned_message_page")
class TestNewPublicCannedMessagePage:
    @pytest.fixture(scope="function")
    def init_page(self, login, page):
        new_public_canned_message_page = NewPublicCannedMessagePage(page)
        new_public_canned_message_page.goto(
            prefix=login["dash_ui_url"], path=new_public_canned_message_page.path, suffix=f""
        )
        return new_public_canned_message_page  

    @allure.story("new_public_canned_message_page_check_title")
    @pytest.mark.smoke
    @pytest.mark.globalpage
    def test_new_public_canned_message_page_check_title(self, init_page):
        init_page.check_both_titles("New Public Canned Message")
```
#### GlobalPage: Edit Public Canned Message Page

**Page Object File**: [`testCases/uiPages/globalpage/canned_messages/edit_public_canned_message_page.py`]

```python
from uiPages.base_page import BasePage

class EditPublicCannedMessagePage(BasePage):
    def __init__(self, page):
        super().__init__(page)
        self.path = "/global/cannedmessages/publiccannedmessage/edit"
```

**Test Case File**: [`testCases/uiTestCases/globalpage/canned_messages/edit_public_canned_message_page.py`]

```python
from testCases.uiPages.globalpage.public_canned_messages.edit_public_canned_message_page import (
    EditPublicCannedMessagePage,
)
import pytest
import allure

@allure.feature("globalpage_edit_public_canned_message_page")
class TestEditPublicCannedMessagePage:
    @pytest.fixture(scope="function")
    def init_page(self, login, create_public_canned_message, page):
        id = create_public_canned_message.json()["id"]

        edit_public_canned_message_page = EditPublicCannedMessagePage(page)
        edit_public_canned_message_page.goto(
            prefix=login["dash_ui_url"], path=edit_public_canned_message_page.path, suffix=f"?publiccannedmessageid="+id
        )
        return edit_public_canned_message_page

    @allure.story("edit_public_canned_message_page_check_title")
    @pytest.mark.smoke
    @pytest.mark.globalpage
    def test_edit_public_canned_message_page_check_title(self, init_page):
        init_page.check_both_titles("Edit Public Canned Message")
```

#### GlobalPage: Private Canned Messages Page

**Page Object File**: [`testCases/uiPages/globalpage/canned_messages/private_canned_messages_page.py`]

```python
from uiPages.base_page import BasePage

class PrivateCannedMessagePage(BasePage):
    def __init__(self, page):
        super().__init__(page)
        self.path = "/global/cannedmessages/privatecannedmessage/"
```

**Test Case File**: [`testCases/uiTestCases/globalpage/canned_messages/private_canned_messages_page.py`]

```python
from testCases.uiPages.globalpage.private_canned_messages.private_canned_messages_page import (
    PrivateCannedMessagePage,
)
import pytest
import allure

@allure.feature("globalpage_private_canned_messages_page")
class TestPrivateCannedMessagePage:
    @pytest.fixture(scope="function")
    def init_page(self, login, page):
        private_canned_messages_page = PrivateCannedMessagePage(page)
        private_canned_messages_page.goto(
            prefix=login["dash_ui_url"], path=private_canned_messages_page.path, suffix=f""
        )
        return private_canned_messages_page

    @allure.story("private_canned_messages_page_check_title")
    @pytest.mark.smoke
    @pytest.mark.globalpage
    def test_private_canned_messages_page_check_title(self, init_page):
        init_page.check_both_titles("Private Canned Messages")
```
#### GlobalPage: New Private Canned Message Page

**Page Object File**: [`testCases/uiPages/globalpage/canned_messages/new_private_canned_message_page.py`]

```python
from uiPages.base_page import BasePage

class NewPrivateCannedMessagePage(BasePage):
    def __init__(self, page):
        super().__init__(page)
        self.path = "/global/cannedmessages/privatecannedmessage/new"
```

**Test Case File**: [`testCases/uiTestCases/globalpage/canned_messages/new_private_canned_message_page.py`]

```python
from testCases.uiPages.globalpage.private_canned_messages.new_private_canned_message_page import (
    NewPrivateCannedMessagePage,
)
import pytest
import allure

@allure.feature("globalpage_new_private_canned_message_page")
class TestNewPrivateCannedMessagePage:
    @pytest.fixture(scope="function")
    def init_page(self, login, page):
        new_private_canned_message_page = NewPrivateCannedMessagePage(page)
        new_private_canned_message_page.goto(
            prefix=login["dash_ui_url"], path=new_private_canned_message_page.path, suffix=f""
        )
        return new_private_canned_message_page  

    @allure.story("new_private_canned_message_page_check_title")
    @pytest.mark.smoke
    @pytest.mark.globalpage
    def test_new_private_canned_message_page_check_title(self, init_page):
        init_page.check_both_titles("New Private Canned Message")
```
#### GlobalPage: Edit Private Canned Message Page

**Page Object File**: [`testCases/uiPages/globalpage/canned_messages/edit_private_canned_message_page.py`]

```python
from uiPages.base_page import BasePage

class EditPrivateCannedMessagePage(BasePage):
    def __init__(self, page):
        super().__init__(page)
        self.path = "/global/cannedmessages/privatecannedmessage/edit"
```

**Test Case File**: [`testCases/uiTestCases/globalpage/canned_messages/edit_private_canned_message_page.py`]

```python
from testCases.uiPages.globalpage.private_canned_messages.edit_private_canned_message_page import (
    EditPrivateCannedMessagePage,
)
import pytest
import allure

@allure.feature("globalpage_edit_private_canned_message_page")
class TestEditPrivateCannedMessagePage:
    @pytest.fixture(scope="function")
    def init_page(self, login, create_private_canned_message, page):
        id = create_private_canned_message.json()["id"]

        edit_private_canned_message_page = EditPrivateCannedMessagePage(page)
        edit_private_canned_message_page.goto(
            prefix=login["dash_ui_url"], path=edit_private_canned_message_page.path, suffix=f"?privatecannedmessageid="+id
        )
        return edit_private_canned_message_page

    @allure.story("edit_private_canned_message_page_check_title")
    @pytest.mark.smoke
    @pytest.mark.globalpage
    def test_edit_private_canned_message_page_check_title(self, init_page):
        init_page.check_both_titles("Edit Private Canned Message")
```



### Hints

1. For {page_title}, if it's empty, please use the value of {page_name}. If it's not empty, please use the value of {page_title}.
2. For {menu_name}, if it's empty, please use the value of {page_name}. If it's not empty, please use the value of {menu_name}. Either way, you need to convert it to snake_case and lower-case.

### This is the List of Pages and Attributes. You need to create the files for these pages.

| module_name  | menu_name | page_name          | page_title | path                                     | suffix_querystring_key | set_up_fixture   |
| ------------ | --------- | ------------------ | ---------- | ---------------------------------------- | ---------------------- | ---------------- |
| globalpage | Canned Messages | Public Canned Messages |            | /global/cannedmessages/publiccannedmessage/  |                        |                  |
| globalpage | Canned Messages | New Public Canned Message |            | /global/cannedmessages/publiccannedmessage/new  |              |                  |
| globalpage | Canned Messages | Edit Public Canned Message |  | /global/cannedmessages/publiccannedmessage/edut |?publiccannedmessageid= |create_publiccannedmessage_id |
| globalpage | Canned Messages | Private Canned Messages |   | /global/cannedmessages/privatecannedmessage/ |               |                  |
| globalpage | Canned Messages | New Private Canned Message |            | /global/cannedmessages/privatecannedmessage/new  |              |                  |
| globalpage | Canned Messages | Edit Private Canned Message | | /global/cannedmessages/privatecannedmessage/edut |?privatecannedmessageid= |create_privatecannedmessage_id |

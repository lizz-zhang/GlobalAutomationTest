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
    def test_{page_name}_page_check_title(self, init_page):
        init_page.check_both_titles("{page_title}")
```

### Examples

#### Example 1: Screen Sharing Page

**Page Object File**: [`testCases/uiPages/livechatpage/screen_sharing/screen_sharing_page.py`]

```python
from uiPages.base_page import BasePage

class ScreenSharingPage(BasePage):
    def __init__(self, page):
        super().__init__(page)
        self.path = "/livechat/settings/screensharing/"
```

**Test Case File**: [`testCases/uiTestCases/livechatpage/screen_sharing/test_screen_sharing_page.py`]

```python
from testCases.uiPages.livechatpage.screen_sharing.screen_sharing_page import (
    ScreenSharingPage,
)
import pytest
import allure

@allure.feature("livechatpage_screen_sharing_page")
class TestScreenSharingPage:
    @pytest.fixture(scope="function")
    def init_page(self, login, page):
        screen_sharing_page = ScreenSharingPage(page)
        screen_sharing_page.goto(
            prefix=login["dash_ui_url"], path=screen_sharing_page.path, suffix=f""
        )
        return screen_sharing_page

    @allure.story("screen_sharing_page_check_title")
    @pytest.mark.smoke
    def test_screen_sharing_page_check_title(self, init_page):
        init_page.check_both_titles("Screen Sharing")
```

#### Example 2: Edit Banned Visitor Page

**Page Object File**: [`testCases/uiPages/livechatpage/ban_list/edit_banned_visitor_page.py`]

```python
from uiPages.base_page import BasePage

class EditBannedVisitorPage(BasePage):
    def __init__(self, page):
        super().__init__(page)
        self.path = "/livechat/settings/banlist/bannedvisitor/edit"
```

**Test Case File**: [`testCases/uiTestCases/livechatpage/ban_list/test_edit_banned_visitor_page.py`]

```python
from testCases.uiPages.livechatpage.ban_list.edit_banned_visitor_page import (
    EditBannedVisitorPage,
)
import pytest
import allure

@allure.feature("livechatpage_edit_banned_visitor_page")
class TestEditBannedVisitorPage:
    @pytest.fixture(scope="function")
    def init_page(self, login, create_banned_visitor, page):
        id = create_banned_visitor.json()["id"]

        edit_banned_visitor_page = EditBannedVisitorPage(page)
        edit_banned_visitor_page.goto(
            prefix=login["dash_ui_url"],
            path=edit_banned_visitor_page.path,
            suffix=f"?bannedvisitorid="+id,
        )
        return edit_banned_visitor_page

    @allure.story("edit_banned_visitor_page_check_title")
    @pytest.mark.smoke
    def test_edit_banned_visitor_page_check_title(self, init_page):
        init_page.check_both_titles("Edit Banned Visitor")
```

### Hints

1. For {page_title}, if it's empty, please use the value of {page_name}. If it's not empty, please use the value of {page_title}.
2. For {menu_name}, if it's empty, please use the value of {page_name}. If it's not empty, please use the value of {menu_name}. Either way, you need to convert it to snake_case and lower-case.

### This is the List of Pages and Attributes. You need to create the files for these pages.

| module_name  | menu_name | page_name          | page_title | path                                     | suffix_querystring_key | set_up_fixture   |
| ------------ | --------- | ------------------ | ---------- | ---------------------------------------- | ---------------------- | ---------------- |
| livechatpage | Ban List  | Edit Banned IP     |            | /livechat/settings/banlist/bannedip/edit | ?bannedipid=           | create_banned_ip |
| livechatpage |           | Cookie Restriction |            | /livechat/settings/cookierestriction/    |                        |                  |

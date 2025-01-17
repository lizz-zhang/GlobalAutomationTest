We have the following page object file in our end-to-end auto testing framework. This page object file is under `testCases\uiPages\{module_name}\{menu_name}` folder. The file name is in the format of `{page_name}_page.py`

The pseudo code is as follows:

```python
from uiPages.base_page import BasePage


class {PageName}Page(BasePage):
    def __init__(self, page):
        super().__init__(page)
        self.path = "{path}"

```

And we have the following test case file which is matching the page object file, in our end-to-end auto testing framework. The test case file is under `testCases\uiTestCases\{module_name}\{menu_name}` folder. The file name is in the format of `test_{page_name}_page.py`.

Please note that when the {suffix_querystring_key} and {set_up_fixture} attributes are provided, the code is slightly different. The {set_up_fixture} attribute is used in the init_page function as a fixture, and the id is extracted from the response of the {set_up_fixture} and appended to the suffix parameter.

The pseudo code is as follows:

```python

from testCases.uiPages.{module_name}.{page_name}.{page_name}_page import (
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

-------------------- This is the first example --------------------------------
For example, For Screen Sharing page, we have the following attributes:

| module_name  | menu_name | page_name      | page_title | path                              | suffix_querystring_key | set_up_fixture |
| ------------ | --------- | -------------- | ---------- | --------------------------------- | ---------------------- | -------------- |
| livechatpage |           | Screen Sharing |            | /livechat/settings/screensharing/ |                        |                |

We have the Page Object file: screen_sharing_page.py, it belongs to livechatpage module. And it's under testCases\uiPages\livechatpage\screen_sharing folder.
In this file we have the following code. As you can see, the class name is ScreenSharingPage and the path is "/livechat/settings/screensharing/":

```python
from uiPages.base_page import BasePage


class ScreenSharingPage(BasePage):
    def __init__(self, page):
        super().__init__(page)
        self.path = "/livechat/settings/screensharing/"

```

We have the Test Case file: test_screen_sharing_page.py, it belongs to livechatpage module. And it's under testCases\uiTestCases\livechatpage\screen_sharing folder.
In this file we have the following code. As you can see, the class name is TestScreenSharingPage

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

-------------------- This is the second example --------------------------------
Another example, For Edit Banned Visitor page, we have the following attributes. Please note that we have the {suffix_querystring_key} and {set_up_fixture} attributes in this example.

| module_name  | menu_name | page_name           | page_title | path                                          | suffix_querystring_key | set_up_fixture        |
| ------------ | --------- | ------------------- | ---------- | --------------------------------------------- | ---------------------- | --------------------- |
| livechatpage | Ban List  | Edit Banned Visitor |            | /livechat/settings/banlist/bannedvisitor/edit | ?bannedvisitorid=      | create_banned_visitor |

We have the Page Object file: edit_banned_visitor_page.py, it belongs to livechatpage module. And it's under testCases\uiPages\livechatpage\ban_list folder.
In this file we have the following code. As you can see, the class name is EditBannedVisitorPage and the path is "/livechat/settings/banlist/bannedvisitor/edit":

```python
from uiPages.base_page import BasePage


class EditBannedVisitorPage(BasePage):
    def __init__(self, page):
        super().__init__(page)
        self.path = "/livechat/settings/banlist/bannedvisitor/edit"

```

We have the Test Case file: test_edit_banned_visitor_page.py, it belongs to livechatpage module. And it's under testCases\uiTestCases\livechatpage\ban_list folder.

Because we have the {suffix_querystring_key} and {set_up_fixture} attributes in this example, the code is slightly different. There are several differences compared to the Screen Sharing page test case file.

1. In the init_page function, we added the {set_up_fixture} parameter as a fixture, and we added the following line of code to get the id from the {set_up_fixture} response.

```python
    def init_page(self, login, create_banned_visitor, page):
        id = create_banned_visitor.json()["id"]
```

2. In the init_page function, we added the {suffix_querystring_key} parameter, and we added the following line of code to append the id to the suffix parameter.

```python
        suffix=f"?bannedvisitorid="+id

```

And the complete code for the test case file is as follows:

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

I will provide a list of {page_name} and {path} for each page.

1. You need to create a new page object file for each {page_name} with the path as {path} using the same framework code as screen_sharing_page.py, but you need to update the code matching the {page_name}.
2. You need to create a test case file for each {page_name} using the same framework code as test_screen_sharing_page.py, but you need to update the code matching the {page_name}.
3. For {page_title}, if it's empty, please use the value of {page_name}. If it's not empty, please use the value of {page_title}.
4. For {menu_name}, if it's empty, please use the value of {page_name}. If it's not empty, please use the value of {menu_name}.

List of pages as follows:

| module_name  | menu_name | page_name          | page_title | path                                     | suffix_querystring_key | set_up_fixture   |
| ------------ | --------- | ------------------ | ---------- | ---------------------------------------- | ---------------------- | ---------------- |
| livechatpage | Ban List  | Edit Banned IP     |            | /livechat/settings/banlist/bannedip/edit | ?bannedipid=           | create_banned_ip |
| livechatpage |           | Cookie Restriction |            | /livechat/settings/cookierestriction/    |                        |                  |

Please create the page object file and test case file directly for the page in above list. Do not create files for the Screen Sharing page as they are already present. Do not provide code and let me copy and paste to new files.
The files created should be in the current workspace and current project. I don't want to create a new workspace.

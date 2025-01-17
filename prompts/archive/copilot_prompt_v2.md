We have the following page object file in our end-to-end auto testing framework. This page object file is under `testCases\uiPages\{module_name}\{menu_name}` folder. The file name is in the format of {page_name}\_page.py

The pseudo code is as follows:

```python
from uiPages.base_page import BasePage


class {PageName}Page(BasePage):
    def __init__(self, page):
        super().__init__(page)
        self.path = "{path}"

```

And we have the following test case file which is matching the page object file, in our end-to-end auto testing framework. The test case file is under `testCases\uiTestCases\{module_name}\{menu_name}` folder. The file name is in the format of test\_{page_name}\_page.py

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
    def init_page(self, login, page):
        {page_name}_page = {PageName}Page(page)
        {page_name}_page.goto(
            prefix=login["dash_ui_url"], path={page_name}_page.path, suffix=""
        )
        return {page_name}_page

    @allure.story("{page_name}_page_check_title")
    @pytest.mark.smoke
    def test_{page_name}_page_check_title(self, init_page):
        init_page.check_both_titles("{page_title}")
```

For example, screen_sharing_page.py, it belongs to livechatpage module. And it's under testCases\uiPages\livechatpage\screen_sharing folder.
In this file we have the following code. As you can see, the class name is ScreenSharingPage and the path is "/livechat/settings/screensharing/":

```python
from uiPages.base_page import BasePage


class ScreenSharingPage(BasePage):
    def __init__(self, page):
        super().__init__(page)
        self.path = "/livechat/settings/screensharing/"

```

For example, test_screen_sharing_page.py, it belongs to livechatpage module. And it's under testCases\uiTestCases\livechatpage\screen_sharing folder.
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
            prefix=login["dash_ui_url"], path=screen_sharing_page.path, suffix=""
        )
        return screen_sharing_page

    @allure.story("screen_sharing_page_check_title")
    @pytest.mark.smoke
    def test_screen_sharing_page_check_title(self, init_page):
        init_page.check_both_titles("Screen Sharing")
```

I will provide a list of {page_name} and {path} for each page.

1. You need to create a new page object file for each {page_name} with the path as {path} using the same framework code as screen_sharing_page.py, but you need to update the code matching the {page_name}.
2. You need to create a test case file for each {page_name} using the same framework code as test_screen_sharing_page.py, but you need to update the code matching the {page_name}.
3. For {page_title}, if it's empty, please use the value of {page_name}. If it's not empty, please use the value of {page_title}.
4. For {menu_name}, if it's empty, please use the value of {page_name}. If it's not empty, please use the value of {menu_name}.

List of pages as follows:

| module_name  | menu_name | page_name          | path                                  | page_title |
| ------------ | --------- | ------------------ | ------------------------------------- | ---------- |
| livechatpage |           | Cookie Restriction | /livechat/settings/cookierestriction/ |            |

Please create the page object file and test case file directly for the page in above list. Do not create files for the Screen Sharing page as they are already present. Do not provide code and let me copy and paste to new files.
The files created should be in the current workspace and current project. I don't want to create a new workspace.

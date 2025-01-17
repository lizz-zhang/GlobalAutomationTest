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

#### GlobalPage: Subscriptions Page

**Page Object File**: [`testCases/uiPages/globalpage/subscriptions/subscriptions_page.py`]

```python
from uiPages.base_page import BasePage

class SubscriptionsPage(BasePage):
    def __init__(self, page):
        super().__init__(page)
        self.path = "/global/subscriptions/"
```

**Test Case File**: [`testCases/uiTestCases/globalpage/subscriptions/test_subscriptions_page.py`]

```python
from testCases.uiPages.globalpage.subscriptions.subscriptions_page import (
    SubscriptionsPage,
)
import pytest
import allure

@allure.feature("globalpage_subscriptions_page")
class TestSubscriptionsPage:
    @pytest.fixture(scope="function")
    def init_page(self, login, page):
        subscriptions_page = SubscriptionsPage(page)
        subscriptions_page.goto(
            prefix=login["dash_ui_url"], path=subscriptions_page.path, suffix=f""
        )
        return subscriptions_page

    @allure.story("subscriptions_page_check_title")
    @pytest.mark.smoke
    @pytest.mark.globalpage
    def test_subscriptions_page_check_title(self, init_page):
        init_page.check_both_titles("Subscriptions")
```
#### GlobalPage: Add More Subscriptions Page

**Page Object File**: [`testCases/uiPages/globalpage/subscriptions/add_more_subscriptions_page.py`]

```python
from uiPages.base_page import BasePage

class AddMoreSubscriptionsPage(BasePage):
    def __init__(self, page):
        super().__init__(page)
        self.path = "/global/subscriptions/addmore/"
```

**Test Case File**: [`testCases/uiTestCases/globalpage/subscriptions/test_add_more_subscriptions_page.py`]

```python
from testCases.uiPages.globalpage.subscriptions.add_more_subscriptions_page import (
    AddMoreSubscriptionsPage,
)
import pytest
import allure

@allure.feature("globalpage_add_more_subscriptions_page")
class TestAddMoreSubscriptionsPage:
    @pytest.fixture(scope="function")
    def init_page(self, login, page):
        add_more_subscriptions_page = AddMoreSubscriptionsPage(page)
        add_more_subscriptions_page.goto(
            prefix=login["dash_ui_url"], path=add_more_subscriptions_page.path, suffix=f""
        )
        return add_more_subscriptions_page

    @allure.story("add_more_subscriptions_page_check_title")
    @pytest.mark.smoke
    @pytest.mark.globalpage
    def test_add_more_subscriptions_page_check_title(self, init_page):
        init_page.check_both_titles("Add More Subscriptions")
```
#### GlobalPage: Agents Page

**Page Object File**: [`testCases/uiPages/globalpage/agents/agents_page.py`]

```python
from uiPages.base_page import BasePage

class AgentsPage(BasePage):
    def __init__(self, page):
        super().__init__(page)
        self.path = "/global/people/agents/"
```

**Test Case File**: [`testCases/uiTestCases/globalpage/agents/agents_page.py`]

```python
from testCases.uiPages.globalpage.agents.agents_page import (
    AgentsPage,
)
import pytest
import allure

@allure.feature("globalpage_agents_page")
class TestAgentsPage:
    @pytest.fixture(scope="function")
    def init_page(self, login, page):
        agents_page = AgentsPage(page)
        agents_page.goto(
            prefix=login["dash_ui_url"], path=agents_page.path, suffix=f""
        )
        return agents_page

    @allure.story("agents_page_check_title")
    @pytest.mark.smoke
    @pytest.mark.globalpage
    def test_agents_page_check_title(self, init_page):
        init_page.check_both_titles("Agents")
```

#### GlobalPage: New Agents Page

**Page Object File**: [`testCases/uiPages/globalpage/agents/new_agent_page.py`]

```python
from uiPages.base_page import BasePage

class NewAgentPage(BasePage):
    def __init__(self, page):
        super().__init__(page)
        self.path = "/global/people/agents/new"
```

**Test Case File**: [`testCases/uiTestCases/globalpage/agents/new_agent_page.py`]

```python
from testCases.uiPages.globalpage.agents.new_agent_page import (
    NewAgentPage,
)
import pytest
import allure

@allure.feature("globalpage_new_agent_page")
class TestNewAgentPage:
    @pytest.fixture(scope="function")
    def init_page(self, login, page):
        new_agent_page = NewAgentPage(page)
        new_agent_page.goto(
            prefix=login["dash_ui_url"], path=new_agent_page.path, suffix=f""
        )
        return new_agent_page

    @allure.story("new_agent_page_check_title")
    @pytest.mark.smoke
    @pytest.mark.globalpage
    def test_new_agent_page_check_title(self, init_page):
        init_page.check_both_titles("New Agent")
```

#### GlobalPage: Edit Agents Page

**Page Object File**: [`testCases/uiPages/globalpage/agents/edit_agent_page.py`]

```python
from uiPages.base_page import BasePage

class EditAgentPage(BasePage):
    def __init__(self, page):
        super().__init__(page)
        self.path = "/global/people/agents/edit"
```

**Test Case File**: [`testCases/uiTestCases/globalpage/agents/edit_agent_page.py`]

```python
from testCases.uiPages.globalpage.agents.edit_agent_page import (
    EditAgentPage,
)
import pytest
import allure

@allure.feature("globalpage_edit_agent_page")
class TestEditAgentPage:
    @pytest.fixture(scope="function")
    def init_page(self, login, create_agent, page):
        id = create_agent.json()["id"]

        edit_agent_page = EditAgentPage(page)
        edit_agent_page.goto(
            prefix=login["dash_ui_url"], path=edit_agent_page.path, suffix=f"?agentid="+id
        )
        return edit_agent_page

    @allure.story("edit_agent_page_check_title")
    @pytest.mark.smoke
    @pytest.mark.globalpage
    def test_edit_agent_page_check_title(self, init_page):
        init_page.check_both_titles("Edit Agent")
```
#### GlobalPage: Departments Page   

**Page Object File**: [`testCases/uiPages/globalpage/departments/departments_page.py`]

```python
from uiPages.base_page import BasePage

class DepartmentsPage(BasePage):
    def __init__(self, page):
        super().__init__(page)
        self.path = "/global/people/departments/"
```

**Test Case File**: [`testCases/uiTestCases/globalpage/departments/departments_page.py`]

```python
from testCases.uiPages.globalpage.departments.departments_page import (
    DepartmentsPage,
)
import pytest
import allure

@allure.feature("globalpage_departments_page")
class TestDepartmentsPage:
    @pytest.fixture(scope="function")
    def init_page(self, login, page):
        departments_page = DepartmentsPage(page)
        departments_page.goto(
            prefix=login["dash_ui_url"], path=departments_page.path, suffix=f""
        )
        return departments_page

    @allure.story("departments_page_check_title")
    @pytest.mark.smoke
    @pytest.mark.globalpage
    def test_departments_page_check_title(self, init_page):
        init_page.check_both_titles("Departments")
```
#### GlobalPage: New Departments Page

**Page Object File**: [`testCases/uiPages/globalpage/departments/new_department_page.py`]

```python
from uiPages.base_page import BasePage

class NewDepartmentsPage(BasePage):
    def __init__(self, page):
        super().__init__(page)
        self.path = "/global/people/departments/new"
```

**Test Case File**: [`testCases/uiTestCases/globalpage/departments/new_department_page.py`]

```python
from testCases.uiPages.globalpage.departments.new_department_page import (
    NewDepartmentsPage,
)
import pytest
import allure

@allure.feature("globalpage_new_department_page")
class TestNewDepartmentsPage:
    @pytest.fixture(scope="function")
    def init_page(self, login, page):
        new_department_page = NewDepartmentsPage(page)
        new_department_page.goto(
            prefix=login["dash_ui_url"], path=new_department_page.path, suffix=f""
        )
        return new_department_page

    @allure.story("new_department_page_check_title")
    @pytest.mark.smoke
    @pytest.mark.globalpage
    def test_new_department_page_check_title(self, init_page):
        init_page.check_both_titles("New Department")
```
#### GlobalPage: Edit Departments Page

**Page Object File**: [`testCases/uiPages/globalpage/departments/edit_department_page.py`]

```python
from uiPages.base_page import BasePage

class EditDepartmentsPage(BasePage):
    def __init__(self, page):
        super().__init__(page)
        self.path = "/global/people/departments/edit"
```

**Test Case File**: [`testCases/uiTestCases/globalpage/departments/edit_department_page.py`]

```python
from testCases.uiPages.globalpage.departments.edit_department_page import (
    EditDepartmentsPage,
)
import pytest
import allure

@allure.feature("globalpage_edit_department_page")
class TestEditDepartmentsPage:
    @pytest.fixture(scope="function")
    def init_page(self, login, create_department, page):
        id = create_department.json()["id"]

        edit_department_page = EditDepartmentsPage(page)
        edit_department_page.goto(
            prefix=login["dash_ui_url"], path=edit_department_page.path, suffix=f"?departmentid="+id
        )
        return edit_department_page

    @allure.story("edit_department_page_check_title")
    @pytest.mark.smoke
    @pytest.mark.globalpage
    def test_edit_department_page_check_title(self, init_page):
        init_page.check_both_titles("Edit Department")
```




### Hints

1. For {page_title}, if it's empty, please use the value of {page_name}. If it's not empty, please use the value of {page_title}.
2. For {menu_name}, if it's empty, please use the value of {page_name}. If it's not empty, please use the value of {menu_name}. Either way, you need to convert it to snake_case and lower-case.

### This is the List of Pages and Attributes. You need to create the files for these pages.

| module_name  | menu_name | page_name          | page_title | path                                     | suffix_querystring_key | set_up_fixture   |
| ------------ | --------- | ------------------ | ---------- | ---------------------------------------- | ---------------------- | ---------------- |
| globalpage | Subscriptions |                  |            | /global/subscriptions/                   |                        |                  |
| globalpage | Subscriptions | Add More Subscriptions |            | /global/subscriptions/addmore/    |                        |                  |
| globalpage | Agents        | Agents           | Agents     | /global/people/agents/                  |                        |                  |
| globalpage | Agents        | New Agent        | New Agent  | /global/people/agents/new               |                        |                  |
| globalpage | Agents        | Edit Agent       | Edit Agent | /global/people/agents/edit              | ?agentid=              | create_agent_id  |
| globalpage | Departments   | Departments      |            | /global/people/departments/             |                        |                  |
| globalpage | Departments   | New Department   | New Department    | /global/people/departments/new   |                        |                  |
| globalpage | Departments   | Edit Department   | Edit Department  | /global/people/departments/edit   |?departmentid=      | create_department_id |

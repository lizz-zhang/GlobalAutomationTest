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

#### GlobalPage: Skills Page

**Page Object File**: [`testCases/uiPages/globalpage/skills/skills_page.py`]

```python
from uiPages.base_page import BasePage

class SkillsPage(BasePage):
    def __init__(self, page):
        super().__init__(page)
        self.path = "/global/people/skills/"
```

**Test Case File**: [`testCases/uiTestCases/globalpage/skills/skills_page.py`]

```python
from testCases.uiPages.globalpage.skills.skills_page import (
    SkillsPage,
)
import pytest
import allure

@allure.feature("globalpage_skills_page")
class TestSkillsPage:
    @pytest.fixture(scope="function")
    def init_page(self, login, page):
        skills_page = SkillsPage(page)
        skills_page.goto(
            prefix=login["dash_ui_url"], path=skills_page.path, suffix=f""
        )
        return skills_page

    @allure.story("skills_page_check_title")
    @pytest.mark.smoke
    @pytest.mark.globalpage
    def test_skills_page_check_title(self, init_page):
        init_page.check_both_titles("Skills")
```
#### GlobalPage: New Skill Page

**Page Object File**: [`testCases/uiPages/globalpage/skills/new_skill_page.py`]

```python
from uiPages.base_page import BasePage

class NewSkillPage(BasePage):
    def __init__(self, page):
        super().__init__(page)
        self.path = "/global/people/skills/new"
```

**Test Case File**: [`testCases/uiTestCases/globalpage/skills/new_skill_page.py`]

```python
from testCases.uiPages.globalpage.skills.new_skill_page import (
    NewSkillPage,
)
import pytest
import allure

@allure.feature("globalpage_new_skill_page")
class TestNewSkillPage:
    @pytest.fixture(scope="function")
    def init_page(self, login, page):
        new_skill_page = NewSkillPage(page)
        new_skill_page.goto(
            prefix=login["dash_ui_url"], path=new_new_skill_page.path, suffix=f""
        )
        return new_skill_page

    @allure.story("new_skill_page_check_title")
    @pytest.mark.smoke
    @pytest.mark.globalpage
    def test_new_skill_page_check_title(self, init_page):
        init_page.check_both_titles("New Skill")
```
#### GlobalPage: Edit Skill Page

**Page Object File**: [`testCases/uiPages/globalpage/skills/edit_skill_page.py`]

```python
from uiPages.base_page import BasePage

class EditSkillPage(BasePage):
    def __init__(self, page):
        super().__init__(page)
        self.path = "/global/people/skills/edit"
```

**Test Case File**: [`testCases/uiTestCases/globalpage/skills/edit_skill_page.py`]

```python
from testCases.uiPages.globalpage.skills.edit_skill_page import (
    EditSkillPage,
)
import pytest
import allure

@allure.feature("globalpage_edit_skill_page")
class TestEditSkillPage:
    @pytest.fixture(scope="function")
    def init_page(self, login, create_skill, page):
        id = create_skill.json()["id"]

        edit_skill_page = EditSkillPage(page)
        edit_skill_page.goto(
            prefix=login["dash_ui_url"], path=edit_skill_page.path, suffix=f"?skillid="+id
        )
        return edit_skill_page

    @allure.story("edit_skill_page_check_title")
    @pytest.mark.smoke
    @pytest.mark.globalpage
    def test_edit_skill_page_check_title(self, init_page):
        init_page.check_both_titles("Edit Skill")
```



#### GlobalPage: Roles Page

**Page Object File**: [`testCases/uiPages/globalpage/roles/roles_page.py`]

```python
from uiPages.base_page import BasePage

class RolesPage(BasePage):
    def __init__(self, page):
        super().__init__(page)
        self.path = "/global/people/roles/"
```

**Test Case File**: [`testCases/uiTestCases/globalpage/roles/roles_page.py`]

```python
from testCases.uiPages.globalpage.roles.roles_page import (
    RolesPage,
)
import pytest
import allure

@allure.feature("globalpage_departments_page")
class TestRolesPage:
    @pytest.fixture(scope="function")
    def init_page(self, login, page):
        roles_page = RolesPage(page)
        roles_page.goto(
            prefix=login["dash_ui_url"], path=roles_page.path, suffix=f""
        )
        return roles_page

    @allure.story("roles_page_check_title")
    @pytest.mark.smoke
    @pytest.mark.globalpage
    def test_roles_page_check_title(self, init_page):
        init_page.check_both_titles("Roles")
```
#### GlobalPage: New Role Page

**Page Object File**: [`testCases/uiPages/globalpage/roles/new_role_page.py`]

```python
from uiPages.base_page import BasePage

class NewRolePage(BasePage):
    def __init__(self, page):
        super().__init__(page)
        self.path = "/global/people/roles/new"
```

**Test Case File**: [`testCases/uiTestCases/globalpage/roles/new_role_page.py`]

```python
from testCases.uiPages.globalpage.roles.new_role_page import (
    NewRolePage,
)
import pytest
import allure

@allure.feature("globalpage_new_role_page")
class TestNewRolePage:
    @pytest.fixture(scope="function")
    def init_page(self, login, page):
        new_role_page = NewRolePage(page)
        new_role_page.goto(
            prefix=login["dash_ui_url"], path=new_role_page.path, suffix=f""
        )
        return new_role_page

    @allure.story("new_role_page_check_title")
    @pytest.mark.smoke
    @pytest.mark.globalpage
    def test_new_role_page_check_title(self, init_page):
        init_page.check_both_titles("New Role")
```
#### GlobalPage: Edit Role Page

**Page Object File**: [`testCases/uiPages/globalpage/roles/edit_role_page.py`]

```python
from uiPages.base_page import BasePage

class EditRolePage(BasePage):
    def __init__(self, page):
        super().__init__(page)
        self.path = "/global/people/roles/edit"
```

**Test Case File**: [`testCases/uiTestCases/globalpage/roles/edit_role_page.py`]

```python
from testCases.uiPages.globalpage.roles.edit_role_page import (
    EditRolePage,
)
import pytest
import allure

@allure.feature("globalpage_edit_role_page")
class TestEditRolePage:
    @pytest.fixture(scope="function")
    def init_page(self, login, create_role, page):
        id = create_role.json()["id"]

        edit_role_page = EditRolePage(page)
        edit_role_page.goto(
            prefix=login["dash_ui_url"], path=edit_role_page.path, suffix=f"?roleid="+id
        )
        return edit_role_page

    @allure.story("edit_role_page_check_title")
    @pytest.mark.smoke
    @pytest.mark.globalpage
    def test_edit_role_page_check_title(self, init_page):
        init_page.check_both_titles("Edit Role")
```

#### GlobalPage: Custom Away Status Page

**Page Object File**: [`testCases/uiPages/globalpage/custom_away_status/custom_away_status_page.py`]

```python
from uiPages.base_page import BasePage

class CustomAwayStatusPage(BasePage):
    def __init__(self, page):
        super().__init__(page)
        self.path = "/global/people/customawaystatus/"
```

**Test Case File**: [`testCases/uiTestCases/globalpage/custom_away_status/custom_away_status_page.py`]

```python
from testCases.uiPages.globalpage.custom_away_status.custom_away_status_page import (
    CustomAwayStatusPage,
)
import pytest
import allure

@allure.feature("globalpage_custom_away_status_page")
class TestCustomAwayStatusPage:
    @pytest.fixture(scope="function")
    def init_page(self, login, page):
        custom_away_status_page = CustomAwayStatusPage(page)
        custom_away_status_page.goto(
            prefix=login["dash_ui_url"], path=custom_away_status_page.path, suffix=f""
        )
        return custom_away_status_page

    @allure.story("custom_away_status_page_check_title")
    @pytest.mark.smoke
    @pytest.mark.globalpage
    def test_custom_away_status_page_check_title(self, init_page):
        init_page.check_both_titles("Custom Away Status")
```
#### GlobalPage: New Away Status Page

**Page Object File**: [`testCases/uiPages/globalpage/custom_away_status/new_away_status_page.py`]

```python
from uiPages.base_page import BasePage

class NewAwayStatusPage(BasePage):
    def __init__(self, page):
        super().__init__(page)
        self.path = "/global/people/customawaystatus/new"
```

**Test Case File**: [`testCases/uiTestCases/globalpage/custom_away_status/new_away_status_page.py`]

```python
from testCases.uiPages.globalpage.custom_away_status.new_away_status_page import (
    NewAwayStatusPage,
)
import pytest
import allure

@allure.feature("globalpage_new_away_status_page")
class TestNewAwayStatusPage:
    @pytest.fixture(scope="function")
    def init_page(self, login, page):
        new_away_status_page = NewAwayStatusPage(page)
        new_away_status_page.goto(
            prefix=login["dash_ui_url"], path=new_away_status_page.path, suffix=f""
        )
        return new_away_status_page  

    @allure.story("new_away_status_page_check_title")
    @pytest.mark.smoke
    @pytest.mark.globalpage
    def test_new_away_status_page_check_title(self, init_page):
        init_page.check_both_titles("New Away Status")
```
#### GlobalPage: Edit Away Status Page

**Page Object File**: [`testCases/uiPages/globalpage/custom_away_status/edit_away_status_page.py`]

```python
from uiPages.base_page import BasePage

class EditAwayStatusPage(BasePage):
    def __init__(self, page):
        super().__init__(page)
        self.path = "/global/people/customawaystatus/edit"
```

**Test Case File**: [`testCases/uiTestCases/globalpage/custom_away_status/edit_away_status_page.py`]

```python
from testCases.uiPages.globalpage.custom_away_status.edit_away_status_page import (
    EditAwayStatusPage,
)
import pytest
import allure

@allure.feature("globalpage_edit_away_status_page")
class TestEditAwayStatusPage:
    @pytest.fixture(scope="function")
    def init_page(self, login, create_away_status, page):
        id = create_away_status.json()["id"]

        edit_away_status_page = EditAwayStatusPage(page)
        edit_away_status_page.goto(
            prefix=login["dash_ui_url"], path=edit_away_status_page.path, suffix=f"?agentawaystatusid="+id
        )
        return edit_away_status_page

    @allure.story("edit_away_status_page_check_title")
    @pytest.mark.smoke
    @pytest.mark.globalpage
    def test_edit_away_status_page_check_title(self, init_page):
        init_page.check_both_titles("Edit Away Status")
```

#### GlobalPage: Agent Chats Page

**Page Object File**: [`testCases/uiPages/globalpage/agent_chats/agent_chats_page.py`]

```python
from uiPages.base_page import BasePage

class AgentChatsPage(BasePage):
    def __init__(self, page):
        super().__init__(page)
        self.path = "/global/people/agentchats/"
```

**Test Case File**: [`testCases/uiTestCases/globalpage/agent_chats/agent_chats_page.py`]

```python
from testCases.uiPages.globalpage.agent_chats.agent_chats_page import (
    AgentChatsPage,
)
import pytest
import allure

@allure.feature("globalpage_agent_chats_page")
class TestAgentChatsPage:
    @pytest.fixture(scope="function")
    def init_page(self, login, page):
        agent_chats_page = AgentChatsPage(page)
        agent_chats_page.goto(
            prefix=login["dash_ui_url"], path=agent_chats_page.path, suffix=f""
        )
        return agent_chats_page

    @allure.story("agent_chats_page_check_title")
    @pytest.mark.smoke
    @pytest.mark.globalpage
    def test_agent_chats_page_check_title(self, init_page):
        init_page.check_both_titles("Agent Chats")
```


### Hints

1. For {page_title}, if it's empty, please use the value of {page_name}. If it's not empty, please use the value of {page_title}.
2. For {menu_name}, if it's empty, please use the value of {page_name}. If it's not empty, please use the value of {menu_name}. Either way, you need to convert it to snake_case and lower-case.

### This is the List of Pages and Attributes. You need to create the files for these pages.

| module_name  | menu_name | page_name          | page_title | path                                     | suffix_querystring_key | set_up_fixture   |
| ------------ | --------- | ------------------ | ---------- | ---------------------------------------- | ---------------------- | ---------------- |
| globalpage | Skills   | Skills      |            | /global/people/skills/             |                        |                  |
| globalpage | Skills   | New Skill   | New Skill    | /global/people/skills/new   |                        |                  |
| globalpage | Skills   | Edit Skill   | Edit Skill  | /global/people/skills/edit   |?skillid=      | create_skill_id |
| globalpage | Roles   | Roles      |            | /global/people/roles/             |                        |                  |
| globalpage | Roles   | New Role   | New Role    | /global/people/roles/new   |                        |                  |
| globalpage | Roles   | Edit Role   | Edit Role  | /global/people/roles/edit   |?roleid=      | create_role_id |
| globalpage | Custom Away Status | Custom Away Status |            | /global/people/customawaystatus/  |                        |                  |
| globalpage | Custom Away Status | New Away Status | New Away Status  | /global/people/customawaystatus/new |               |                  |
| globalpage | Custom Away Status | Edit Away Status | Edit Away Status | /global/people/customawaystatus/edit |?agentawaystatusid= | create_agentawaystatus_id |
| globalpage | Agent Chats   | Agent Chats   |            | /global/people/agentchats/             |                        |                  |

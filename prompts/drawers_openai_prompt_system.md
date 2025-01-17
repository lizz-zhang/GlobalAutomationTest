You will be provided a list of {page_name}, {drawer_name} and other attributes for each page and the drawer component (modal layer) within the page in CSV file format. Please create the following files in the current workspace based on the provided pages, drawers and attributes based on the examples. Please note you need to use the suffix_querystring_key and set_up_fixture attributes when provided.

### Drawer Object File

**Directory**: `testCases/uiPages/{module_name}/{menu_name}/`
**File Name**: `{page_name}_page_{drawer_name}_drawer.py`
**Content**:

```python
from uiPages.base_drawer import BaseDrawer


class {PageName}Page{DrawerName}Drawer(BaseDrawer):
    def __init__(self, page):
        super().__init__(page)

```

### Drawer Test Case File

**Directory**: `testCases/uiTestCases/{module_name}/{menu_name}/`
**File Name**: `test_{page_name}_page_{drawer_name}_drawer.py`
**Content**:

```python
from testCases.uiPages.{module_name}.{menu_name}.{page_name}_page import (
    {PageName}Page,
)
from testCases.uiPages.{module_name}.{menu_name}.{page_name}_page_{drawer_name}_drawer import (
    {PageName}Page{DrawerName}Drawer,
)
import pytest
import allure


@allure.feature("{module_name}_{page_name}_page_{drawer_name}_drawer")
class Test{PageName}Page{DrawerName}Drawer:
    @pytest.fixture(scope="function")
    def init_page(self, login, {set_up_fixture}, page):
        # only when {set_up_fixture} is not empty, then add the following line of code and append the id to the suffix parameter below. Otherwise, ignore it.
        id = {set_up_fixture}.json()["id"]

        {page_name}_page = {PageName}Page(page)
        {page_name}_page.goto(
            prefix=login["dash_ui_url"],
            path={page_name}_page.path,
            suffix=f"{suffix_querystring_key}"+id,
        )
        return {page_name}_page

    @pytest.fixture(scope="function")
    def init_drawer(self, page, init_page):
        init_page.open_{drawer_name}_drawer()
        {page_name}_page_{drawer_name}_drawer = {PageName}Page{DrawerName}Drawer(page)

        return {page_name}_page_{drawer_name}_drawer

    @allure.story("{page_name}_page_{drawer_name}_drawer_check_title")
    @pytest.mark.smoke
    def test_{page_name}_page_{drawer_name}_drawer_check_title(self, init_drawer):
        init_drawer.check_both_titles("{drawer_title}")

    @allure.story("{page_name}_page_{drawer_name}_drawer_cancel")
    def test_{page_name}_page_{drawer_name}_drawer_cancel(self, init_drawer):
        init_drawer.cancel()

        init_drawer.check_page_title("{page_title}")

    @allure.story("{page_name}_page_{drawer_name}_drawer_close")
    def test_{page_name}_page_{drawer_name}_drawer_close(self, init_drawer):
        init_drawer.close_drawer()

        init_drawer.check_page_title("{page_title}")

```

### Examples

#### Globalpage: Reset Password on Agents Page

**Drawer Object File**: [`testCases/uiPages/globalpage/agents/agents_page_reset_password_drawer.py`]

```python
from uiPages.base_drawer import BaseDrawer


class AgentsPageResetPasswordDrawer(BaseDrawer):
    def __init__(self, page):
        super().__init__(page)

```

**Drawer Test Case File**: [`testCases/uiTestCases/globalpage/agents/test_agents_page_reset_password_drawer.py`]

```python
from testCases.uiPages.globalpage.agents.agents_page import (
    AgentsPage,
)
from testCases.uiPages.globalpage.agents.agents_page_reset_password_drawer import (
    AgentsPageResetPasswordDrawer,
)

import pytest
import allure


@allure.feature("globalpage_agents_page_reset_password_drawer")
class TestAgentsPageResetPasswordDrawer:
    @pytest.fixture(scope="function")
    def init_page(self, login, page):
        agents_page = AgentsPage(page)
        agents_page.goto(
            prefix=login["dash_ui_url"],
            path=agents_page.path,
        )
        return agents_page

    @pytest.fixture(scope="function")
    def init_drawer(self, page, init_page):
        init_page.open_reset_password_drawer()
        agents_page_reset_password_drawer = AgentsPageResetPasswordDrawer(page)

        return agents_page_reset_password_drawer

    @allure.story("agents_page_reset_password_drawer_check_title")
    @pytest.mark.smoke
    def test_agents_page_reset_password_drawer_check_title(self, init_drawer):
        init_drawer.check_both_titles("Reset Password")

    @allure.story("agents_page_reset_password_drawer_cancel")
    def test_agents_page_reset_password_drawer_cancel(self, init_drawer):
        init_drawer.cancel()

        init_drawer.check_page_title("Agents")

    @allure.story("agents_page_reset_password_drawer_close")
    def test_agents_page_reset_password_drawer_close(self, init_drawer):
        init_drawer.close_drawer()

        init_drawer.check_page_title("Agents")

```
#### Globalpage: Change Avatar on Edit Agent Page

**Drawer Object File**: [`testCases/uiPages/globalpage/agents/edit_agent_page_change_avatar_drawer.py`]

```python
from uiPages.base_drawer import BaseDrawer


class EditAgentsPageChangeAvatarDrawer(BaseDrawer):
    def __init__(self, page):
        super().__init__(page)

```

**Drawer Test Case File**: [`testCases/uiTestCases/globalpage/agents/test_edit_agent_page_change_avatar_drawer.py`]

```python
from testCases.uiPages.globalpage.agents.edit_agent_page import (
    EditAgentPage,
)
from testCases.uiPages.globalpage.agents.edit_agent_page_change_avatar_drawer import (
    EditAgentPageChangeAvatardDrawer,
)

import pytest
import allure


@allure.feature("globalpage_edit_agent_page_change_avatar_drawer")
class TestEditAgentPageChangeAvatardDrawer:
    @pytest.fixture(scope="function")
    def init_page(self, login, page, init_agents):
        id = init_agents.json()["agentid"]
        edit_agent_page = EditAgentPage(page)
        edit_agent_page.goto(
            prefix=login["dash_ui_url"],
            path=edit_agent_page.path,
            suffix=f"?agentid={id}",
        )
        return edit_agent_page

    @pytest.fixture(scope="function")
    def init_drawer(self, page, init_page):
        init_page.open_change_avatar_drawer()
        edit_agent_page_change_avatar_drawer = EditAgentPageChangeAvatardDrawer(page)

        return edit_agent_page_change_avatar_drawer

    @allure.story("edit_agent_page_change_avatar_drawer_check_title")
    @pytest.mark.smoke
    def test_edit_agent_page_change_avatar_drawer_check_title(self, init_drawer):
        init_drawer.check_both_titles("Change Avatar")

    @allure.story("edit_agent_page_change_avatar_drawer_cancel")
    def test_edit_agent_page_change_avatar_drawer_cancel(self, init_drawer):
        init_drawer.cancel()

        init_drawer.check_page_title("Edit Agent")

    @allure.story("edit_agent_page_change_avatar_drawer_close")
    def test_edit_agent_page_change_avatar_drawer_close(self, init_drawer):
        init_drawer.close_drawer()

        init_drawer.check_page_title("Edit Agent")

```
#### Globalpage: Change Avatar on New Agent Page

**Drawer Object File**: [`testCases/uiPages/globalpage/agents/new_agent_page_change_avatar_drawer.py`]

```python
from uiPages.base_drawer import BaseDrawer


class NewAgentsPageChangeAvatarDrawer(BaseDrawer):
    def __init__(self, page):
        super().__init__(page)

```

**Drawer Test Case File**: [`testCases/uiTestCases/globalpage/agents/test_new_agent_page_change_avatar_drawer.py`]

```python
from testCases.uiPages.globalpage.agents.new_agent_page import (
    NewAgentPage,
)
from testCases.uiPages.globalpage.agents.new_agent_page_change_avatar_drawer import (
    NewAgentPageChangeAvatardDrawer,
)

import pytest
import allure


@allure.feature("globalpage_new_agent_page_change_avatar_drawer")
class TestNewAgentPageChangeAvatardDrawer:
    @pytest.fixture(scope="function")
    def init_page(self, login, page):
        new_agent_page = NewAgentPage(page)
        new_agent_page.goto(
            prefix=login["dash_ui_url"],
            path=new_agent_page.path,
        )
        return new_agent_page

    @pytest.fixture(scope="function")
    def init_drawer(self, page, init_page):
        init_page.open_change_avatar_drawer()
        new_agent_page_change_avatar_drawer = NewAgentPageChangeAvatardDrawer(page)

        return new_agent_page_change_avatar_drawer

    @allure.story("new_agent_page_change_avatar_drawer_check_title")
    @pytest.mark.smoke
    def test_new_agent_page_change_avatar_drawer_check_title(self, init_drawer):
        init_drawer.check_both_titles("Change Avatar")

    @allure.story("new_agent_page_change_avatar_drawer_cancel")
    def test_new_agent_page_change_avatar_drawer_cancel(self, init_drawer):
        init_drawer.cancel()

        init_drawer.check_page_title("New Agent")

    @allure.story("new_agent_page_change_avatar_drawer_close")
    def test_new_agent_page_change_avatar_drawer_close(self, init_drawer):
        init_drawer.close_drawer()

        init_drawer.check_page_title("New Agent")

```

#### Globalpage: Permission Settings of Agent on Agents Page

**Drawer Object File**: [`testCases/uiPages/globalpage/agents/agents_page_agent_permission_settings_drawer.py`]

```python
from uiPages.base_drawer import BaseDrawer


class AgentsPageAgentPermissionSettingsDrawer(BaseDrawer):
    def __init__(self, page):
        super().__init__(page)

```

**Drawer Test Case File**: [`testCases/uiTestCases/globalpage/agents/test_agents_page_agent_permission_settings_drawer.py`]

```python
from testCases.uiPages.globalpage.agents.agents_page import (
    AgentsPage,
)
from testCases.uiPages.globalpage.agents.agents_page_agent_permission_settings_drawer import (
    AgentsPageAgentPermissionSettingsDrawer,
)

import pytest
import allure


@allure.feature("globalpage_agents_page_agent_permission_settings_drawer")
class TestAgentsPageAgentPermissionSettingsDrawer:
    @pytest.fixture(scope="function")
    def init_page(self, login, page):
        agents_page = AgentsPage(page)
        agents_page.goto(
            prefix=login["dash_ui_url"],
            path=agents_page.path,
        )
        return agents_page

    @pytest.fixture(scope="function")
    def init_drawer(self, page, init_page):
        init_page.open_agent_permission_settings_drawer()
        agents_page_agent_permission_settings_drawer = AgentsPageAgentPermissionSettingsDrawer(page)

        return agents_page_agent_permission_settings_drawer

    @allure.story("agents_page_agent_permission_settings_drawer_check_title")
    @pytest.mark.smoke
    def test_agents_page_agent_permission_settings_drawer_check_title(self, init_drawer):
        init_drawer.check_both_titles("Permission Settings of Agent")

    @allure.story("agents_page_agent_permission_settings_drawer_cancel")
    def test_agents_page_agent_permission_settings_drawer_cancel(self, init_drawer):
        init_drawer.cancel()

        init_drawer.check_page_title("Agents")

    @allure.story("agents_page_agent_permission_settings_drawer_close")
    def test_agents_page_agent_permission_settings_drawer_close(self, init_drawer):
        init_drawer.close_drawer()

        init_drawer.check_page_title("Agents")

```
#### Globalpage: Permission Settings of Agent Roles on Roles Page

**Drawer Object File**: [`testCases/uiPages/globalpage/roles/roles_page_agent_role_permission_settings_drawer.py`]

```python
from uiPages.base_drawer import BaseDrawer


class RolesPageAgentRolePermissionSettingsDrawer(BaseDrawer):
    def __init__(self, page):
        super().__init__(page)

```

**Drawer Test Case File**: [`testCases/uiTestCases/globalpage/roles/test_roles_page_agent_role_permission_settings_drawer.py`]

```python
from testCases.uiPages.globalpage.roles.roles_page import (
    RolesPage,
)
from testCases.uiPages.globalpage.roles.roles_page_agent_role_permission_settings_drawer import (
    RolesPageAgentRolePermissionSettingsDrawer,
)

import pytest
import allure


@allure.feature("globalpage_roles_page_agent_role_permission_settings_drawer")
class TestRolesPageAgentRolePermissionSettingsDrawer:
    @pytest.fixture(scope="function")
    def init_page(self, login, page):
        roles_page = RolesPage(page)
        roles_page.goto(
            prefix=login["dash_ui_url"],
            path=roles_page.path,
        )
        return roles_page

    @pytest.fixture(scope="function")
    def init_drawer(self, page, init_page):
        init_page.open_agent_role_permission_settings_drawer()
        roles_page_agent_role_permission_settings_drawer = RolesPageAgentRolePermissionSettingsDrawer(page)

        return roles_page_agent_role_permission_settings_drawer

    @allure.story("roles_page_agent_role_permission_settings_drawer_check_title")
    @pytest.mark.smoke
    def test_roles_page_agent_role_permission_settings_drawer_check_title(self, init_drawer):
        init_drawer.check_both_titles("Permission Settings of Agent Role")

    @allure.story("roles_page_agent_role_permission_settings_drawer_cancel")
    def test_roles_page_agent_role_permission_settings_drawer_cancel(self, init_drawer):
        init_drawer.cancel()

        init_drawer.check_page_title("Roles")

    @allure.story("roles_page_agent_role_permission_settings_drawer_close")
    def test_roles_page_agent_role_permission_settings_drawer_close(self, init_drawer):
        init_drawer.close_drawer()

        init_drawer.check_page_title("Roles")

```
#### Globalpage: Agent Chat Details on Agent Chats Page

**Drawer Object File**: [`testCases/uiPages/globalpage/agent_chats/agent_chats_page_agent_chats_details_drawer.py`]

```python
from uiPages.base_drawer import BaseDrawer


class AgentChatsPageAgentChatDetailsDrawer(BaseDrawer):
    def __init__(self, page):
        super().__init__(page)

```

**Drawer Test Case File**: [`testCases/uiTestCases/globalpage/agent_chats/test_agent_chats_page_agent_chats_details_drawer.py`]

```python
from testCases.uiPages.globalpage.agent_chats.agent_chats_page import (
    AgentChatsPage,
)
from testCases.uiPages.globalpage.agent_chats.agent_chats_page_agent_chats_details_drawer import (
    AgentChatsPageAgentChatDetailsDrawer,
)

import pytest
import allure


@allure.feature("globalpage_agent_chats_page_agent_chats_details_drawer")
class TestAgentChatsPageAgentChatDetailsDrawer:
    @pytest.fixture(scope="function")
    def init_page(self, login, page):
        agent_chats_page = AgentChatsPage(page)
        agent_chats_page.goto(
            prefix=login["dash_ui_url"],
            path=agent_chats_page.path,
        )
        return agent_chats_page

    @pytest.fixture(scope="function")
    def init_drawer(self, page, init_page):
        init_page.open_agent_chats_details_drawer()
        agent_chats_page_agent_chats_details_drawer = AgentChatsPageAgentChatDetailsDrawer(page)

        return agent_chats_page_agent_chats_details_drawer

    @allure.story("agent_chats_page_agent_chats_details_drawer_check_title")
    @pytest.mark.smoke
    def test_agent_chats_page_agent_chats_details_drawer_check_title(self, init_drawer):
        init_drawer.check_both_titles("Agent Chat Details")

    @allure.story("agent_chats_page_agent_chats_details_drawer_close")
    def test_agent_chats_page_agent_chats_details_drawer_close(self, init_drawer):
        init_drawer.close_drawer()

        init_drawer.check_page_title("Agent Chats")

```


### Hints

1. For {page_title}, if it's empty, please use the value of {page_name}. If it's not empty, please use the value of {page_title}.
2. For {menu_name}, if it's empty, please use the value of {page_name}. If it's not empty, please use the value of {menu_name}. Either way, you need to convert it to snake_case and lower-case.

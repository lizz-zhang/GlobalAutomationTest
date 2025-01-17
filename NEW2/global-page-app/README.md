# README for Global Page Application

## Overview

The Global Page Application is designed to manage various global pages within a user interface. It includes functionalities for skills, roles, custom away statuses, and agent chats. Each section is organized into page objects and corresponding test cases to ensure functionality and reliability.

## Project Structure

The project is structured as follows:

```
global-page-app
├── testCases
│   ├── uiPages
│   │   ├── globalpage
│   │   │   ├── agent_chats
│   │   │   │   └── agent_chats_page.py
│   │   │   ├── custom_away_status
│   │   │   │   ├── custom_away_status_page.py
│   │   │   │   ├── edit_away_status_page.py
│   │   │   │   └── new_away_status_page.py
│   │   │   ├── roles
│   │   │   │   ├── edit_role_page.py
│   │   │   │   ├── new_role_page.py
│   │   │   │   └── roles_page.py
│   │   │   ├── skills
│   │   │   │   ├── edit_skill_page.py
│   │   │   │   ├── new_skill_page.py
│   │   │   │   └── skills_page.py
│   ├── uiTestCases
│   │   ├── globalpage
│   │   │   ├── agent_chats
│   │   │   │   └── test_agent_chats_page.py
│   │   │   ├── custom_away_status
│   │   │   │   ├── test_custom_away_status_page.py
│   │   │   │   ├── test_edit_away_status_page.py
│   │   │   │   └── test_new_away_status_page.py
│   │   │   ├── roles
│   │   │   │   ├── test_edit_role_page.py
│   │   │   │   ├── test_new_role_page.py
│   │   │   │   └── test_roles_page.py
│   │   │   ├── skills
│   │   │   │   ├── test_edit_skill_page.py
│   │   │   │   ├── test_new_skill_page.py
│   │   │   │   └── test_skills_page.py
```

## Features

- **Skills Management**: Create, edit, and view skills.
- **Roles Management**: Create, edit, and view roles.
- **Custom Away Status**: Manage custom away statuses for users.
- **Agent Chats**: View and manage agent chats.

## Testing

The application includes a comprehensive suite of tests for each page to ensure functionality. Tests are organized by page and include fixtures for initializing pages.

## Getting Started

To get started with the Global Page Application, clone the repository and install the necessary dependencies. Run the test suite to ensure everything is functioning as expected.

## Contributing

Contributions are welcome! Please submit a pull request or open an issue for any enhancements or bug fixes.

## License

This project is licensed under the MIT License.
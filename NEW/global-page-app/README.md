# Global Page Application

This project is designed to manage and test the global pages of the application. It includes page object files and corresponding test case files for various sections such as subscriptions, agents, and departments.

## Project Structure

The project is organized as follows:

```
global-page-app
├── testCases
│   ├── uiPages
│   │   ├── globalpage
│   │   │   ├── subscriptions
│   │   │   │   ├── subscriptions_page.py
│   │   │   │   ├── add_more_subscriptions_page.py
│   │   │   ├── agents
│   │   │   │   ├── agents_page.py
│   │   │   │   ├── new_agent_page.py
│   │   │   │   ├── edit_agent_page.py
│   │   │   ├── departments
│   │   │   │   ├── departments_page.py
│   │   │   │   ├── new_department_page.py
│   │   │   │   ├── edit_department_page.py
│   ├── uiTestCases
│   │   ├── globalpage
│   │   │   ├── subscriptions
│   │   │   │   ├── test_subscriptions_page.py
│   │   │   │   ├── test_add_more_subscriptions_page.py
│   │   │   ├── agents
│   │   │   │   ├── test_agents_page.py
│   │   │   │   ├── test_new_agent_page.py
│   │   │   │   ├── test_edit_agent_page.py
│   │   │   ├── departments
│   │   │   │   ├── test_departments_page.py
│   │   │   │   ├── test_new_department_page.py
│   │   │   │   ├── test_edit_department_page.py
├── README.md
```

## Features

- **Page Object Model**: Each page is represented by a class that encapsulates the page's properties and behaviors.
- **Test Cases**: Each page has corresponding test cases to verify functionality and ensure the application behaves as expected.

## Getting Started

1. Clone the repository.
2. Install the required dependencies.
3. Run the test cases to verify the functionality of the global pages.

## Contributing

Contributions are welcome! Please submit a pull request or open an issue for any enhancements or bug fixes.
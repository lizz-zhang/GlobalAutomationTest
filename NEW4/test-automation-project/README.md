# Test Automation Project

This project is designed for automated testing of various web pages using a structured approach. It includes page object models and corresponding test cases for each page.

## Project Structure

The project is organized into the following directories:

- **testCases**
  - **uiPages**: Contains the page object files that define the structure and behavior of each page.
    - **globalpage**: Contains page objects for global pages such as:
      - Agent Single Sign-On
      - Audit Log
      - OAuth Client
      - Secure Forms
  - **uiTestCases**: Contains the test case files that implement the tests for each page.
    - **globalpage**: Contains test cases for global pages corresponding to the page objects.

## Page Object Files

Each page object file defines a class that inherits from `BasePage`. The class initializes the page with a specific path. Here are some examples:

- **Agent Single Sign-On Page**: `testCases/uiPages/globalpage/agent_single_sign_on/agent_single_sign_on_page.py`
- **Audit Log Page**: `testCases/uiPages/globalpage/audit_log/audit_log_page.py`
- **OAuth Client Page**: `testCases/uiPages/globalpage/oauth_client/oauth_client_page.py`
- **Secure Forms Page**: `testCases/uiPages/globalpage/secure_forms/secure_forms_page.py`

## Test Case Files

Each test case file defines a class that contains fixtures to set up the test environment and methods to verify the page titles. Examples include:

- **Test Agent Single Sign-On Page**: `testCases/uiTestCases/globalpage/agent_single_sign_on/test_agent_single_sign_on_page.py`
- **Test Audit Log Page**: `testCases/uiTestCases/globalpage/audit_log/test_audit_log_page.py`
- **Test OAuth Client Page**: `testCases/uiTestCases/globalpage/oauth_client/test_oauth_client_page.py`
- **Test Secure Forms Page**: `testCases/uiTestCases/globalpage/secure_forms/test_secure_forms_page.py`

## Usage

To run the tests, ensure that the necessary dependencies are installed and execute the test suite using your preferred test runner.

## Contribution

Contributions to enhance the project are welcome. Please follow the standard practices for contributing to open-source projects.
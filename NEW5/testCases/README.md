# README.md

# Test Cases Project

This project contains automated test cases for various UI pages in the application. The tests are organized into two main directories: `uiPages` for the page object models and `uiTestCases` for the corresponding test cases.

## Directory Structure

- **uiPages**: Contains the page object files that define the structure and behavior of each page.
  - **billing**: Contains pages related to billing.
    - `billing_profile_page.py`: Defines the `BillingProfilePage` class.
    - `invoices_page.py`: Defines the `InvoicesPage` class.
  - **globalpage**: Contains global pages.
    - **custom_smtp_servers**: Contains pages related to custom SMTP servers.
      - `custom_smtp_servers_page.py`: Defines the `CustomSMTPServersPage` class.
      - `edit_custom_smtp_server_page.py`: Defines the `EditCustomSMTPServerPage` class.
      - `new_custom_smtp_server_page.py`: Defines the `NewCustomSMTPServerPage` class.
    - `password_policy_page.py`: Defines the `PasswordPolicyPage` class.
    - `site_profile_page.py`: Defines the `SiteProfilePage` class.
    - `two_factor_auth_page.py`: Defines the `TwoFactorAuthenticationPage` class.
  
- **uiTestCases**: Contains the test case files that validate the functionality of each page.
  - **billing**: Contains test cases related to billing.
    - `test_billing_profile_page.py`: Tests the `BillingProfilePage`.
    - `test_invoices_page.py`: Tests the `InvoicesPage`.
  - **globalpage**: Contains test cases for global pages.
    - **custom_smtp_servers**: Contains test cases for custom SMTP server pages.
      - `test_custom_smtp_servers_page.py`: Tests the `CustomSMTPServersPage`.
      - `test_edit_custom_smtp_server_page.py`: Tests the `EditCustomSMTPServerPage`.
      - `test_new_custom_smtp_server_page.py`: Tests the `NewCustomSMTPServerPage`.
    - `test_password_policy_page.py`: Tests the `PasswordPolicyPage`.
    - `test_site_profile_page.py`: Tests the `SiteProfilePage`.
    - `test_two_factor_auth_page.py`: Tests the `TwoFactorAuthenticationPage`.

## Usage

To run the tests, ensure you have the necessary dependencies installed and execute the test suite using your preferred test runner.

## Contribution

Feel free to contribute to this project by adding new test cases or improving existing ones. Please ensure that all tests are well-documented and follow the project's coding standards.
# README.md

# Login Project

This project is designed to test the login functionalities of a web application, specifically focusing on the "Sign in with SSO" and "Forgot your password" pages. It utilizes the pytest framework for testing and allure for reporting.

## Project Structure

The project is organized as follows:

```
login-project
├── testCases
│   ├── uiPages
│   │   └── login
│   │       ├── dash_sign_in_with_sso
│   │       │   └── dash_sign_in_with_sso_page.py
│   │       └── dash_forgot_your_password
│   │           └── dash_forgot_your_password_page.py
│   └── uiTestCases
│       └── login
│           ├── dash_sign_in_with_sso
│           │   └── test_dash_sign_in_with_sso_page.py
│           └── dash_forgot_your_password
│               └── test_dash_forgot_your_password_page.py
├── README.md
└── requirements.txt
```

## Pages

1. **Sign in with SSO**
   - Located at: `testCases/uiPages/login/dash_sign_in_with_sso/dash_sign_in_with_sso_page.py`
   - Class: `DashSignInWithSSOPage`
   - Path: `/login/sso`

2. **Forgot your password**
   - Located at: `testCases/uiPages/login/dash_forgot_your_password/dash_forgot_your_password_page.py`
   - Class: `DashForgotYourPasswordPage`
   - Path: `/login/forgotpassword`

## Test Cases

- **Sign in with SSO Page Tests**
  - Located at: `testCases/uiTestCases/login/dash_sign_in_with_sso/test_dash_sign_in_with_sso_page.py`
  - Class: `TestDashSignInWithSSOPage`
  - Tests the title of the Sign in with SSO page.

- **Forgot your password Page Tests**
  - Located at: `testCases/uiTestCases/login/dash_forgot_your_password/test_dash_forgot_your_password_page.py`
  - Class: `TestDashForgotYourPasswordPage`
  - Tests the title of the Forgot your password page.

## Requirements

To install the necessary dependencies, please refer to the `requirements.txt` file.
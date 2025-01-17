# Page Object Generator

This project is designed to automate the generation of page object files and corresponding test case files for UI testing. It follows a structured approach to organize the code and ensure maintainability.

## Project Structure

The project contains the following directories and files:

```
page-object-generator
├── testCases
│   ├── uiPages
│   │   ├── module_name
│   │   │   ├── menu_name
│   │   │   │   ├── edit_banned_ip_page.py
│   │   │   │   └── cookie_restriction_page.py
│   ├── uiTestCases
│   │   ├── module_name
│   │   │   ├── menu_name
│   │   │   │   ├── test_edit_banned_ip_page.py
│   │   │   │   └── test_cookie_restriction_page.py
├── generate_files.py
└── README.md
```

## File Descriptions

- **testCases/uiPages/livechatpage/ban_list/edit_banned_ip_page.py**: Contains the `EditBannedIPPage` class, which inherits from `BasePage`. It initializes with a page parameter and sets the path to `/livechat/settings/banlist/bannedip/edit`.

- **testCases/uiPages/livechatpage/ban_list/cookie_restriction_page.py**: Contains the `CookieRestrictionPage` class, which inherits from `BasePage`. It initializes with a page parameter and sets the path to `/livechat/settings/cookierestriction/`.

- **testCases/uiTestCases/livechatpage/ban_list/test_edit_banned_ip_page.py**: Contains the `TestEditBannedIPPage` class, which uses `pytest` and `allure` for testing. It includes a fixture `init_page` that sets up the `EditBannedIPPage` and a test method `test_edit_banned_ip_page_check_title` that checks the title of the page.

- **testCases/uiTestCases/livechatpage/ban_list/test_cookie_restriction_page.py**: Contains the `TestCookieRestrictionPage` class, which uses `pytest` and `allure` for testing. It includes a fixture `init_page` that sets up the `CookieRestrictionPage` and a test method `test_cookie_restriction_page_check_title` that checks the title of the page.

- **generate_files.py**: Responsible for generating the page object files and test case files based on the provided attributes.

## Usage

To generate the page object and test case files, run the `generate_files.py` script. Ensure that the necessary attributes are provided for the pages you wish to create.

## Contributing

Contributions are welcome! Please feel free to submit a pull request or open an issue for any enhancements or bug fixes.
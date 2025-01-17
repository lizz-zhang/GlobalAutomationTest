# GlobalPage Canned Messages Project

This project contains the implementation of the GlobalPage Canned Messages feature, which includes both public and private canned messages. The project is structured to facilitate easy navigation and testing of the various pages related to canned messages.

## Project Structure

```
globalpage-canned-messages
├── testCases
│   ├── uiPages
│   │   └── globalpage
│   │       └── canned_messages
│   │           ├── public_canned_messages_page.py
│   │           ├── new_public_canned_message_page.py
│   │           ├── edit_public_canned_message_page.py
│   │           ├── private_canned_messages_page.py
│   │           ├── new_private_canned_message_page.py
│   │           └── edit_private_canned_message_page.py
│   └── uiTestCases
│       └── globalpage
│           └── canned_messages
│               ├── test_public_canned_messages_page.py
│               ├── test_new_public_canned_message_page.py
│               ├── test_edit_public_canned_message_page.py
│               ├── test_private_canned_messages_page.py
│               ├── test_new_private_canned_message_page.py
│               └── test_edit_private_canned_message_page.py
└── README.md
```

## Overview of Files

- **Page Object Files**: These files define the structure and behavior of the various pages related to canned messages.
  - `public_canned_messages_page.py`: Contains the `PublicCannedMessagesPage` class.
  - `new_public_canned_message_page.py`: Contains the `NewPublicCannedMessagePage` class.
  - `edit_public_canned_message_page.py`: Contains the `EditPublicCannedMessagePage` class.
  - `private_canned_messages_page.py`: Contains the `PrivateCannedMessagesPage` class.
  - `new_private_canned_message_page.py`: Contains the `NewPrivateCannedMessagePage` class.
  - `edit_private_canned_message_page.py`: Contains the `EditPrivateCannedMessagePage` class.

- **Test Case Files**: These files contain the test cases for each of the page objects.
  - `test_public_canned_messages_page.py`: Tests the `PublicCannedMessagesPage`.
  - `test_new_public_canned_message_page.py`: Tests the `NewPublicCannedMessagePage`.
  - `test_edit_public_canned_message_page.py`: Tests the `EditPublicCannedMessagePage`.
  - `test_private_canned_messages_page.py`: Tests the `PrivateCannedMessagesPage`.
  - `test_new_private_canned_message_page.py`: Tests the `NewPrivateCannedMessagePage`.
  - `test_edit_private_canned_message_page.py`: Tests the `EditPrivateCannedMessagePage`.

## Getting Started

To get started with this project, clone the repository and navigate to the project directory. You can run the test cases using a test runner like pytest.

## Contributing

Contributions are welcome! Please feel free to submit a pull request or open an issue for any enhancements or bug fixes.
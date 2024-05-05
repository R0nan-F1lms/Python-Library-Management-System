# Library Management System

The Library Management System is a Python application designed to manage a library's operations including book management, member management, and transaction tracking.

## Installation

1. Clone the repository to your local machine:

    ```bash
    git clone <repository-url>
    ```

2. Navigate to the project directory:

    ```bash
    cd LibraryManagement
    ```

3. Set up a virtual environment (optional but recommended):

    ```bash
    python -m venv .venv
    ```

4. Activate the virtual environment:

    On Windows:

    ```bash
    .venv\Scripts\activate
    ```

    On macOS and Linux:

    ```bash
    source .venv/bin/activate
    ```

5. Install the required dependencies:

    ```bash
    pip install -r requirements.txt
    ```

## Usage

1. Make sure your virtual environment is activated (if you set one up).

2. Run the `program.py` file:

    ```bash
    python program.py
    ```

3. Follow the on-screen instructions to interact with the Library Management System.

## Features

- **Book Management**: Add, edit, and view books in the library's collection.
- **Member Management**: Add, edit, and view library members.
- **Transaction Tracking**: Track book borrowing and return transactions.
- **Staff Permissions**: Differentiate between staff roles (teller, admin) with varying permissions.
- **Subcommands**: Use subcommands to view specific subsets of books, members, and transactions.

## Contributing

Contributions are welcome! If you'd like to contribute to the project, please follow these steps:

1. Fork the repository.
2. Create a new branch for your feature or bug fix.
3. Make your changes.
4. Test your changes thoroughly.
5. Create a pull request.

## License

This project is licensed under the MIT License

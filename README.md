# Enhanced CRUD API with Flask and SQLite

This project is an enhanced version of a simple CRUD API built with Flask and SQLite. It includes comprehensive testing, improved dependency management, and a modular project structure.

## Features

- **RESTful API**: Full CRUD operations for a game resource.
- **Comprehensive Testing**: Automated tests using `pytest` and Flask's test client, covering all CRUD operations and error handling.
- **Separate Test Database**: Tests use a dedicated test database (`test_games.db`) to ensure a clean state.
- **Dependency Management**: Updated `requirements.txt` with all necessary packages for testing and API development.
- **Modular Structure**: Separated API logic, database handling, and application entry points for better maintainability.

## Installation

1. Clone the repository:
   ```bash
   git clone <repository-url>
   cd Sample-CRUD-Python-Flask-SQLite-master
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Run the application:
   ```bash
   python main.py
   ```

## Running Tests

To run the tests, use the following command:
```bash
python -m pytest test_api.py -v
```

To suppress deprecation warnings, use:
```bash
python -m pytest test_api.py -v -W ignore::DeprecationWarning
```

## Project Structure

- `main.py`: Application entry point and route definitions.
- `api.py`: API blueprint and resource definitions.
- `game_controller.py`: Business logic for game operations.
- `db.py`: Database connection and table creation.
- `test_api.py`: Comprehensive test suite for the API.
- `templates/`: HTML templates for the web interface.

## License

This project is licensed under the MIT License - see the LICENSE file for details.

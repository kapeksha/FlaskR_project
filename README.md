# TodoMVC API

A simple TodoMVC API built with Flask and Flask-RESTX.

## Description

This is a simple TodoMVC API that allows you to create, read, update, and delete todo items. The API is built using Flask and Flask-RESTX.

## Installation

1. **Create and activate a virtual environment**:
    ```sh
    pip install virtualenv
    python3 -m venv myenv
    source myenv/bin/activate  
    ```


2. **Clone the repository**:
    ```sh
    git clone https://github.com/kapeksha/RestX_Assignment.git
    ```
3. 
3. **Install the dependencies**:
    ```sh
    pip install -r Requirements.txt
    ```

## Running the Application

1. **Run the Flask application**:
    ```sh
    flask run
    ```

    The application will be running at `http://127.0.0.1:5000/`.

## Running the Tests

1. **Ensure the application is not running** to avoid port conflicts.

2. **Run the tests using pytest**:
    ```sh
    pytest
    ```

    This will run all the test cases in the `test_app.py` file.

## API Endpoints

- `GET /todos/`: Get a list of all todos.
- `POST /todos/`: Create a new todo.
- `GET /todos/<id>`: Get a specific todo by ID.
- `PUT /todos/<id>`: Update a specific todo by ID.
- `DELETE /todos/<id>`: Delete a specific todo by ID.

## Example Requests

- **Get all todos**:
    ```sh
    http://127.0.0.1:5000/todos/
    ```

- **Get a specific todo**:
    ```sh
    http://127.0.0.1:5000/todos/1
    ```
- **Get a swagger.json:**
   ```sh
   http://127.0.0.1:5000/swagger.json
   ```

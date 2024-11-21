# Simple CRUD Flask REST API

This project demonstrates a simple Flask-based REST API that allows basic CRUD (Create, Read, Update, Delete) operations. It is designed to handle a database of records using Flask, Flask-RESTful, and SQLAlchemy.

## Demo

https://simple-crud-flask-rest-api.onrender.com/

## Sample

![Flask_API](https://github.com/user-attachments/assets/29b415c1-e635-45a3-8b7d-4560c46c4bdf)

## Table of Contents

- [Installation](#installation)
- [Usage](#usage)
- [API Endpoints](#api-endpoints)
- [Contributing](#contributing)
- [License](#license)

## Installation

1. Clone this repository:

   ```bash
   git clone https://github.com/Okkar25/Simple_CRUD_Flask_REST_API.git

   ```

2. Navigate into the project folder:

   ```bash
   cd Simple_CRUD_Flask_REST_API

   ```

3. Set up a virtual environment and activate it:

   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows use `venv/Scripts/activate`

   ```

4. Install the dependencies:

   ```bash
   pip install -r requirements.txt

   ```

## Usage

Run the Flask application:

```bash
python app.py

```

Visit http://localhost:8000 in your browser or use Postman or use ThunderClient VSCode extension to interact with the API.

## API Endpoints

- **GET** `/api/users` - Retrieve all users.
- **POST** `/api/users` - Create a new user.
- **GET** `/api/users/<id>` - Retrieve a specific user by ID.
- **PATCH** `/api/users/<id>` - Update an existing user by ID.
- **DELETE** `/api/users/<id>` - Delete a record by ID.

## Contributing

Feel free to fork this repository, submit issues, and make pull requests. Contributions are always welcome!

## License

This project is licensed under the MIT License.

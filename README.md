# Personal Finance Tracker API

A small FastAPI project for tracking personal income and expenses with JWT authentication.

## Overview

This project provides a simple backend API for:
- registering users
- logging in and receiving JWT tokens
- creating, reading, updating, and deleting personal transactions

It uses in-memory Python lists as a mock database, plus secure password hashing and JWT authentication.

## Tech Stack

- Python
- FastAPI
- Uvicorn
- Passlib for password hashing
- python-jose for JWT token handling
- python-multipart for OAuth2 form handling

## Repository Structure

- `main.py` - FastAPI app entry point
- `routers/auth.py` - authentication endpoints
- `routers/transactions.py` - transaction CRUD endpoints
- `schemas.py` - Pydantic request/response models
- `security.py` - password hashing and JWT helpers
- `dependencies.py` - protected route dependencies
- `database.py` - mock in-memory storage

## Setup

1. Create and activate a Python virtual environment:

```bash
python3 -m venv .venv
source .venv/bin/activate
```

2. Install dependencies:

```bash
pip install -r requirements.txt
```

3. Run the API:

```bash
uvicorn main:app --reload
```

4. Open the interactive API docs:

```text
http://127.0.0.1:8000/docs
```

## API Endpoints

### Authentication

- `POST /auth/register`
  - Registers a new user
  - Request body: `username`, `password`

- `POST /auth/login`
  - Logs in and returns an access token
  - Uses form data: `username`, `password`

### Transactions (Protected)

Use the `Authorize` button in `/docs` to add the JWT bearer token.

- `POST /transactions/`
  - Create a new transaction
  - Fields: `amount`, `category`, `transaction_type`, `description`

- `GET /transactions/`
  - Get the current user's transactions
  - Optional query parameter: `type_filter=income` or `type_filter=expense`

- `PUT /transactions/{transaction_id}`
  - Update an existing transaction for the authenticated user

- `DELETE /transactions/{transaction_id}`
  - Delete an existing transaction for the authenticated user

## Notes

- This project uses in-memory storage. Restarting the server will reset users and transactions.
- The JWT secret key is currently stored in code for demonstration. For production, use environment variables or a secrets manager.

## License

Add a license file if you want to publish this repository under an open-source license.

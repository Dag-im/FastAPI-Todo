# FastAPI Todo & User Management API

A **FastAPI** backend that implements:

- 🔐 JWT authentication (login, logout, token‑protected endpoints)
- 👥 User management with **RBAC** (admin & regular user)
- 📝 Todo CRUD, scoped per user
- 🔄 Password reset flows (user‑initiated & admin‑triggered)
- 📧 Email sending via SMTP (e.g. Gmail App Password or SendGrid)

---

## 🚀 Features

1. **Authentication**

   - `POST /auth/login` → obtain access token
   - `GET /auth/users/me` → get current user profile

2. **User Management**

   - `POST /users/` → self‑signup
   - `GET /users/me` → view own profile
   - **Admin‑only**:

     - `GET /users/` → list all users
     - `GET /users/{user_id}` → get user by ID
     - `PATCH /users/{user_id}` → update email, name, role
     - `DELETE /users/{user_id}` → remove a user
     - `POST /users/invite` → invite (create) an admin user

3. **Todo Management**

   - All endpoints require a valid JWT (bearer)
   - `GET /todos/` → list your todos
   - `POST /todos/` → create a new todo
   - `GET /todos/{id}` → fetch a specific todo
   - `PUT /todos/{id}` → update a todo
   - `DELETE /todos/{id}` → delete a todo

4. **Password Reset**

   - `POST /users/forgot-password` → send user‑reset email
   - `POST /users/reset-password` → reset using token
   - **Admin‑only**: `POST /users/{user_id}/reset-password` → trigger email reset for any user

---

## 📋 Requirements

- Python 3.10+
- PostgreSQL (or any SQLAlchemy‑compatible DB)
- SMTP credentials (Gmail App Password, SendGrid, etc.)

---

## 📦 Installation

1. **Clone** this repo

   ```bash
   git clone <your-repo-url>
   cd PythonRefresh
   ```

2. **Create & activate** a virtual environment

   ```bash
   python3 -m venv .venv
   source .venv/bin/activate
   ```

3. **Install** dependencies

   ```bash
   pip install -r requirements.txt
   ```

4. **Create** a `.env` in the project root:

   ```dotenv
   # Database
   DATABASE_URL=postgresql://user:pass@host:port/dbname?sslmode=require

   # JWT
   SECRET_KEY=your_very_long_random_string
   ACCESS_TOKEN_EXPIRE_MINUTES=60

   # Email (Gmail App Password or transactional SMTP)
   EMAIL_HOST=smtp.gmail.com
   EMAIL_PORT=587
   EMAIL_USER=you@example.com
   EMAIL_PASSWORD=your_app_password
   EMAIL_FROM="Todo List <no-reply@todolist.com>"

   # Frontend URL (for reset links)
   FRONTEND_URL=http://localhost:3000

   # Debug
   DEBUG=True
   ```

---

## ⚙️ Database Setup

This project uses SQLAlchemy’s `Base.metadata.create_all` for simplicity. On startup, it will:

```python
from core.database import Base, engine
Base.metadata.create_all(bind=engine)
```

For production schema migrations, integrate [Alembic](https://alembic.sqlalchemy.org/).

---

## ▶️ Running the Server

```bash
uvicorn main:app --reload
```

- The API will be live at `http://127.0.0.1:8000`
- Interactive docs at `http://127.0.0.1:8000/docs`

---

## 🔑 Authentication Flow

### 1. Register (Self‑Signup)

```bash
POST /users/
Content-Type: application/json

{
  "email": "alice@example.com",
  "full_name": "Alice",
  "password": "supersecret"
}
```

### 2. Login

```bash
POST /auth/login
Content-Type: application/x-www-form-urlencoded

username=alice@example.com&password=supersecret
```

Response:

```json
{
  "access_token": "eyJ0eXAiOiJKV1QiLCJhb...",
  "token_type": "bearer"
}
```

### 3. Use Token

Add header to all protected calls:

```
Authorization: Bearer <access_token>
```

---

## 📑 Endpoints Overview

### Todos (`/todos/`)

| Method | Path          | Description         |
| ------ | ------------- | ------------------- |
| GET    | `/todos/`     | List your todos     |
| POST   | `/todos/`     | Create a new todo   |
| GET    | `/todos/{id}` | Get a specific todo |
| PUT    | `/todos/{id}` | Update a todo       |
| DELETE | `/todos/{id}` | Delete a todo       |

### Users (`/users/`)

| Method    | Path                               | Access | Description                             |
| --------- | ---------------------------------- | ------ | --------------------------------------- |
| POST      | `/users/`                          | Public | Register (role=user)                    |
| GET       | `/users/me`                        | Auth   | View your profile                       |
| POST      | `/users/forgot-password?email=...` | Public | Send password-reset email               |
| POST      | `/users/reset-password`            | Public | Reset password with token               |
| **Admin** | `/users/`                          | Admin  | List all users                          |
| **Admin** | `/users/{user_id}`                 | Admin  | Get user by ID                          |
| **Admin** | `/users/{user_id}` (PATCH)         | Admin  | Update user (email, name, role)         |
| **Admin** | `/users/{user_id}` (DELETE)        | Admin  | Delete a user                           |
| **Admin** | `/users/invite`                    | Admin  | Invite (create) an admin user           |
| **Admin** | `/users/{user_id}/reset-password`  | Admin  | Trigger password-reset email for a user |

### Auth (`/auth/`)

| Method | Path             | Description      |
| ------ | ---------------- | ---------------- |
| POST   | `/auth/login`    | Obtain JWT token |
| GET    | `/auth/users/me` | Get current user |

---

## 📧 Password Reset Flow

1. **User‑initiated**: `POST /users/forgot-password?email=<email>`
   → Sends reset link via email (202 Accepted).

2. **Reset**: `POST /users/reset-password`

   ```json
   {
     "token": "<reset_token>",
     "new_password": "newsecret123"
   }
   ```

3. **Admin‑triggered**: `POST /users/{user_id}/reset-password`
   → Sends reset email to specified user (202 Accepted).

---

## 🧪 Testing with cURL

```bash
# Register
curl -X POST http://127.0.0.1:8000/users/ \
  -H "Content-Type: application/json" \
  -d '{"email":"alice@example.com","full_name":"Alice","password":"secret123"}'

# Login
curl -X POST http://127.0.0.1:8000/auth/login \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "username=alice@example.com&password=secret123"

# List todos
curl -H "Authorization: Bearer <token>" http://127.0.0.1:8000/todos/

# Request password reset
curl -X POST "http://127.0.0.1:8000/users/forgot-password?email=alice@example.com"

# Reset password
curl -X POST http://127.0.0.1:8000/users/reset-password \
  -H "Content-Type: application/json" \
  -d '{"token":"<token>","new_password":"newpassword"}'
```

Built with ❤️ using FastAPI and SQLAlchemy.

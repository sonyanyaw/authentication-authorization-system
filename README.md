[Читать на русском](./README.ru.md)

# Authentication and Authorization System  

## Description

This project is a **backend application** implementing a **custom authentication and authorization system** built with Django REST Framework (DRF) and PostgreSQL.  
The application **does not use** the built-in `django.contrib.auth` mechanisms for managing users and permissions.


---

## 🛠️ Technologies

- **Python 3.x**
- **Django**
- **Django REST Framework (DRF)**
- **PostgreSQL**
- **PyJWT** (for token generation)
- **bcrypt** (for password hashing)

---

## 🧱 Database Structure

The project includes the following **custom models**:

### 1. `User`
- `id`: Primary key  
- `first_name`, `last_name`, `patronymic`: User’s full name  
- `email`: Unique user email  
- `password_hash`: Hashed password (`bcrypt`)  
- `is_active`: Active flag (for soft deletion)  
- `created_at`, `updated_at`: Creation and update timestamps  
- `role`: Foreign key to `Role`  

### 2. `Role`
- `id`: Primary key  
- `name`: Role name (e.g., `admin`, `user`, `manager`)  

### 3. `BusinessElement`
- `id`: Primary key  
- `name`: Business entity name (e.g., `products`, `orders`, `users`, `access_rules`)  

### 4. `AccessRule`
- `id`: Primary key  
- `role`: Foreign key to `Role`  
- `business_element`: Foreign key to `BusinessElement`  
- Permissions: `read_permission`, `read_all_permission`, `create_permission`, `update_permission`, `update_all_permission`, `delete_permission`, `delete_all_permission`  
- **Uniqueness**: `(role, business_element)` — each role can have only one access rule per entity.

---

## 🔐 Authentication

- **Registration** (`POST /api/auth/register/`)  
  - Accepts: `first_name`, `last_name`, `patronymic`, `email`, `password`, `password_confirm`  
  - Validates password match  
  - Hashes the password with `bcrypt`  
  - Creates a user with a default role  
  - Returns a `JWT` token  

- **Login** (`POST /api/auth/login/`)  
  - Accepts: `email`, `password`  
  - Verifies password  
  - Returns a `JWT` token if credentials are correct  

- **Logout** (`POST /api/auth/logout/`)  
  - Client should delete the token  
  - Server remains stateless  

- **Profile** (`GET`, `PUT`, `DELETE /api/auth/profile/`)  
  - `GET`: Retrieve user info  
  - `PUT`: Update user data  
  - `DELETE`: Soft delete (`is_active = False`)  

---

## 🔒 Authorization

- **JWT Authentication**  
  - Token is passed in header: `Authorization: Bearer <token>`  
  - Custom `JWTAuthentication` extracts `user` from token and sets it in `request.user`.

- **Custom Permissions**  
  - Uses `AccessPermission` and subclasses (e.g., `AccessPermissionForProducts`)  
  - Checks user rights based on `role` and `business_element`  
  - Returns:
    - `401 Unauthorized` — if token missing/invalid/expired  
    - `403 Forbidden` — if user lacks required permission  

---

## 🧪 Mock Objects

Endpoints such as `/api/products/`, `/api/orders/`, etc.  
- Return dummy data  
- Protected by `@permission_classes([AccessPermissionFor...])`  
- Example:  
  `GET /api/products/ → [{ "id": 1, "name": "Product 1", "owner_id": 7 }]`

---

## 🔧 Access Rule Management (Admin Only)

- `GET /api/auth/access-rules/` — Get all rules  
- `POST /api/auth/access-rules/` — Create new rule  
- `GET /api/auth/access-rules/{id}/` — Get rule by ID  
- `PUT /api/auth/access-rules/{id}/` — Update rule  
- `DELETE /api/auth/access-rules/{id}/` — Delete rule  

---

## 📦 Installation and Launch

1. Ensure `Python`, `PostgreSQL`, and `pip` are installed.  
2. Clone the repository.  
3. Create a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # Linux/macOS
   venv\Scripts\activate     # Windows
   ```

4. Install dependencies:
    ```bash
    pip install django djangorestframework psycopg2-binary PyJWT bcrypt python-decouple
    ```

5. Configure .env:
    ```env
    SECRET_KEY=ваш_секретный_ключ
    DEBUG=True
    DB_NAME=auth_system
    DB_USER=postgres
    DB_PASSWORD=ваш_пароль
    DB_HOST=localhost
    DB_PORT=5432
    ```

6. Apply migrations:
    ```bash
    python manage.py makemigrations
    python manage.py migrate
    ```

7. Load test data:
    ```bash
    python manage.py init_data
    ```

8. Run server:
    ```bash
    python manage.py runserver
    ```

## Example Requests

- Registration: 
    ```bash
    curl -X POST http://127.0.0.1:8000/api/auth/register/ \
    -H "Content-Type: application/json" \
    -d '{
        "first_name": "Тест",
        "last_name": "Пользователь",
        "email": "test@example.com",
        "password": "testpass123",
        "password_confirm": "testpass123"
    }'
    ```

- Login:
    ```bash
    curl -X POST http://127.0.0.1:8000/api/auth/login/ \
    -H "Content-Type: application/json" \
    -d '{
        "email": "test@example.com",
        "password": "testpass123"
    }'
    ```

- Get Profile:
    ```bash
    curl -X GET http://127.0.0.1:8000/api/auth/profile/ \
    -H "Authorization: Bearer <token>"
    ```

- Get Products (mock):
    ```bash
    curl -X GET http://127.0.0.1:8000/api/products/ \
    -H "Authorization: Bearer <user_token>"
    ```

- Get Access Rules (admin only):
    ```bash
    curl -X GET http://127.0.0.1:8000/api/auth/access-rules/ \
    -H "Authorization: Bearer <admin_token>"
    ```


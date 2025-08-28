# Restaurant Management System API

A FastAPI-based backend system for restaurant management, featuring menu management, order processing, and user authentication.

## Features

- 🔐 Authentication & Role-based Access Control
  - User registration and login
  - JWT-based authentication
  - Role-based permissions (admin, staff, customer)

- 📋 Menu Management
  - CRUD operations for menu items
  - Category-based filtering
  - Availability status

- 🛒 Order Processing
  - Create orders with multiple items
  - Order status tracking
  - Order history
  - Role-based order access

## Tech Stack

- Python 3.10+
- FastAPI (ASGI web framework)
- MongoDB with Motor (async driver)
- PyJWT for authentication
- Pydantic for data validation
- bcrypt for password hashing

## Project Structure

```
restaurant-backend/
├─ app/
│  ├─ main.py          # FastAPI application setup
│  ├─ config.py        # Configuration management
│  ├─ db/              # Database connection
│  ├─ models/          # Pydantic models
│  ├─ services/        # Business logic
│  ├─ auth/            # Authentication utilities
│  └─ routes/          # API endpoints
├─ scripts/
│  └─ seed.py          # Database seeding
├─ tests/              # Test cases
└─ README.md
```

## Setup Instructions

1. Clone the repository:
   ```bash
   git clone <repository-url>
   cd restaurant-backend
   ```

2. Create and activate virtual environment:
   ```bash
   python -m venv .venv
   # Windows
   .venv\Scripts\activate
   # Unix/macOS
   source .venv/bin/activate
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Create `.env` file:
   ```
   MONGODB_URI=mongodb://localhost:27017
   MONGODB_DB_NAME=restaurant_db
   JWT_SECRET=your-super-secret-key
   JWT_ALGORITHM=HS256
   ACCESS_TOKEN_EXPIRE_MINUTES=1440
   ```

5. Seed the database:
   ```bash
   python scripts/seed.py
   ```

6. Run the application:
   ```bash
   uvicorn app.main:app --reload
   ```

The API will be available at `http://localhost:8000`
- API documentation: `http://localhost:8000/docs`
- OpenAPI Spec: `http://localhost:8000/api/v1/openapi.json`

## API Endpoints

### Authentication

- POST `/api/v1/auth/register` - Register new user
- POST `/api/v1/auth/login` - Login and get JWT token
- GET `/api/v1/auth/profile` - Get current user profile

### Menu Management

- GET `/api/v1/menu` - List all menu items
- POST `/api/v1/menu` - Create menu item (admin/staff)
- GET `/api/v1/menu/{id}` - Get menu item details
- PUT `/api/v1/menu/{id}` - Update menu item (admin/staff)
- DELETE `/api/v1/menu/{id}` - Delete menu item (admin/staff)

### Orders

- POST `/api/v1/orders` - Create new order (customer)
- GET `/api/v1/orders` - List orders (filtered by role)
- GET `/api/v1/orders/{id}` - Get order details
- PUT `/api/v1/orders/{id}/status` - Update order status (admin/staff)

## Example API Usage

### Register a New User
```bash
curl -X POST "http://localhost:8000/api/v1/auth/register" \
     -H "Content-Type: application/json" \
     -d '{"email":"user@example.com","password":"secret123","name":"John Doe"}'
```

### Login
```bash
curl -X POST "http://localhost:8000/api/v1/auth/login" \
     -H "Content-Type: application/x-www-form-urlencoded" \
     -d "username=user@example.com&password=secret123"
```

### Create Menu Item (Admin/Staff)
```bash
curl -X POST "http://localhost:8000/api/v1/menu" \
     -H "Authorization: Bearer {your-token}" \
     -H "Content-Type: application/json" \
     -d '{"name":"Burger","description":"Delicious burger","price":9.99,"category":"Main"}'
```

### Create Order (Customer)
```bash
curl -X POST "http://localhost:8000/api/v1/orders" \
     -H "Authorization: Bearer {your-token}" \
     -H "Content-Type: application/json" \
     -d '{"items":[{"menu_id":"item-id","quantity":2}]}'
```

## Development

### Running Tests
```bash
pytest
```

### Code Style
The project follows PEP 8 style guide. Install and run flake8:
```bash
pip install flake8
flake8 .
```

## Deployment

### Environment Variables
When deploying, make sure to set these environment variables:
- `MONGODB_URI`: Your MongoDB connection string
- `JWT_SECRET`: A secure random string
- `MONGODB_DB_NAME`: Database name (default: restaurant_db)

### Deploy to Railway
1. Create a new Railway project
2. Add MongoDB addon
3. Set environment variables
4. Deploy using Railway CLI or GitHub integration

### Deploy to Render
1. Create a new Web Service
2. Connect your repository
3. Set environment variables
4. Set build command: `pip install -r requirements.txt`
5. Set start command: `uvicorn app.main:app --host 0.0.0.0 --port $PORT`

## Contributing

1. Fork the repository
2. Create your feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

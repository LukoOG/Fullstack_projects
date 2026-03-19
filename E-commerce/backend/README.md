# E-commerce Backend

A Django REST Framework backend for an e-commerce platform with products, categories, carts, and orders.

## Features

- User authentication and registration
- Product CRUD with categories
- Cart management (add/remove items)
- Order creation and tracking
- Media handling for product images
- Admin-only endpoints for product management

## Demo Endpoints

### Authentication
- POST /api/auth/login/

### Products
- GET /api/products/
- POST /api/products/ (admin only)

### Cart
- GET /api/cart/
- POST /api/cart/add/

### Orders
- POST /api/orders/checkout/
- GET /api/orders/

Tech stack: Python, Django, Django REST Framework, PostgreSQL
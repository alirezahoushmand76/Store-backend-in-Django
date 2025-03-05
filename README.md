# Storefront API

A full-featured e-commerce RESTful API built with Django REST Framework.

## Overview

This project is a modern e-commerce backend API that provides comprehensive product management, user authentication, shopping carts, order processing, and more. It's designed with best practices in mind and uses JWT-based authentication for secure access.

## Features

- **Product Management**: Create, read, update, and delete products with filtering, searching, and ordering capabilities
- **Collection Management**: Organize products into collections
- **User Authentication**: JWT-based authentication with token refresh
- **Shopping Cart**: Create carts, add/update/remove items
- **Customer Profiles**: Customer management with user relation
- **Order Processing**: Create and manage orders
- **Reviews**: Product review system
- **Permissions**: Role-based access control

## Tech Stack

- **Django**: Web framework
- **Django REST Framework**: API toolkit
- **MySQL**: Database
- **JWT Authentication**: Token-based security via Djoser and Simple JWT
- **Django Filter**: Advanced filtering
- **RESTful design**: Following REST principles

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/your-username/storefront.git
   cd storefront
   ```

2. Set up a virtual environment (recommended):
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Set up the database:
   ```bash
   python manage.py migrate
   ```

5. Create a superuser:
   ```bash
   python manage.py createsuperuser
   ```

6. Run the development server:
   ```bash
   python manage.py runserver
   ```

## API Endpoints

### Authentication
- `POST /auth/jwt/create/`: Obtain JWT tokens
- `POST /auth/jwt/refresh/`: Refresh JWT tokens
- `POST /auth/users/`: Register a new user

### Products
- `GET /store/products/`: List all products
- `POST /store/products/`: Create a new product (admin only)
- `GET /store/products/{id}/`: Get a specific product
- `PUT /store/products/{id}/`: Update a product (admin only)
- `DELETE /store/products/{id}/`: Delete a product (admin only)

### Collections
- `GET /store/collections/`: List all collections
- `POST /store/collections/`: Create a new collection (admin only)
- `GET /store/collections/{id}/`: Get a specific collection
- `PUT /store/collections/{id}/`: Update a collection (admin only)
- `DELETE /store/collections/{id}/`: Delete a collection (admin only)

### Customers
- `GET /store/customers/me/`: Get current customer profile
- `PUT /store/customers/me/`: Update current customer profile

### Carts
- `POST /store/carts/`: Create a new cart
- `GET /store/carts/{id}/`: Get a specific cart
- `DELETE /store/carts/{id}/`: Delete a cart
- `GET /store/carts/{id}/items/`: List items in a cart
- `POST /store/carts/{id}/items/`: Add an item to a cart
- `PATCH /store/carts/{id}/items/{id}/`: Update quantity of a cart item
- `DELETE /store/carts/{id}/items/{id}/`: Remove an item from a cart

### Reviews
- `GET /store/products/{id}/reviews/`: List reviews for a product
- `POST /store/products/{id}/reviews/`: Create a review for a product

## Authentication

This API uses JWT (JSON Web Token) authentication. To authenticate:

1. Obtain tokens by sending credentials to `/auth/jwt/create/`:
   ```json
   {
     "username": "user@example.com",
     "password": "password"
   }
   ```

2. Use the access token in the Authorization header:
   ```
   Authorization: JWT your_access_token
   ```

3. When the access token expires, use the refresh token to get a new one:
   ```json
   {
     "refresh": "your_refresh_token"
   }
   ```

## Development

- Run tests:
  ```bash
  python manage.py test
  ```

- Check code style:
  ```bash
  flake8
  ```

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request. 
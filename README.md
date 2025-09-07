## Library Management System API

A RESTful backend API built with Django and Django REST Framework for managing books, users, and transactions.

## Features

- User registration and login
- Book CRUD (Create, Read, Update, Delete)
- Check out and return books
- Admin-only transaction history
- search by Title, Author, or ISBN
- Filter Available Books

## Tech Stack

- Python
- Django
- Django REST Framework

## API Endpoints
- `/api/register/` | POST | Public | Register new user |
- `/api/login/` | POST | Public | Get auth token |

- `/api/checkout/<book_id>/` | POST | Authenticated | Checkout a book |
- `/api/return/<book_id>/` | POST | Authenticated | Return a book |
- `/api/mybooks/` | GET | Authenticated | My checked out books |
- `/api/transactions/` | GET | Admin only | View all transactions |
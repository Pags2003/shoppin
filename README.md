# Flask Web App with SQLAlchemy

## Overview
This is a Flask-based web application that utilizes SQLAlchemy for database management. The app allows user registration, item management, cart functionality, order processing, and an admin panel for managing users, items, and orders.

## Live Demo
Check out the live version of the project: [pags2003.pythonanywhere.com](http://pags2003.pythonanywhere.com/)

## Features
- **User Authentication**: Allows users to register and store credentials securely.
- **Item Management**: Add, delete, and categorize items in the database.
- **Shopping Cart**: Add items to the cart and proceed to checkout.
- **Order Processing**: Place orders and track their status.
- **Admin Dashboard**: Manage users, orders, and inventory.

## Technologies Used
- **Backend**: Flask (Python)
- **Database**: SQLite (SQLAlchemy ORM)
- **Frontend**: HTML & Jinja Templates

## Installation
### Prerequisites
Ensure you have Python installed (recommended version 3.6+).

### Steps to Run the Application
1. **Clone the Repository**
   ```sh
   git clone <repository_url>
   cd <repository_name>
   ```

2. **Create a Virtual Environment** (Optional but recommended)
   ```sh
   python -m venv venv
   source venv/bin/activate  # On Windows use: venv\Scripts\activate
   ```

3. **Install Dependencies**
   ```sh
   pip install -r requirements.txt
   ```

4. **Initialize the Database**
   ```sh
   python
   >>> from app import db
   >>> db.create_all()
   >>> exit()
   ```

5. **Run the Application**
   ```sh
   flask run
   ```

6. Open a web browser and navigate to:
   ```
   http://127.0.0.1:5000/
   ```

## Project Structure
```
.
├── app.py          # Main application file
├── templates/      # HTML templates
├── static/         # CSS and JS files
├── database.db     # SQLite database
├── requirements.txt # Required dependencies
└── README.md       # Documentation
```

## API Endpoints
| Endpoint               | Method | Description |
|------------------------|--------|-------------|
| `/`                    | GET    | Home Page |
| `/admin`               | GET    | Admin Panel |
| `/users`               | GET    | List all users |
| `/deleteuser/<id>`     | GET    | Delete user |
| `/items`               | GET    | List all items |
| `/newitem`             | POST   | Add a new item |
| `/cart`                | GET    | View cart |
| `/checkout`            | POST   | Checkout and place an order |
| `/orders`              | GET    | List all orders |
| `/updatestatus/<id>`   | GET    | Update order status |



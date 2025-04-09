🛠️ Product Management Dashboard

A secure and efficient product management dashboard developed with Django and Django REST Framework. The app allows users to register, log in, view products, place orders, and download reports — all in line with the internship assessment task from ExactConnect.

✅ Key Features
    🔐 Authentication
        Register and log in using JWT tokens
        Secure access to dashboard features
        Token refresh mechanism
    🛍️ Product Dashboard
        Products dynamically fetched from a public API
        Filter and browse product listings
        Place and manage product orders
    📦 Order Management
        Create new orders for selected products
        View your past orders
        Download report of your orders with pricing

💡 Tech Stack
    Backend: Django, Django REST Framework
    Auth: JWT (using djangorestframework-simplejwt)
    Frontend: (Can be React, Bootstrap, or Django templates — depending on implementation)
    Others: dotenv, PostgreSQL (or SQLite), PDF/CSV generation for reports


📦 Installation
1. Clone the Repository
```bash
    git clone https://github.com/allarassemmaxwell/exactconnect-backend
    cd exactconnect-backend
```

2. Create Virtual Environment
```bash
    python -m venv env
    source env/bin/activate  # On Windows: env\Scripts\activate
```

3. Install Dependencies
```bash
    pip install -r requirements.txt
```

4. Set Up Environment Variables
Create a .env file in the root directory and add the following:
```bash
    SECRET_KEY=your-django-secret-key
    DEBUG=True
```

5. Apply Migrations and Run the Server
```bash
    python manage.py migrate
    python manage.py runserver
```

🔗 API Endpoints
    Method	        Endpoint	            Description
    POST	        /register/	            Register a new user
    POST	        /login/	                Login and receive JWT tokens
    POST	        /token/refresh/	        Refresh JWT access token
    GET	            /products/	            Get product list (from public API)
    POST	        /orders/	            Place a new order
    GET	            /my-orders/	            Retrieve orders by the logged-in user

    All endpoints require JWT authentication (except register and login).

🧪 Sample Usage
    1. Register & Login
        Register at /register/
        Log in at /login/ to receive access and refresh tokens
    2. Access Dashboard APIs
        Use Authorization: Bearer <access_token> in headers
    3. Place Orders
        Call /orders/ with selected product data
    4. View Orders
        Retrieve via /my-orders/
    5. Download Report
        (Optionally via a button in frontend for CSV or PDF export)

📁 File Structure Overview
    ├── product_app/
│   ├── views.py         # API views for auth, products, orders
│   ├── models.py        # User, Product, Order, OrderItem models
│   ├── serializers.py   # Serializers for API endpoints
│   ├── urls.py          # Routes and endpoint mapping
│   └── ...
├── .env
├── requirements.txt
├── manage.py
└── README.md

📆 Submission Checklist
    Register/Login and token refresh working
    Product listing, filtering, and ordering complete
    Ordered products viewable by user
    Report download ready
    App hosted with working live link
    Public GitHub repo shared

 👤 Author
Allarassem Maxime
🌍 Chad 🇹🇩 | 📍 Based in Kenya

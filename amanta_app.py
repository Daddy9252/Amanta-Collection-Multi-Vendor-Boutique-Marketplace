"""
Amanta Collection — single-file Flask app (for quick local demo / screenshots)
================================================================================
This file contains the ENTIRE application (models, forms, templates, and
routes) in one place so you can run it immediately and start taking
screenshots without setting up the full multi-file project structure.

HOW TO RUN
----------
1. Install dependencies (one line):
     pip install flask flask-sqlalchemy flask-login flask-wtf

2. Run the app:
     python amanta_app.py

3. Open your browser to:
     http://127.0.0.1:5000

The database (amanta_demo.db) is created automatically on first run and is
pre-seeded with demo accounts and products so the interface looks populated
immediately — perfect for screenshots.

DEMO LOGINS
-----------
  Admin:   admin@amanta.test   / AdminPass123
  Vendor:  vendor@amanta.test  / VendorPass123
  Buyer:   buyer@amanta.test   / BuyerPass123

NOTE: This single-file version omits image upload (to avoid needing extra
folders) and keeps all CSS inline for simplicity. The full, production-style
multi-file project (with image upload, separate templates/routes files, and
static assets) is the one delivered earlier as
Amanta_Collection_Coursework_Deliverables.zip — use that for your actual
submission and source-code deliverable. This file is only for quickly
viewing/screenshotting the working interface.
"""

import os
from datetime import datetime

from flask import Flask, render_template, redirect, url_for, flash, request, abort
from flask_sqlalchemy import SQLAlchemy
from flask_login import (
    LoginManager, UserMixin, login_user, logout_user,
    login_required, current_user
)
from flask_wtf import FlaskForm
from flask_wtf.csrf import CSRFProtect
from wtforms import (
    StringField, PasswordField, SelectField, SubmitField,
    TextAreaField, DecimalField, IntegerField
)
from wtforms.validators import DataRequired, Email, Length, EqualTo, NumberRange, Optional
from werkzeug.security import generate_password_hash, check_password_hash
from jinja2 import DictLoader

basedir = os.path.abspath(os.path.dirname(__file__))

# ---------------------------------------------------------------------------
# App setup
# ---------------------------------------------------------------------------
app = Flask(__name__)
app.config["SECRET_KEY"] = "dev-secret-key-change-this-later"
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///" + os.path.join(basedir, "amanta_demo.db")
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["SESSION_COOKIE_HTTPONLY"] = True
app.config["SESSION_COOKIE_SAMESITE"] = "Lax"

db = SQLAlchemy(app)
csrf = CSRFProtect(app)

login_manager = LoginManager(app)
login_manager.login_view = "login"


# ---------------------------------------------------------------------------
# Models
# ---------------------------------------------------------------------------
class User(UserMixin, db.Model):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    role = db.Column(db.String(20), nullable=False)       # buyer, vendor, admin
    status = db.Column(db.String(20), default="active")   # active, deactivated
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    products = db.relationship("Product", backref="vendor", lazy=True)
    cart_items = db.relationship("CartItem", backref="buyer", lazy=True)
    orders = db.relationship("Order", backref="buyer", lazy=True)


class Product(db.Model):
    __tablename__ = "products"
    id = db.Column(db.Integer, primary_key=True)
    vendor_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    name = db.Column(db.String(150), nullable=False)
    description = db.Column(db.Text)
    price = db.Column(db.Numeric(10, 2), nullable=False)
    size = db.Column(db.String(10))
    color = db.Column(db.String(30))
    stock = db.Column(db.Integer, nullable=False, default=0)
    category = db.Column(db.String(50), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)


class CartItem(db.Model):
    __tablename__ = "cart_items"
    id = db.Column(db.Integer, primary_key=True)
    buyer_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    product_id = db.Column(db.Integer, db.ForeignKey("products.id"), nullable=False)
    quantity = db.Column(db.Integer, nullable=False, default=1)
    product = db.relationship("Product")


class Order(db.Model):
    __tablename__ = "orders"
    id = db.Column(db.Integer, primary_key=True)
    buyer_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    total = db.Column(db.Numeric(10, 2), nullable=False)
    status = db.Column(db.String(20), default="Pending")
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    items = db.relationship("OrderItem", backref="order", lazy=True)


class OrderItem(db.Model):
    __tablename__ = "order_items"
    id = db.Column(db.Integer, primary_key=True)
    order_id = db.Column(db.Integer, db.ForeignKey("orders.id"), nullable=False)
    product_id = db.Column(db.Integer, db.ForeignKey("products.id"), nullable=False)
    quantity = db.Column(db.Integer, nullable=False)
    price_at_purchase = db.Column(db.Numeric(10, 2), nullable=False)
    product = db.relationship("Product")


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


# ---------------------------------------------------------------------------
# Forms
# ---------------------------------------------------------------------------
class RegisterForm(FlaskForm):
    name = StringField("Name", validators=[DataRequired(), Length(min=2, max=100)])
    email = StringField("Email", validators=[DataRequired(), Email()])
    password = PasswordField("Password", validators=[DataRequired(), Length(min=8)])
    confirm_password = PasswordField(
        "Confirm Password",
        validators=[DataRequired(), EqualTo("password", message="Passwords must match")]
    )
    role = SelectField("Role", choices=[("buyer", "Buyer"), ("vendor", "Vendor")])
    submit = SubmitField("Register")


class LoginForm(FlaskForm):
    email = StringField("Email", validators=[DataRequired(), Email()])
    password = PasswordField("Password", validators=[DataRequired()])
    submit = SubmitField("Login")


class ProductForm(FlaskForm):
    name = StringField("Product Name", validators=[DataRequired(), Length(min=2, max=150)])
    description = TextAreaField("Description", validators=[Optional()])
    price = DecimalField("Price", validators=[DataRequired(), NumberRange(min=0.01)])
    size = SelectField("Size", choices=[("S", "S"), ("M", "M"), ("L", "L"), ("XL", "XL")])
    color = StringField("Color", validators=[Optional(), Length(max=30)])
    stock = IntegerField("Stock Quantity", validators=[DataRequired(), NumberRange(min=0)])
    category = SelectField("Category", choices=[
        ("Dresses", "Dresses"), ("Outerwear", "Outerwear"),
        ("Tops", "Tops"), ("Bottoms", "Bottoms"), ("Accessories", "Accessories")
    ])
    submit = SubmitField("Save Product")


# ---------------------------------------------------------------------------
# Templates (all inline via a DictLoader so this stays a single file)
# ---------------------------------------------------------------------------
TEMPLATES = {}

TEMPLATES["layout.html"] = """
<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Amanta Collection</title>
<link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
<style>
body { font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; background-color:#faf9f7; }
.navbar-brand { font-weight:600; letter-spacing:0.5px; }
.card { border:none; box-shadow:0 2px 8px rgba(0,0,0,0.08); transition:transform .15s ease, box-shadow .15s ease; }
.card:hover { transform:translateY(-3px); box-shadow:0 6px 16px rgba(0,0,0,0.12); }
.product-thumb { height:180px; background:linear-gradient(135deg,#ddd,#eee); display:flex; align-items:center; justify-content:center; color:#999; font-size:0.85rem; }
.btn-dark { background-color:#2b2b2b; border:none; }
.btn-dark:hover { background-color:#000; }
footer { border-top:1px solid #e0e0e0; color:#777; font-size:0.9rem; }
table th { background-color:#f4f3f1; }
.badge { font-weight:500; padding:0.4em 0.7em; }
</style>
</head>
<body>
<nav class="navbar navbar-expand-lg navbar-dark bg-dark">
  <div class="container">
    <a class="navbar-brand" href="{{ url_for('home') }}">Amanta Collection</a>
    <form class="d-flex mx-3" method="GET" action="{{ url_for('browse_products') }}">
      <input class="form-control me-2" type="search" name="q" placeholder="Search products...">
      <button class="btn btn-outline-light" type="submit">Search</button>
    </form>
    <div class="collapse navbar-collapse">
      <ul class="navbar-nav ms-auto">
        {% if current_user.is_authenticated %}
          {% if current_user.role == 'buyer' %}
          <li class="nav-item"><a class="nav-link" href="{{ url_for('view_cart') }}">Cart</a></li>
          <li class="nav-item"><a class="nav-link" href="{{ url_for('buyer_orders') }}">My Orders</a></li>
          {% endif %}
          {% if current_user.role == 'vendor' %}
          <li class="nav-item"><a class="nav-link" href="{{ url_for('vendor_products') }}">My Products</a></li>
          <li class="nav-item"><a class="nav-link" href="{{ url_for('vendor_orders') }}">Orders</a></li>
          {% endif %}
          {% if current_user.role == 'admin' %}
          <li class="nav-item"><a class="nav-link" href="{{ url_for('manage_users') }}">Users</a></li>
          <li class="nav-item"><a class="nav-link" href="{{ url_for('manage_products') }}">Products</a></li>
          <li class="nav-item"><a class="nav-link" href="{{ url_for('all_orders') }}">All Orders</a></li>
          {% endif %}
          <li class="nav-item"><span class="nav-link">Hi, {{ current_user.name }} ({{ current_user.role }})</span></li>
          <li class="nav-item"><a class="nav-link" href="{{ url_for('logout') }}">Logout</a></li>
        {% else %}
          <li class="nav-item"><a class="nav-link" href="{{ url_for('login') }}">Login</a></li>
          <li class="nav-item"><a class="nav-link" href="{{ url_for('register') }}">Register</a></li>
        {% endif %}
      </ul>
    </div>
  </div>
</nav>
<div class="container mt-4">
  {% with messages = get_flashed_messages(with_categories=true) %}
    {% if messages %}
      {% for category, message in messages %}
        <div class="alert alert-{{ category }} alert-dismissible fade show" role="alert">
          {{ message }}
          <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
        </div>
      {% endfor %}
    {% endif %}
  {% endwith %}
  {% block content %}{% endblock %}
</div>
<footer class="text-center mt-5 py-3 bg-light">
  <p class="mb-0">&copy; 2026 Amanta Collection. Coursework Demo.</p>
</footer>
<script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/js/bootstrap.bundle.min.js"></script>
</body>
</html>
"""

TEMPLATES["home.html"] = """
{% extends 'layout.html' %}
{% block content %}
<div class="text-center py-5 mb-4" style="background-color:#2b2b2b; color:white; border-radius:8px;">
  <h1>Amanta Collection</h1>
  <p class="lead">Discover unique boutique fashion from independent vendors.</p>
  <a href="{{ url_for('browse_products') }}" class="btn btn-light btn-lg mt-2">Shop All Products</a>
</div>
<h3 class="mb-3">Featured Products</h3>
<div class="row">
  {% for product in featured_products %}
  <div class="col-md-3 col-sm-6 mb-4">
    <div class="card h-100">
      <div class="product-thumb">{{ product.category }}</div>
      <div class="card-body">
        <h6 class="card-title">{{ product.name }}</h6>
        <p class="card-text">£{{ "%.2f"|format(product.price) }}</p>
        <a href="{{ url_for('product_detail', product_id=product.id) }}" class="btn btn-sm btn-outline-dark">View</a>
      </div>
    </div>
  </div>
  {% else %}
  <p>No products available yet.</p>
  {% endfor %}
</div>
{% endblock %}
"""

TEMPLATES["register.html"] = """
{% extends 'layout.html' %}
{% block content %}
<div class="row justify-content-center">
  <div class="col-md-6">
    <h2 class="mb-4">Create an Account</h2>
    <form method="POST">
      {{ form.hidden_tag() }}
      <div class="mb-3">{{ form.name.label(class="form-label") }}{{ form.name(class="form-control") }}</div>
      <div class="mb-3">{{ form.email.label(class="form-label") }}{{ form.email(class="form-control") }}</div>
      <div class="mb-3">{{ form.password.label(class="form-label") }}{{ form.password(class="form-control") }}</div>
      <div class="mb-3">{{ form.confirm_password.label(class="form-label") }}{{ form.confirm_password(class="form-control") }}</div>
      <div class="mb-3">{{ form.role.label(class="form-label") }}{{ form.role(class="form-select") }}</div>
      {{ form.submit(class="btn btn-dark") }}
    </form>
    <p class="mt-3">Already have an account? <a href="{{ url_for('login') }}">Login</a></p>
  </div>
</div>
{% endblock %}
"""

TEMPLATES["login.html"] = """
{% extends 'layout.html' %}
{% block content %}
<div class="row justify-content-center">
  <div class="col-md-6">
    <h2 class="mb-4">Login to Amanta Collection</h2>
    <form method="POST">
      {{ form.hidden_tag() }}
      <div class="mb-3">{{ form.email.label(class="form-label") }}{{ form.email(class="form-control") }}</div>
      <div class="mb-3">{{ form.password.label(class="form-label") }}{{ form.password(class="form-control") }}</div>
      {{ form.submit(class="btn btn-dark") }}
    </form>
    <p class="mt-3">Don't have an account? <a href="{{ url_for('register') }}">Register</a></p>
    <hr>
    <p class="text-muted small">
      Demo logins —<br>
      Admin: admin@amanta.test / AdminPass123<br>
      Vendor: vendor@amanta.test / VendorPass123<br>
      Buyer: buyer@amanta.test / BuyerPass123
    </p>
  </div>
</div>
{% endblock %}
"""

TEMPLATES["product_list.html"] = """
{% extends 'layout.html' %}
{% block content %}
<div class="row">
  <div class="col-md-3">
    <h5>Filters</h5>
    <form method="GET" action="{{ url_for('browse_products') }}">
      <input type="hidden" name="q" value="{{ query }}">
      <div class="mb-3">
        <label class="form-label">Category</label>
        <select name="category" class="form-select">
          <option value="">All</option>
          {% for cat in categories %}
          <option value="{{ cat }}" {% if cat == category %}selected{% endif %}>{{ cat }}</option>
          {% endfor %}
        </select>
      </div>
      <div class="mb-3">
        <label class="form-label">Size</label>
        <select name="size" class="form-select">
          <option value="">All</option>
          <option value="S" {% if size=='S' %}selected{% endif %}>S</option>
          <option value="M" {% if size=='M' %}selected{% endif %}>M</option>
          <option value="L" {% if size=='L' %}selected{% endif %}>L</option>
          <option value="XL" {% if size=='XL' %}selected{% endif %}>XL</option>
        </select>
      </div>
      <div class="mb-3">
        <label class="form-label">Min Price</label>
        <input type="number" step="0.01" name="min_price" class="form-control" value="{{ min_price or '' }}">
      </div>
      <div class="mb-3">
        <label class="form-label">Max Price</label>
        <input type="number" step="0.01" name="max_price" class="form-control" value="{{ max_price or '' }}">
      </div>
      <button type="submit" class="btn btn-dark w-100">Apply Filters</button>
    </form>
  </div>
  <div class="col-md-9">
    <h2 class="mb-4">{% if query %}Results for "{{ query }}"{% else %}All Products{% endif %}</h2>
    <div class="row">
      {% for product in products %}
      <div class="col-md-4 mb-4">
        <div class="card h-100">
          <div class="product-thumb">{{ product.category }}</div>
          <div class="card-body">
            <h5 class="card-title">{{ product.name }}</h5>
            <p class="card-text">£{{ "%.2f"|format(product.price) }}</p>
            <a href="{{ url_for('product_detail', product_id=product.id) }}" class="btn btn-outline-dark">View</a>
          </div>
        </div>
      </div>
      {% else %}
      <p>No products found.</p>
      {% endfor %}
    </div>
  </div>
</div>
{% endblock %}
"""

TEMPLATES["product_detail.html"] = """
{% extends 'layout.html' %}
{% block content %}
<div class="row">
  <div class="col-md-5"><div class="product-thumb" style="height:320px;">{{ product.category }}</div></div>
  <div class="col-md-7">
    <h2>{{ product.name }}</h2>
    <p class="fs-4">£{{ "%.2f"|format(product.price) }}</p>
    <p>Size: {{ product.size }} | Color: {{ product.color }}</p>
    <p>Sold by: {{ product.vendor.name }}</p>
    {% if product.stock > 0 %}
    <p class="text-success">In stock ({{ product.stock }} available)</p>
    {% else %}
    <p class="text-danger">Out of stock</p>
    {% endif %}
    {% if current_user.is_authenticated and current_user.role == 'buyer' %}
    <form method="POST" action="{{ url_for('add_to_cart', product_id=product.id) }}" class="d-flex gap-2 align-items-end">
      <input type="hidden" name="csrf_token" value="{{ csrf_token() }}">
      <div>
        <label class="form-label">Quantity</label>
        <input type="number" name="quantity" value="1" min="1" max="{{ product.stock }}" class="form-control" style="width:100px;">
      </div>
      <button type="submit" class="btn btn-dark" {% if product.stock == 0 %}disabled{% endif %}>Add to Cart</button>
    </form>
    {% endif %}
    <hr>
    <h5>Description</h5>
    <p>{{ product.description }}</p>
  </div>
</div>
{% endblock %}
"""

TEMPLATES["cart.html"] = """
{% extends 'layout.html' %}
{% block content %}
<h2 class="mb-4">Your Cart</h2>
{% if cart_items %}
<table class="table align-middle">
  <thead><tr><th>Product</th><th>Price</th><th>Quantity</th><th>Subtotal</th><th></th></tr></thead>
  <tbody>
    {% for item in cart_items %}
    <tr>
      <td>{{ item.product.name }}</td>
      <td>£{{ "%.2f"|format(item.product.price) }}</td>
      <td>
        <form method="POST" action="{{ url_for('update_cart_item', item_id=item.id) }}" class="d-flex gap-2">
          <input type="hidden" name="csrf_token" value="{{ csrf_token() }}">
          <input type="number" name="quantity" value="{{ item.quantity }}" min="1" max="{{ item.product.stock }}" class="form-control" style="width:80px;">
          <button type="submit" class="btn btn-sm btn-outline-secondary">Update</button>
        </form>
      </td>
      <td>£{{ "%.2f"|format(item.product.price * item.quantity) }}</td>
      <td>
        <form method="POST" action="{{ url_for('remove_cart_item', item_id=item.id) }}">
          <input type="hidden" name="csrf_token" value="{{ csrf_token() }}">
          <button type="submit" class="btn btn-sm btn-outline-danger">Remove</button>
        </form>
      </td>
    </tr>
    {% endfor %}
  </tbody>
</table>
<div class="text-end">
  <h4>Total: £{{ "%.2f"|format(total) }}</h4>
  <a href="{{ url_for('browse_products') }}" class="btn btn-outline-dark">Continue Shopping</a>
  <a href="{{ url_for('checkout') }}" class="btn btn-dark">Proceed to Checkout</a>
</div>
{% else %}
<p>Your cart is empty.</p>
<a href="{{ url_for('browse_products') }}" class="btn btn-dark">Browse Products</a>
{% endif %}
{% endblock %}
"""

TEMPLATES["checkout.html"] = """
{% extends 'layout.html' %}
{% block content %}
<h2 class="mb-4">Checkout</h2>
<h5>Order Summary</h5>
<table class="table">
  <thead><tr><th>Product</th><th>Qty</th><th>Subtotal</th></tr></thead>
  <tbody>
    {% for item in cart_items %}
    <tr><td>{{ item.product.name }}</td><td>{{ item.quantity }}</td><td>£{{ "%.2f"|format(item.product.price * item.quantity) }}</td></tr>
    {% endfor %}
  </tbody>
</table>
<h4 class="text-end">Total: £{{ "%.2f"|format(total) }}</h4>
<hr>
<div class="card p-4 mt-3" style="max-width:400px;">
  <h5>Simulated Payment</h5>
  <p class="text-muted">This is a demo/academic checkout. No real payment is processed.</p>
  <form method="POST" action="{{ url_for('confirm_checkout') }}">
    <input type="hidden" name="csrf_token" value="{{ csrf_token() }}">
    <button type="submit" class="btn btn-dark w-100">Confirm &amp; Place Order</button>
  </form>
</div>
{% endblock %}
"""

TEMPLATES["order_confirmation.html"] = """
{% extends 'layout.html' %}
{% block content %}
<div class="text-center">
  <h1 class="text-success">&#10003; Order Confirmed</h1>
  <p>Thank you! Your order #{{ order.id }} has been placed.</p>
  <p>Total: £{{ "%.2f"|format(order.total) }}</p>
  <p>Status: {{ order.status }}</p>
  <a href="{{ url_for('browse_products') }}" class="btn btn-dark">Continue Shopping</a>
</div>
{% endblock %}
"""

TEMPLATES["buyer_orders.html"] = """
{% extends 'layout.html' %}
{% block content %}
<h2 class="mb-4">My Orders</h2>
{% if orders %}
<table class="table">
  <thead><tr><th>Order ID</th><th>Date</th><th>Total</th><th>Status</th></tr></thead>
  <tbody>
    {% for order in orders %}
    <tr>
      <td>#{{ order.id }}</td>
      <td>{{ order.created_at.strftime('%d %b %Y') }}</td>
      <td>£{{ "%.2f"|format(order.total) }}</td>
      <td><span class="badge {% if order.status=='Delivered' %}bg-success{% elif order.status=='Shipped' %}bg-info{% else %}bg-secondary{% endif %}">{{ order.status }}</span></td>
    </tr>
    {% endfor %}
  </tbody>
</table>
{% else %}
<p>You haven't placed any orders yet.</p>
{% endif %}
{% endblock %}
"""

TEMPLATES["vendor_dashboard.html"] = """
{% extends 'layout.html' %}
{% block content %}
<div class="d-flex justify-content-between align-items-center mb-4">
  <h2>My Products</h2>
  <a href="{{ url_for('add_product') }}" class="btn btn-dark">+ Add Product</a>
</div>
{% if products %}
<table class="table table-bordered align-middle">
  <thead><tr><th>Name</th><th>Price</th><th>Stock</th><th>Category</th><th>Actions</th></tr></thead>
  <tbody>
    {% for product in products %}
    <tr>
      <td>{{ product.name }}</td>
      <td>£{{ "%.2f"|format(product.price) }}</td>
      <td>{{ product.stock }}</td>
      <td>{{ product.category }}</td>
      <td>
        <a href="{{ url_for('edit_product', product_id=product.id) }}" class="btn btn-sm btn-outline-secondary">Edit</a>
        <form method="POST" action="{{ url_for('delete_product', product_id=product.id) }}" class="d-inline">
          <input type="hidden" name="csrf_token" value="{{ csrf_token() }}">
          <button type="submit" class="btn btn-sm btn-outline-danger">Delete</button>
        </form>
      </td>
    </tr>
    {% endfor %}
  </tbody>
</table>
{% else %}
<p>You haven't added any products yet.</p>
{% endif %}
{% endblock %}
"""

TEMPLATES["product_form.html"] = """
{% extends 'layout.html' %}
{% block content %}
<h2>{{ action }} Product</h2>
<form method="POST">
  {{ form.hidden_tag() }}
  <div class="mb-3">{{ form.name.label(class="form-label") }}{{ form.name(class="form-control") }}</div>
  <div class="mb-3">{{ form.description.label(class="form-label") }}{{ form.description(class="form-control", rows=4) }}</div>
  <div class="mb-3">{{ form.price.label(class="form-label") }}{{ form.price(class="form-control") }}</div>
  <div class="mb-3">{{ form.size.label(class="form-label") }}{{ form.size(class="form-select") }}</div>
  <div class="mb-3">{{ form.color.label(class="form-label") }}{{ form.color(class="form-control") }}</div>
  <div class="mb-3">{{ form.stock.label(class="form-label") }}{{ form.stock(class="form-control") }}</div>
  <div class="mb-3">{{ form.category.label(class="form-label") }}{{ form.category(class="form-select") }}</div>
  {{ form.submit(class="btn btn-dark") }}
</form>
{% endblock %}
"""

TEMPLATES["vendor_orders.html"] = """
{% extends 'layout.html' %}
{% block content %}
<h2 class="mb-4">Orders for My Products</h2>
{% if order_items %}
<table class="table align-middle">
  <thead><tr><th>Order ID</th><th>Product</th><th>Buyer</th><th>Qty</th><th>Status</th><th>Action</th></tr></thead>
  <tbody>
    {% for item in order_items %}
    <tr>
      <td>#{{ item.order.id }}</td>
      <td>{{ item.product.name }}</td>
      <td>{{ item.order.buyer.name }}</td>
      <td>{{ item.quantity }}</td>
      <td><span class="badge {% if item.order.status=='Delivered' %}bg-success{% elif item.order.status=='Shipped' %}bg-info{% else %}bg-secondary{% endif %}">{{ item.order.status }}</span></td>
      <td>
        {% if item.order.status == 'Pending' %}
        <form method="POST" action="{{ url_for('update_order_status', order_item_id=item.id) }}">
          <input type="hidden" name="csrf_token" value="{{ csrf_token() }}">
          <input type="hidden" name="status" value="Shipped">
          <button type="submit" class="btn btn-sm btn-outline-dark">Mark Shipped</button>
        </form>
        {% elif item.order.status == 'Shipped' %}
        <form method="POST" action="{{ url_for('update_order_status', order_item_id=item.id) }}">
          <input type="hidden" name="csrf_token" value="{{ csrf_token() }}">
          <input type="hidden" name="status" value="Delivered">
          <button type="submit" class="btn btn-sm btn-outline-dark">Mark Delivered</button>
        </form>
        {% else %}—{% endif %}
      </td>
    </tr>
    {% endfor %}
  </tbody>
</table>
{% else %}
<p>No orders yet for your products.</p>
{% endif %}
{% endblock %}
"""

TEMPLATES["admin_users.html"] = """
{% extends 'layout.html' %}
{% block content %}
<h2 class="mb-4">Manage Users</h2>
<table class="table align-middle">
  <thead><tr><th>Name</th><th>Email</th><th>Role</th><th>Status</th><th>Action</th></tr></thead>
  <tbody>
    {% for user in users %}
    <tr>
      <td>{{ user.name }}</td><td>{{ user.email }}</td><td>{{ user.role }}</td>
      <td><span class="badge {% if user.status=='active' %}bg-success{% else %}bg-secondary{% endif %}">{{ user.status }}</span></td>
      <td>
        {% if user.id != current_user.id %}
        <form method="POST" action="{{ url_for('toggle_user_status', user_id=user.id) }}">
          <input type="hidden" name="csrf_token" value="{{ csrf_token() }}">
          <button type="submit" class="btn btn-sm btn-outline-dark">{% if user.status=='active' %}Deactivate{% else %}Activate{% endif %}</button>
        </form>
        {% endif %}
      </td>
    </tr>
    {% endfor %}
  </tbody>
</table>
{% endblock %}
"""

TEMPLATES["admin_products.html"] = """
{% extends 'layout.html' %}
{% block content %}
<h2 class="mb-4">Manage Products</h2>
<table class="table align-middle">
  <thead><tr><th>Name</th><th>Vendor</th><th>Category</th><th>Price</th><th>Action</th></tr></thead>
  <tbody>
    {% for product in products %}
    <tr>
      <td>{{ product.name }}</td><td>{{ product.vendor.name }}</td><td>{{ product.category }}</td><td>£{{ "%.2f"|format(product.price) }}</td>
      <td>
        <form method="POST" action="{{ url_for('admin_remove_product', product_id=product.id) }}">
          <input type="hidden" name="csrf_token" value="{{ csrf_token() }}">
          <button type="submit" class="btn btn-sm btn-outline-danger">Remove</button>
        </form>
      </td>
    </tr>
    {% endfor %}
  </tbody>
</table>
{% endblock %}
"""

TEMPLATES["admin_orders.html"] = """
{% extends 'layout.html' %}
{% block content %}
<h2 class="mb-4">All Orders (Platform-wide)</h2>
<table class="table">
  <thead><tr><th>Order ID</th><th>Buyer</th><th>Total</th><th>Status</th><th>Date</th></tr></thead>
  <tbody>
    {% for order in orders %}
    <tr>
      <td>#{{ order.id }}</td><td>{{ order.buyer.name }}</td><td>£{{ "%.2f"|format(order.total) }}</td>
      <td><span class="badge {% if order.status=='Delivered' %}bg-success{% elif order.status=='Shipped' %}bg-info{% else %}bg-secondary{% endif %}">{{ order.status }}</span></td>
      <td>{{ order.created_at.strftime('%d %b %Y') }}</td>
    </tr>
    {% endfor %}
  </tbody>
</table>
{% endblock %}
"""

TEMPLATES["404.html"] = """
{% extends 'layout.html' %}
{% block content %}
<div class="text-center py-5"><h1 class="text-danger">404</h1><p>Page not found.</p><a href="{{ url_for('home') }}" class="btn btn-dark">Return to Home</a></div>
{% endblock %}
"""

TEMPLATES["500.html"] = """
{% extends 'layout.html' %}
{% block content %}
<div class="text-center py-5"><h1 class="text-danger">500</h1><p>Something went wrong on our end.</p><a href="{{ url_for('home') }}" class="btn btn-dark">Return to Home</a></div>
{% endblock %}
"""

app.jinja_loader = DictLoader(TEMPLATES)


# ---------------------------------------------------------------------------
# Routes — Auth
# ---------------------------------------------------------------------------
@app.route("/")
def home():
    featured_products = Product.query.order_by(Product.created_at.desc()).limit(8).all()
    return render_template("home.html", featured_products=featured_products)


@app.route("/register", methods=["GET", "POST"])
def register():
    if current_user.is_authenticated:
        return redirect(url_for("home"))
    form = RegisterForm()
    if form.validate_on_submit():
        if User.query.filter_by(email=form.email.data).first():
            flash("Email already registered. Please log in instead.", "danger")
            return redirect(url_for("register"))
        user = User(
            name=form.name.data, email=form.email.data,
            password_hash=generate_password_hash(form.password.data),
            role=form.role.data, status="active"
        )
        db.session.add(user)
        db.session.commit()
        flash("Registration successful! Please log in.", "success")
        return redirect(url_for("login"))
    return render_template("register.html", form=form)


@app.route("/login", methods=["GET", "POST"])
def login():
    if current_user.is_authenticated:
        return redirect(url_for("home"))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user is None or not check_password_hash(user.password_hash, form.password.data):
            flash("Invalid email or password.", "danger")
            return redirect(url_for("login"))
        if user.status == "deactivated":
            flash("This account has been deactivated. Contact admin.", "danger")
            return redirect(url_for("login"))
        login_user(user)
        flash(f"Welcome back, {user.name}!", "success")
        if user.role == "buyer":
            return redirect(url_for("browse_products"))
        elif user.role == "vendor":
            return redirect(url_for("vendor_products"))
        else:
            return redirect(url_for("manage_users"))
    return render_template("login.html", form=form)


@app.route("/logout")
@login_required
def logout():
    logout_user()
    flash("You have been logged out.", "info")
    return redirect(url_for("home"))


# ---------------------------------------------------------------------------
# Routes — Products (vendor + browsing)
# ---------------------------------------------------------------------------
def vendor_required():
    if current_user.role != "vendor":
        abort(403)


@app.route("/vendor/products")
@login_required
def vendor_products():
    vendor_required()
    products = Product.query.filter_by(vendor_id=current_user.id).all()
    return render_template("vendor_dashboard.html", products=products)


@app.route("/vendor/products/add", methods=["GET", "POST"])
@login_required
def add_product():
    vendor_required()
    form = ProductForm()
    if form.validate_on_submit():
        product = Product(
            vendor_id=current_user.id, name=form.name.data, description=form.description.data,
            price=form.price.data, size=form.size.data, color=form.color.data,
            stock=form.stock.data, category=form.category.data
        )
        db.session.add(product)
        db.session.commit()
        flash("Product added successfully!", "success")
        return redirect(url_for("vendor_products"))
    return render_template("product_form.html", form=form, action="Add")


@app.route("/vendor/products/edit/<int:product_id>", methods=["GET", "POST"])
@login_required
def edit_product(product_id):
    vendor_required()
    product = Product.query.get_or_404(product_id)
    if product.vendor_id != current_user.id:
        abort(403)
    form = ProductForm(obj=product)
    if form.validate_on_submit():
        form.populate_obj(product)
        db.session.commit()
        flash("Product updated successfully!", "success")
        return redirect(url_for("vendor_products"))
    return render_template("product_form.html", form=form, action="Edit")


@app.route("/vendor/products/delete/<int:product_id>", methods=["POST"])
@login_required
def delete_product(product_id):
    vendor_required()
    product = Product.query.get_or_404(product_id)
    if product.vendor_id != current_user.id:
        abort(403)
    db.session.delete(product)
    db.session.commit()
    flash("Product deleted.", "info")
    return redirect(url_for("vendor_products"))


@app.route("/products")
def browse_products():
    query = request.args.get("q", "")
    category = request.args.get("category", "")
    size = request.args.get("size", "")
    min_price = request.args.get("min_price", type=float)
    max_price = request.args.get("max_price", type=float)

    q = Product.query
    if query:
        q = q.filter(Product.name.ilike(f"%{query}%"))
    if category:
        q = q.filter_by(category=category)
    if size:
        q = q.filter_by(size=size)
    if min_price is not None:
        q = q.filter(Product.price >= min_price)
    if max_price is not None:
        q = q.filter(Product.price <= max_price)

    products = q.all()
    categories = ["Dresses", "Outerwear", "Tops", "Bottoms", "Accessories"]
    return render_template("product_list.html", products=products, categories=categories,
                            query=query, category=category, size=size,
                            min_price=min_price, max_price=max_price)


@app.route("/products/<int:product_id>")
def product_detail(product_id):
    product = Product.query.get_or_404(product_id)
    return render_template("product_detail.html", product=product)


# ---------------------------------------------------------------------------
# Routes — Cart
# ---------------------------------------------------------------------------
def buyer_required():
    if current_user.role != "buyer":
        abort(403)


@app.route("/cart/add/<int:product_id>", methods=["POST"])
@login_required
def add_to_cart(product_id):
    buyer_required()
    product = Product.query.get_or_404(product_id)
    quantity = request.form.get("quantity", 1, type=int)
    if quantity < 1 or quantity > product.stock:
        flash("Invalid quantity or not enough stock.", "danger")
        return redirect(url_for("product_detail", product_id=product_id))
    item = CartItem.query.filter_by(buyer_id=current_user.id, product_id=product_id).first()
    if item:
        item.quantity += quantity
    else:
        item = CartItem(buyer_id=current_user.id, product_id=product_id, quantity=quantity)
        db.session.add(item)
    db.session.commit()
    flash(f"{product.name} added to cart.", "success")
    return redirect(url_for("view_cart"))


@app.route("/cart")
@login_required
def view_cart():
    buyer_required()
    cart_items = CartItem.query.filter_by(buyer_id=current_user.id).all()
    total = sum(i.product.price * i.quantity for i in cart_items)
    return render_template("cart.html", cart_items=cart_items, total=total)


@app.route("/cart/update/<int:item_id>", methods=["POST"])
@login_required
def update_cart_item(item_id):
    buyer_required()
    item = CartItem.query.get_or_404(item_id)
    if item.buyer_id != current_user.id:
        abort(403)
    new_qty = request.form.get("quantity", 1, type=int)
    if new_qty < 1:
        db.session.delete(item)
    elif new_qty > item.product.stock:
        flash("Not enough stock available.", "danger")
        return redirect(url_for("view_cart"))
    else:
        item.quantity = new_qty
    db.session.commit()
    return redirect(url_for("view_cart"))


@app.route("/cart/remove/<int:item_id>", methods=["POST"])
@login_required
def remove_cart_item(item_id):
    buyer_required()
    item = CartItem.query.get_or_404(item_id)
    if item.buyer_id != current_user.id:
        abort(403)
    db.session.delete(item)
    db.session.commit()
    flash("Item removed from cart.", "info")
    return redirect(url_for("view_cart"))


# ---------------------------------------------------------------------------
# Routes — Checkout & Orders
# ---------------------------------------------------------------------------
@app.route("/checkout")
@login_required
def checkout():
    buyer_required()
    cart_items = CartItem.query.filter_by(buyer_id=current_user.id).all()
    if not cart_items:
        flash("Your cart is empty.", "danger")
        return redirect(url_for("view_cart"))
    total = sum(i.product.price * i.quantity for i in cart_items)
    return render_template("checkout.html", cart_items=cart_items, total=total)


@app.route("/checkout/confirm", methods=["POST"])
@login_required
def confirm_checkout():
    buyer_required()
    cart_items = CartItem.query.filter_by(buyer_id=current_user.id).all()
    if not cart_items:
        flash("Your cart is empty.", "danger")
        return redirect(url_for("view_cart"))
    for item in cart_items:
        if item.quantity > item.product.stock:
            flash(f"{item.product.name} no longer has enough stock.", "danger")
            return redirect(url_for("view_cart"))

    total = sum(i.product.price * i.quantity for i in cart_items)
    order = Order(buyer_id=current_user.id, total=total, status="Pending")
    db.session.add(order)
    db.session.flush()
    for item in cart_items:
        db.session.add(OrderItem(order_id=order.id, product_id=item.product_id,
                                  quantity=item.quantity, price_at_purchase=item.product.price))
        item.product.stock -= item.quantity
        db.session.delete(item)
    db.session.commit()
    flash("Order placed successfully! (Simulated/demo payment.)", "success")
    return redirect(url_for("order_confirmation", order_id=order.id))


@app.route("/order/confirmation/<int:order_id>")
@login_required
def order_confirmation(order_id):
    order = Order.query.get_or_404(order_id)
    if order.buyer_id != current_user.id:
        abort(403)
    return render_template("order_confirmation.html", order=order)


@app.route("/orders/my")
@login_required
def buyer_orders():
    buyer_required()
    orders = Order.query.filter_by(buyer_id=current_user.id).order_by(Order.created_at.desc()).all()
    return render_template("buyer_orders.html", orders=orders)


@app.route("/vendor/orders")
@login_required
def vendor_orders():
    if current_user.role != "vendor":
        abort(403)
    order_items = OrderItem.query.join(Product).filter(Product.vendor_id == current_user.id).all()
    return render_template("vendor_orders.html", order_items=order_items)


@app.route("/vendor/orders/update/<int:order_item_id>", methods=["POST"])
@login_required
def update_order_status(order_item_id):
    if current_user.role != "vendor":
        abort(403)
    item = OrderItem.query.get_or_404(order_item_id)
    if item.product.vendor_id != current_user.id:
        abort(403)
    new_status = request.form.get("status")
    valid = {"Pending": ["Shipped"], "Shipped": ["Delivered"], "Delivered": []}
    if new_status not in valid.get(item.order.status, []):
        flash("Invalid status transition.", "danger")
        return redirect(url_for("vendor_orders"))
    item.order.status = new_status
    db.session.commit()
    flash("Order status updated.", "success")
    return redirect(url_for("vendor_orders"))


# ---------------------------------------------------------------------------
# Routes — Admin
# ---------------------------------------------------------------------------
def admin_required():
    if current_user.role != "admin":
        abort(403)


@app.route("/admin/users")
@login_required
def manage_users():
    admin_required()
    users = User.query.all()
    return render_template("admin_users.html", users=users)


@app.route("/admin/users/toggle/<int:user_id>", methods=["POST"])
@login_required
def toggle_user_status(user_id):
    admin_required()
    user = User.query.get_or_404(user_id)
    if user.id == current_user.id:
        flash("You cannot deactivate your own account.", "danger")
        return redirect(url_for("manage_users"))
    user.status = "deactivated" if user.status == "active" else "active"
    db.session.commit()
    flash(f"{user.name} is now {user.status}.", "success")
    return redirect(url_for("manage_users"))


@app.route("/admin/products")
@login_required
def manage_products():
    admin_required()
    products = Product.query.all()
    return render_template("admin_products.html", products=products)


@app.route("/admin/products/remove/<int:product_id>", methods=["POST"])
@login_required
def admin_remove_product(product_id):
    admin_required()
    product = Product.query.get_or_404(product_id)
    db.session.delete(product)
    db.session.commit()
    flash("Product removed.", "info")
    return redirect(url_for("manage_products"))


@app.route("/admin/orders")
@login_required
def all_orders():
    admin_required()
    orders = Order.query.order_by(Order.created_at.desc()).all()
    return render_template("admin_orders.html", orders=orders)


# ---------------------------------------------------------------------------
# Error handlers
# ---------------------------------------------------------------------------
@app.errorhandler(403)
def forbidden(e):
    return render_template("404.html"), 403


@app.errorhandler(404)
def not_found(e):
    return render_template("404.html"), 404


@app.errorhandler(500)
def server_error(e):
    return render_template("500.html"), 500


# ---------------------------------------------------------------------------
# Seed demo data (runs once, only if the database is empty)
# ---------------------------------------------------------------------------
def seed_demo_data():
    if User.query.first():
        return  # already seeded

    admin = User(name="Amanta Admin", email="admin@amanta.test",
                 password_hash=generate_password_hash("AdminPass123"), role="admin")
    vendor = User(name="Chidinma Okafor", email="vendor@amanta.test",
                  password_hash=generate_password_hash("VendorPass123"), role="vendor")
    buyer = User(name="Tunde Bakare", email="buyer@amanta.test",
                 password_hash=generate_password_hash("BuyerPass123"), role="buyer")
    db.session.add_all([admin, vendor, buyer])
    db.session.commit()

    demo_products = [
        ("Ankara Print Dress", "Vibrant Ankara print, tailored fit, perfect for daytime events.", 45.00, "M", "Blue", 12, "Dresses"),
        ("Classic Denim Jacket", "Timeless denim jacket, lightly distressed finish.", 60.00, "L", "Blue", 8, "Outerwear"),
        ("Silk Blouse", "Soft silk blend blouse with a relaxed fit.", 38.50, "S", "Cream", 15, "Tops"),
        ("Tailored Wide-Leg Trousers", "High-waisted wide-leg trousers in a soft drape fabric.", 52.00, "M", "Black", 10, "Bottoms"),
        ("Statement Beaded Necklace", "Handmade beaded necklace, one-of-a-kind design.", 22.00, "M", "Multicolor", 20, "Accessories"),
        ("Linen Wrap Top", "Breathable linen wrap top, great for warm weather.", 34.00, "L", "White", 9, "Tops"),
        ("Pleated Midi Skirt", "Flowing pleated midi skirt with an elastic waist.", 41.00, "M", "Green", 7, "Bottoms"),
        ("Quilted Crossbody Bag", "Compact quilted crossbody bag with gold-tone hardware.", 29.99, "S", "Black", 14, "Accessories"),
    ]
    products = []
    for name, desc, price, size, color, stock, category in demo_products:
        prod = Product(vendor_id=vendor.id, name=name, description=desc, price=price,
                        size=size, color=color, stock=stock, category=category)
        db.session.add(prod)
        products.append(prod)
    db.session.commit()

    # Seed one existing order so vendor/admin order screens aren't empty
    order = Order(buyer_id=buyer.id, total=float(products[0].price) + float(products[4].price), status="Pending")
    db.session.add(order)
    db.session.flush()
    db.session.add(OrderItem(order_id=order.id, product_id=products[0].id, quantity=1, price_at_purchase=products[0].price))
    db.session.add(OrderItem(order_id=order.id, product_id=products[4].id, quantity=1, price_at_purchase=products[4].price))
    products[0].stock -= 1
    products[4].stock -= 1
    db.session.commit()

    print("Demo data seeded: 1 admin, 1 vendor (8 products), 1 buyer, 1 sample order.")


# ---------------------------------------------------------------------------
# Entry point
# ---------------------------------------------------------------------------
if __name__ == "__main__":
    with app.app_context():
        db.create_all()
        seed_demo_data()
    print("\nAmanta Collection demo running at http://127.0.0.1:5000")
    print("Admin:  admin@amanta.test  / AdminPass123")
    print("Vendor: vendor@amanta.test / VendorPass123")
    print("Buyer:  buyer@amanta.test  / BuyerPass123\n")
    app.run(debug=True)

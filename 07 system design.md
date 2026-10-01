# 7. System Design — Amanta Collection

## 7.1 System Architecture
Amanta Collection uses a classic 3-tier web architecture.

![System Architecture](../diagrams/architecture.png)

- **Presentation layer:** Browser (HTML + CSS + Bootstrap + JS) — renders pages, sends form submissions
- **Application layer:** Flask (Python) — routes, business logic (auth, cart, checkout...), Flask-Login (sessions), Flask-WTF (form validation, CSRF)
- **Data layer:** SQLite database — Users, Products, CartItems, Orders, OrderItems (accessed via SQLAlchemy ORM)

**Folder-level mapping:**
- Presentation layer → `templates/` (HTML/Jinja2) + `static/` (CSS/JS/images)
- Application layer → `app.py` / `routes/` (Flask route functions) + `forms.py` (Flask-WTF forms)
- Data layer → `models.py` (SQLAlchemy models) + `amanta.db` (SQLite file)

## 7.2 Database Design (ERD)
![Entity Relationship Diagram](../diagrams/erd.png)

**Relationships:**
- One **User** (vendor) → many **Products**
- One **User** (buyer) → many **CartItems** and many **Orders**
- One **Product** → many **CartItems** and many **OrderItems**
- One **Order** → many **OrderItems** (line items)

## 7.3 Database Tables

### `users`
| Field | Type | Constraints |
|---|---|---|
| id | INTEGER | PK, AUTOINCREMENT |
| name | VARCHAR(100) | NOT NULL |
| email | VARCHAR(120) | NOT NULL, UNIQUE |
| password_hash | VARCHAR(255) | NOT NULL |
| role | VARCHAR(20) | NOT NULL — 'buyer','vendor','admin' |
| status | VARCHAR(20) | DEFAULT 'active' — 'active','deactivated' |
| created_at | DATETIME | DEFAULT CURRENT_TIMESTAMP |

### `products`
| Field | Type | Constraints |
|---|---|---|
| id | INTEGER | PK, AUTOINCREMENT |
| vendor_id | INTEGER | FK → users.id, NOT NULL |
| name | VARCHAR(150) | NOT NULL |
| description | TEXT | |
| price | DECIMAL(10,2) | NOT NULL, > 0 |
| size | VARCHAR(10) | e.g. S/M/L/XL |
| color | VARCHAR(30) | |
| stock | INTEGER | NOT NULL, DEFAULT 0 |
| category | VARCHAR(50) | NOT NULL |
| image_path | VARCHAR(255) | |
| created_at | DATETIME | DEFAULT CURRENT_TIMESTAMP |

### `cart_items`
| Field | Type | Constraints |
|---|---|---|
| id | INTEGER | PK, AUTOINCREMENT |
| buyer_id | INTEGER | FK → users.id, NOT NULL |
| product_id | INTEGER | FK → products.id, NOT NULL |
| quantity | INTEGER | NOT NULL, DEFAULT 1 |

### `orders`
| Field | Type | Constraints |
|---|---|---|
| id | INTEGER | PK, AUTOINCREMENT |
| buyer_id | INTEGER | FK → users.id, NOT NULL |
| total | DECIMAL(10,2) | NOT NULL |
| status | VARCHAR(20) | DEFAULT 'Pending' — Pending/Shipped/Delivered |
| created_at | DATETIME | DEFAULT CURRENT_TIMESTAMP |

### `order_items`
| Field | Type | Constraints |
|---|---|---|
| id | INTEGER | PK, AUTOINCREMENT |
| order_id | INTEGER | FK → orders.id, NOT NULL |
| product_id | INTEGER | FK → products.id, NOT NULL |
| quantity | INTEGER | NOT NULL |
| price_at_purchase | DECIMAL(10,2) | NOT NULL — snapshot of price when ordered |

## 7.4 Sample Records
**users**
| id | name | email | role | status |
|---|---|---|---|---|
| 1 | Amanta Admin | admin@amanta.test | admin | active |
| 2 | Chidinma Okafor | chidinma@example.test | vendor | active |
| 3 | Tunde Bakare | tunde@example.test | buyer | active |

**products**
| id | vendor_id | name | price | size | color | stock | category |
|---|---|---|---|---|---|---|---|
| 1 | 2 | Ankara Print Dress | 45.00 | M | Blue | 10 | Dresses |
| 2 | 2 | Denim Jacket | 60.00 | L | Blue | 5 | Outerwear |

## 7.5 Input / Output and Interface Design
**System Inputs:** registration data, login credentials, product data (name, description, price, size, color, stock, category, image), search/filter criteria, cart actions, checkout/demo payment confirmation, order status updates, admin actions.

**System Outputs:** registration/login confirmation or error messages, product listing/search results, product detail pages, cart summary with running total, order confirmation receipt, order history, order management lists, admin dashboards, validation/error messages.

**UI/UX Pages designed:** Home, Registration, Login, Product Listing (Search Results), Product Details, Search, Cart, Checkout, Buyer Dashboard, Vendor Dashboard, Admin Dashboard, Orders, Profile, Error/Success pages — all sharing a common navbar/footer via a single base layout template for interface consistency.

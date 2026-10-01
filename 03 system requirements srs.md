# 3. Software Requirements Specification (SRS) — Amanta Collection

## 3.1 Functional Requirements

### Authentication & User Management
- **FR1:** The system shall allow users to register as a Buyer or Vendor with email, password, and role selection.
- **FR2:** The system shall allow registered users to log in and log out securely.
- **FR3:** The system shall hash and store passwords securely (never plain text).
- **FR4:** The system shall enforce role-based access control (buyer/vendor/admin see different features).
- **FR5:** The system shall allow users to update their profile information.

### Product Management (Vendor)
- **FR6:** The system shall allow vendors to create new product listings (name, description, price, size, color, stock, image, category).
- **FR7:** The system shall allow vendors to edit their own product listings.
- **FR8:** The system shall allow vendors to delete their own product listings.
- **FR9:** The system shall allow vendors to view a list of their own products.

### Search & Browsing (Buyer)
- **FR10:** The system shall allow buyers to browse all available products.
- **FR11:** The system shall allow buyers to search products by keyword.
- **FR12:** The system shall allow buyers to filter products by category, price range, and size.
- **FR13:** The system shall display full product details on a dedicated page.

### Shopping Cart
- **FR14:** The system shall allow buyers to add products to a cart.
- **FR15:** The system shall allow buyers to update item quantity in the cart.
- **FR16:** The system shall allow buyers to remove items from the cart.
- **FR17:** The system shall calculate and display the cart total automatically.

### Checkout & Orders
- **FR18:** The system shall allow buyers to check out their cart and create an order.
- **FR19:** The system shall simulate a demo payment step (no real payment gateway).
- **FR20:** The system shall generate an order confirmation upon successful checkout.
- **FR21:** The system shall allow buyers to view their order history.
- **FR22:** The system shall allow vendors to view and update the status of orders containing their products (Pending → Shipped → Delivered).

### Admin
- **FR23:** The system shall allow admins to view and manage all users (activate/deactivate accounts).
- **FR24:** The system shall allow admins to view and manage all products (e.g., remove inappropriate listings).
- **FR25:** The system shall allow admins to view all orders platform-wide.

## 3.2 Non-Functional Requirements
| ID | Attribute | Description |
|---|---|---|
| NFR1 | Security | Passwords hashed (PBKDF2 via Werkzeug); sessions protected against CSRF |
| NFR2 | Performance | Pages load within 2 seconds under normal demo conditions |
| NFR3 | Usability | UI navigable without training, familiar e-commerce UX conventions |
| NFR4 | Reliability | System handles invalid input gracefully (no crashes on bad form data) |
| NFR5 | Maintainability | Code organized into clear modules (models, routes, templates) |
| NFR6 | Portability | Runs on any machine with Python 3.x, no OS-specific dependencies |
| NFR7 | Scalability (academic scope) | Supports at least 50 dummy products and 10 dummy users without issues |

## 3.3 Hardware Requirements
- Development: any laptop/PC with 4GB+ RAM, 1GB free disk space
- Deployment (demo): runs locally; no special server hardware needed

## 3.4 Software Requirements
- Python 3.10+
- Flask, Flask-SQLAlchemy, Flask-Login, Flask-WTF
- SQLite (bundled with Python)
- A code editor (VS Code recommended)
- A modern web browser (Chrome/Firefox/Edge) for testing

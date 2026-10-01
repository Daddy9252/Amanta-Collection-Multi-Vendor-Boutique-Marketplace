# Amanta Collection — Multi-Vendor Boutique Marketplace

A Flask-based marketplace e-commerce coursework application where independent
boutique vendors list clothing items and buyers browse, cart, and checkout.

## Setup

1. Create and activate a virtual environment:
   ```
   python -m venv venv
   venv\Scripts\activate        (Windows)
   source venv/bin/activate     (Mac/Linux)
   ```

2. Install dependencies:
   ```
   pip install -r requirements.txt
   ```

3. Create the database (first run only):
   ```
   python create_db.py
   ```
   This also creates a default admin account:
   - Email: admin@amanta.test
   - Password: AdminPass123

4. Run the app:
   ```
   python app.py
   ```

5. Visit http://127.0.0.1:5000

## Roles
- **Buyer** — browse, search, cart, checkout, view order history
- **Vendor** — manage own products, fulfil own orders (register as Vendor)
- **Admin** — manage users/products, view all orders (use the seeded admin account above)

## Notes
- Checkout uses a simulated/demo payment — no real payment processor is integrated.
- SECRET_KEY in config.py is a development placeholder; replace it before any real deployment.

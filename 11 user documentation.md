# 11. User Documentation — Amanta Collection

## 11.1 Installation Guide

**Prerequisites:** Python 3.10+, a web browser.

```bash
# 1. Create and activate a virtual environment
python -m venv venv
venv\Scripts\activate          # Windows
source venv/bin/activate       # Mac/Linux

# 2. Install dependencies
pip install -r requirements.txt

# 3. Create the database (first-time setup only)
python create_db.py

# 4. Run the application
python app.py

# 5. Open your browser to:
http://127.0.0.1:5000
```

`create_db.py` also seeds a default admin account:
- Email: `admin@amanta.test`
- Password: `AdminPass123`

## 11.2 Buyer Manual

**Creating an account**
1. Click "Register" in the top navigation.
2. Fill in your name, email, and password; select "Buyer" as your role.
3. Click "Register", then log in with your new credentials.

**Browsing and searching**
- Use the search bar in the navbar to find products by keyword.
- Click "Shop All Products" from the home page to browse everything.
- Use the filters on the left (Category, Size, Price) to narrow results.

**Buying a product**
1. Click "View" on any product to see full details.
2. Choose a quantity and click "Add to Cart".
3. Click "Cart" in the navbar to review your items.
4. Adjust quantities or remove items as needed.
5. Click "Proceed to Checkout".
6. Review your order summary and click "Confirm & Place Order" (simulated payment — no real charge occurs).

**Tracking orders**
- Click "My Orders" in the navbar to see all past orders and their current status (Pending / Shipped / Delivered).

## 11.3 Vendor Manual

**Creating an account:** Register as above, selecting "Vendor" as your role.

**Adding a product**
1. Click "My Products" in the navbar.
2. Click "+ Add Product".
3. Fill in name, description, price, size, color, stock quantity, category, and upload an image.
4. Click "Save Product".

**Editing or removing a product:** From "My Products", click "Edit" to change details, or "Delete" to remove it permanently.

**Managing orders**
1. Click "Orders" in the navbar to see all orders containing your products.
2. Click "Mark Shipped" once you've dispatched an item.
3. Click "Mark Delivered" once the buyer has received it.

## 11.4 Administrator Manual

**Logging in:** Use the seeded admin account created by `create_db.py` (or any account you manually promote to `role='admin'` in the database).

**Managing users**
1. Click "Users" in the navbar.
2. Click "Deactivate" to suspend a user's account, or "Activate" to restore it.

**Managing products**
1. Click "Products" in the navbar.
2. Click "Remove" to permanently delete any listing from the platform.

**Viewing all orders:** Click "All Orders" to see every order placed across the entire platform.

## 11.5 FAQ

**Q: I forgot my password — how do I reset it?**
A: Password reset is not implemented in this version (out of scope for this coursework). Contact the administrator.

**Q: Why can't I see other vendors' order management options?**
A: Each vendor can only manage orders containing their own products — this protects buyer and vendor data between unrelated sellers.

**Q: Is my payment information real/charged?**
A: No. Checkout uses a simulated/demo payment step for academic purposes — no real payment processor is integrated.

**Q: Why was my account deactivated?**
A: Accounts can be deactivated by an administrator. Contact the administrator for details.

**Q: Can a buyer also become a vendor?**
A: Not with the same account in this version — each account has a single fixed role (Buyer, Vendor, or Admin) assigned at registration.

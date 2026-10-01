# 9. Testing Evidence — Amanta Collection

## Test Plan
**Objective:** Verify FR1–FR25 and key NFRs work correctly across Buyer, Vendor, and Admin roles.
**Approach:** Manual black-box testing.
**Environment:** Local development server (http://127.0.0.1:5000), Chrome/Firefox, Windows.

## Test Case Table

> Fill in **Actual Result** and **Pass/Fail** as you run each test against your running application.

| ID | Test Case | Steps | Test Input | Expected Result | Actual Result | Pass/Fail |
|---|---|---|---|---|---|---|
| TC01 | Register new buyer | Go to Register, fill form, submit | Valid name/email/password, role=Buyer | Account created, redirected to login | | |
| TC02 | Register with duplicate email | Register using an existing email | Existing email | Error: "Email already registered" | | |
| TC03 | Register with short password | Register using <8 char password | Password: "abc" | Validation error shown | | |
| TC04 | Login with correct credentials | Log in with valid buyer account | Correct email/password | Redirected to product browsing page | | |
| TC05 | Login with wrong password | Log in with incorrect password | Wrong password | Error: "Invalid email or password" | | |
| TC06 | Login as deactivated user | Log in with a deactivated account | Deactivated account creds | Error: "Account deactivated" | | |
| TC07 | Logout | Click Logout while logged in | — | Redirected to home, session ended | | |
| TC08 | Vendor adds product | Login as vendor, Add Product form | Valid product data + image | Product appears in "My Products" | | |
| TC09 | Add product with invalid price | Enter price = 0 or negative | Price: -5 | Validation error shown | | |
| TC10 | Vendor edits own product | Edit an existing product | New price | Product updated correctly | | |
| TC11 | Vendor cannot edit others' product | Try accessing another vendor's edit URL directly | Product ID not owned | 403 Forbidden | | |
| TC12 | Vendor deletes product | Click Delete on own product | — | Product removed from list | | |
| TC13 | Buyer searches products | Enter keyword in navbar search | e.g. "dress" | Matching products shown | | |
| TC14 | Buyer filters by category/size/price | Apply filters on product list page | e.g. category=Dresses | Only matching products shown | | |
| TC15 | View product detail page | Click "View" on a product | — | Full product details shown | | |
| TC16 | Add product to cart | On product detail, select qty, Add to Cart | Qty=2 | Item appears in cart with correct subtotal | | |
| TC17 | Add more than available stock | Enter qty > stock | Qty=999 | Error: "Not enough stock" | | |
| TC18 | Update cart quantity | Change quantity in cart, click Update | New qty | Cart total recalculates | | |
| TC19 | Remove cart item | Click Remove on a cart item | — | Item removed, total updates | | |
| TC20 | Checkout with items in cart | Go to Checkout, confirm demo payment | — | Order created, confirmation page shown | | |
| TC21 | Checkout with empty cart | Navigate to /checkout with empty cart | — | Redirected to cart with "Cart is empty" message | | |
| TC22 | Stock decreases after order | Check product stock before/after checkout | — | Stock reduced by quantity ordered | | |
| TC23 | Cart clears after checkout | Check cart after placing order | — | Cart is empty | | |
| TC24 | Buyer views order history | Go to "My Orders" | — | List of past orders with correct status | | |
| TC25 | Vendor views orders for own products | Go to "Orders" as vendor | — | Only orders containing their products shown | | |
| TC26 | Vendor updates order status | Click "Mark Shipped" / "Mark Delivered" | — | Status updates, reflected in buyer's order history | | |
| TC27 | Admin deactivates a user | Go to Users, click Deactivate | — | User status changes, cannot log in | | |
| TC28 | Admin removes a product | Go to Products, click Remove | — | Product deleted from catalog | | |
| TC29 | Admin views all orders | Go to All Orders | — | Every platform order listed | | |
| TC30 | Unauthorized access to vendor route | As a buyer, navigate directly to `/vendor/products` | — | 403 Forbidden | | |
| TC31 | Unauthorized access to admin route | As a vendor, navigate directly to `/admin/users` | — | 403 Forbidden | | |
| TC32 | Password stored hashed | Inspect `users` table in DB Browser for SQLite | — | `password_hash` column shows a long hash, not plain text | | |
| TC33 | CSRF token present | View page source of any form | — | Hidden `csrf_token` input present | | |
| TC34 | 404 error handling | Visit a non-existent URL | — | Styled 404 page shown, not a stack trace | | |

## How to perform these tests
1. Run `python app.py` and keep the terminal open to watch for errors.
2. Work through the table top to bottom using 2–3 test accounts (buyer, vendor, admin).
3. Fill in **Actual Result** and **Pass/Fail** for each row.
4. If something fails: fix the code, re-test, and update the table.

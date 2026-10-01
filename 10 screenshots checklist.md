# 10. Screenshots Checklist — Amanta Collection

> These screenshots must be captured from **your own running application** — they cannot be generated for you. Capture each one and save it into a `screenshots/` folder with the filename shown, then reference them in your final report.

## A. Setup & Environment
- [ ] `01_project_structure.png` — VS Code sidebar showing full folder structure
- [ ] `02_app_running.png` — terminal showing `python app.py` running without errors
- [ ] `03_database_created.png` — `amanta.db` file visible in project folder, or DB Browser showing all 5 tables

## B. Authentication
- [ ] `04_register_form.png` — empty registration form
- [ ] `05_register_success.png` — success message after registering
- [ ] `06_login_form.png` — login page
- [ ] `07_login_error.png` — invalid credentials error
- [ ] `08_logged_in_navbar.png` — navbar showing "Hi, [name]" and role-specific links

## C. Buyer Features
- [ ] `09_home_page.png` — home page with hero banner + featured products
- [ ] `10_search_results.png` — product list filtered by a search term
- [ ] `11_filters_applied.png` — product list with category/size/price filters applied
- [ ] `12_product_detail.png` — full product detail page
- [ ] `13_add_to_cart.png` — confirmation after adding an item to cart
- [ ] `14_cart_view.png` — cart page with multiple items and correct total
- [ ] `15_stock_error.png` — error when requesting more than available stock
- [ ] `16_checkout_summary.png` — checkout page with order summary
- [ ] `17_order_confirmation.png` — order confirmation page
- [ ] `18_order_history.png` — buyer's "My Orders" page

## D. Vendor Features
- [ ] `19_vendor_add_product.png` — add product form filled in
- [ ] `20_vendor_products_list.png` — vendor's product list with at least 2-3 products
- [ ] `21_vendor_edit_product.png` — edit product form
- [ ] `22_vendor_delete_confirm.png` — delete confirmation dialog
- [ ] `23_vendor_orders.png` — vendor's order list
- [ ] `24_order_status_update.png` — order status changed to "Shipped"

## E. Admin Features
- [ ] `25_admin_users.png` — admin user management table
- [ ] `26_admin_deactivate.png` — a user shown as "deactivated"
- [ ] `27_admin_products.png` — admin product management table
- [ ] `28_admin_all_orders.png` — admin's platform-wide order view

## F. Security Evidence
- [ ] `29_password_hashed.png` — DB Browser view showing hashed password in `users` table
- [ ] `30_csrf_token.png` — page source (Ctrl+U) showing hidden `csrf_token` input in a form
- [ ] `31_403_forbidden.png` — forbidden page when a buyer tries to access a vendor-only URL directly
- [ ] `32_404_page.png` — styled custom 404 page

## G. Responsiveness
- [ ] `33_mobile_view.png` — home page or product list shown in a narrow browser window (or browser dev tools "mobile" view)

# 4. Algorithms — Amanta Collection

## 4.1 Registration / Login

### Register User
```
START
1. Display registration form (name, email, password, role)
2. Receive user input
3. Validate input:
   a. IF email already exists in database THEN
        Display error "Email already registered"
        GOTO Step 1
   b. IF password length < 8 THEN
        Display error "Password too short"
        GOTO Step 1
4. Hash the password using a secure hashing algorithm
5. Create new User record with name, email, password_hash, role
6. Save User record to database
7. Display success message
8. Redirect to login page
END
```

### Login User
```
START
1. Display login form (email, password)
2. Receive user input
3. Look up user by email in database
4. IF user not found THEN
     Display error "Invalid credentials"
     GOTO Step 1
5. Verify submitted password against stored password_hash
6. IF verification fails THEN
     Display error "Invalid credentials"
     GOTO Step 1
7. Create authenticated session for user
8. Redirect based on role:
     IF role = Buyer THEN go to Buyer Dashboard
     IF role = Vendor THEN go to Vendor Dashboard
     IF role = Admin THEN go to Admin Dashboard
END
```

## 4.2 Product Management (Vendor)
```
START (Create Product)
1. Vendor navigates to "Add Product" form
2. Receive input: name, description, price, size, color, stock, category, image
3. Validate input:
   a. IF price <= 0 THEN display error, GOTO Step 1
   b. IF stock < 0 THEN display error, GOTO Step 1
   c. IF required fields missing THEN display error, GOTO Step 1
4. Create Product record linked to logged-in vendor's ID
5. Save Product record to database
6. Display success message
7. Redirect to vendor's product list
END
```
*(Edit/Delete follow the same pattern: fetch product by ID, verify it belongs to the logged-in vendor, then update or remove the record.)*

## 4.3 Shopping Cart
```
START (Add to Cart)
1. Buyer selects a product and quantity
2. IF quantity requested > available stock THEN
     Display error "Insufficient stock"
     STOP
3. IF product already exists in buyer's cart THEN
     Update existing cart item quantity += requested quantity
   ELSE
     Create new CartItem record (buyer_id, product_id, quantity)
4. Save cart changes
5. Recalculate and display cart total
END
```

## 4.4 Checkout
```
START (Checkout)
1. Buyer navigates to cart and selects "Checkout"
2. IF cart is empty THEN
     Display error "Cart is empty"
     STOP
3. Display order summary (items, quantities, total)
4. Buyer confirms demo payment step
5. FOR EACH item in cart:
     a. IF stock < quantity THEN
          Display error "Item no longer available"
          STOP
     b. Decrease product stock by quantity
6. Create Order record (buyer_id, total, status = "Pending", created_at)
7. FOR EACH item in cart:
     Create OrderItem record (order_id, product_id, quantity, price_at_purchase)
8. Clear buyer's cart
9. Display order confirmation
END
```

## 4.5 Order Management (Update)
```
START (Vendor Updates Order Status)
1. Vendor views list of orders containing their products
2. Vendor selects an order and chooses new status (e.g. Shipped)
3. Validate status transition is logical (e.g. cannot go from Delivered back to Pending)
4. Update order status in database
5. Display updated status to vendor
6. (Buyer sees updated status next time they view order history)
END
```

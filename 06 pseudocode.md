# 6. Pseudocode — Amanta Collection

Language-independent pseudocode for the major system functions.

## 6.1 Register User
```
FUNCTION registerUser(name, email, password, role)
    IF findUserByEmail(email) EXISTS THEN
        RETURN error "Email already registered"
    END IF

    IF LENGTH(password) < 8 THEN
        RETURN error "Password must be at least 8 characters"
    END IF

    hashedPassword = HASH(password)
    newUser = CREATE User WITH (name, email, hashedPassword, role)
    SAVE newUser TO database
    RETURN success "Registration successful"
END FUNCTION
```

## 6.2 Login User
```
FUNCTION loginUser(email, password)
    user = findUserByEmail(email)
    IF user DOES NOT EXIST THEN
        RETURN error "Invalid credentials"
    END IF

    IF VERIFY(password, user.hashedPassword) == FALSE THEN
        RETURN error "Invalid credentials"
    END IF

    CREATE session FOR user
    IF user.role == "Buyer" THEN
        REDIRECT TO buyerDashboard
    ELSE IF user.role == "Vendor" THEN
        REDIRECT TO vendorDashboard
    ELSE IF user.role == "Admin" THEN
        REDIRECT TO adminDashboard
    END IF
END FUNCTION
```

## 6.3 Add Product (Vendor)
```
FUNCTION addProduct(vendorId, name, description, price, size, color, stock, category, image)
    IF price <= 0 OR stock < 0 THEN
        RETURN error "Invalid price or stock"
    END IF

    newProduct = CREATE Product WITH (vendorId, name, description, price, size, color, stock, category, image)
    SAVE newProduct TO database
    RETURN success "Product added"
END FUNCTION
```

## 6.4 Search Products
```
FUNCTION searchProducts(keyword, category, minPrice, maxPrice, size)
    results = ALL products WHERE
        (name CONTAINS keyword OR description CONTAINS keyword)
        AND (category matches category, IF provided)
        AND (price BETWEEN minPrice AND maxPrice, IF provided)
        AND (size matches size, IF provided)
    RETURN results
END FUNCTION
```

## 6.5 Add to Cart
```
FUNCTION addToCart(buyerId, productId, quantity)
    product = findProductById(productId)
    IF quantity > product.stock THEN
        RETURN error "Insufficient stock"
    END IF

    existingItem = findCartItem(buyerId, productId)
    IF existingItem EXISTS THEN
        existingItem.quantity = existingItem.quantity + quantity
        SAVE existingItem
    ELSE
        newItem = CREATE CartItem WITH (buyerId, productId, quantity)
        SAVE newItem TO database
    END IF

    RETURN updatedCartTotal(buyerId)
END FUNCTION
```

## 6.6 Checkout
```
FUNCTION checkout(buyerId)
    cartItems = getCartItems(buyerId)
    IF cartItems IS EMPTY THEN
        RETURN error "Cart is empty"
    END IF

    FOR EACH item IN cartItems
        product = findProductById(item.productId)
        IF item.quantity > product.stock THEN
            RETURN error "Item no longer available: " + product.name
        END IF
    END FOR

    newOrder = CREATE Order WITH (buyerId, total = SUM(cartItems.price * cartItems.quantity), status = "Pending", createdAt = NOW())
    SAVE newOrder TO database

    FOR EACH item IN cartItems
        CREATE OrderItem WITH (newOrder.id, item.productId, item.quantity, item.priceAtPurchase)
        product.stock = product.stock - item.quantity
        SAVE product
    END FOR

    CLEAR cart FOR buyerId
    RETURN success newOrder
END FUNCTION
```

## 6.7 Update Order Status (Vendor)
```
FUNCTION updateOrderStatus(orderId, newStatus, vendorId)
    order = findOrderById(orderId)
    IF order CONTAINS product belonging to vendorId == FALSE THEN
        RETURN error "Unauthorized"
    END IF

    IF isValidStatusTransition(order.status, newStatus) == FALSE THEN
        RETURN error "Invalid status change"
    END IF

    order.status = newStatus
    SAVE order TO database
    RETURN success "Order status updated"
END FUNCTION
```

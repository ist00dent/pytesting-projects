class MockDatabase:
    def __init__(self):
        self.users = {}
        self.products = {}
        self.orders = {}
        self.sessions = {}
        self.login_attempts = {}
        self.reset_tokens = {}

    def reset(self):
        """Reset the mock database."""
        self.__init__()

    # ----------------- User Management -----------------

    def add_user(self, username, password, email):
        """Create a new user in the database."""
        if self.username_exists(username):
            raise ValueError("User already exists.")
        self.users[username] = {"password": password, "email": email}
        return True

    def validate_user(self, username, password):
        """Validate user credentials."""
        user = self.users.get(username)
        if not user or user["password"] != password:
            raise ValueError("Invalid credentials.")
        return True

    def update_user_email(self, username, new_email):
        """Update the email address for an existing user."""
        if not self.username_exists(username):
            raise ValueError("User not found.")
        self.users[username]["email"] = new_email
        return True

    def delete_user(self, username):
        """Delete an existing user from the database."""
        if not self.username_exists(username):
            raise ValueError("User not found.")
        del self.users[username]
        return True

    def username_exists(self, username):
        """Check if a username exists."""
        return username in self.users

    def email_exists(self, email):
        """Check if an email exists."""
        print(self.users)
        return any(user["email"] == email for user in self.users.values())

    # ----------------- Login Tracking -----------------

    def increment_login_attempts(self, username):
        """Increment the login attempt count for a user."""
        self.login_attempts[username] = self.get_login_attempts(username) + 1

    def get_login_attempts(self, username):
        """Get the login attempt count for a user."""
        return self.login_attempts.get(username, 0)

    # ----------------- Password Reset -----------------

    def generate_reset_token(self, email):
        """Generate a password reset token for a user."""
        token = f"reset-token-{email}"
        self.reset_tokens[email] = token
        return token

    def verify_reset_token(self, email, token):
        """Verify a password reset token."""
        return self.reset_tokens.get(email) == token

    # ----------------- Product Management -----------------

    def add_product(self, product_id, details):
        """Add a new product to the catalog."""
        if self.product_exists(product_id):
            raise ValueError("Product already exists.")
        self.products[product_id] = details
        return True

    def edit_product(self, product_id, new_details):
        """Edit an existing product's details."""
        if not self.product_exists(product_id):
            raise ValueError("Product not found.")
        self.products[product_id].update(new_details)
        return True

    def delete_product(self, product_id):
        """Delete a product from the catalog."""
        if not self.product_exists(product_id):
            raise ValueError("Product not found.")
        del self.products[product_id]
        return True

    def product_exists(self, product_id):
        """Check if a product exists."""
        return product_id in self.products

    # ----------------- Order Management -----------------

    def place_order(self, username, cart):
        """Place a new order for a user."""
        if not self.username_exists(username):
            raise ValueError("User not found.")
        order_id = f"ORD{len(self.orders) + 1}"
        self.orders[order_id] = {"user": username, "cart": cart, "status": "pending"}
        return order_id

    def update_order_status(self, order_id, status):
        """Update the status of an order."""
        if not self.order_exists(order_id):
            raise ValueError("Order not found.")
        self.orders[order_id]["status"] = status
        return True

    def order_exists(self, order_id):
        """Check if an order exists."""
        return order_id in self.orders

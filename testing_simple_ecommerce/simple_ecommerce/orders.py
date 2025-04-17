import json
import os
from datetime import datetime


class InvalidProductError(Exception):
    pass


def calculate_order_total(cart):
    if not cart:
        return 0.0
    total = sum(
        item["price"] * item["quantity"] for item in cart if item["quantity"] > 0
    )
    return round(total, 2)


def validate_product(product):
    if "id" not in product or "price" not in product or "quantity" not in product:
        raise InvalidProductError("Missing required product fields.")
    if product["price"] < 0 or product["quantity"] < 0:
        raise InvalidProductError("Invalid product price or quantity.")
    return True


def save_order(filepath, order_data):
    os.makedirs(os.path.dirname(filepath), exist_ok=True)
    with open(filepath, "w") as f:
        json.dump(order_data, f)


def load_order(filepath):
    with open(filepath, "r") as f:
        return json.load(f)


def apply_discount(cart, discount_percent):
    if not 0 <= discount_percent <= 100:
        raise ValueError("Discount percent must be between 0 and 100.")
    total = calculate_order_total(cart)
    discounted = total * (1 - discount_percent / 100)
    return round(discounted, 2)


def generate_order_id():
    return f"ORD-{datetime.utcnow().strftime('%Y%m%d%H%M%S%f')}"


def create_order(customer, cart):
    for product in cart:
        validate_product(product)
    total = calculate_order_total(cart)
    order = {
        "order_id": generate_order_id(),
        "customer": customer,
        "items": cart,
        "total": total,
        "timestamp": datetime.utcnow().isoformat(),
    }
    return order


def add_shipping_fee(order, fee):
    if fee < 0:
        raise ValueError("Shipping fee cannot be negative.")
    order["total"] += round(fee, 2)
    return order

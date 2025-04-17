import pytest
import json
from testing_simple_ecommerce.simple_ecommerce.orders import (
    calculate_order_total,
    validate_product,
    InvalidProductError,
    save_order,
    load_order,
    apply_discount,
    generate_order_id,
    create_order,
)


@pytest.mark.parametrize(
    "cart, expected",
    [
        ([{"price": 10, "quantity": 2}], 20.00),
        ([{"price": 15.5, "quantity": 1}, {"price": 4.5, "quantity": 3}], 29.0),
        ([], 0.0),
    ],
)
def test_calculate_order_total(cart, expected):
    assert calculate_order_total(cart) == expected


def test_validate_product_success():
    assert validate_product({"id": 1, "price": 10, "quantity": 1}) is True


@pytest.mark.parametrize(
    "product",
    [
        {"id": 1, "quantity": 1},
        {"price": 10, "quantity": 1},
        {"id": 1, "price": -5, "quantity": 2},
    ],
)
def test_validate_product_fail(product):
    with pytest.raises(InvalidProductError):
        validate_product(product)


def test_save_and_load_order(tmp_path):
    order = {"customer": "John", "total": 99.99}
    filepath = tmp_path / "orders" / "order.json"
    save_order(filepath, order)
    assert load_order(filepath) == order


def test_calculate_order_total_negative_quantity():
    cart = [{"price": 10, "quantity": -5}]
    assert calculate_order_total(cart) == 0.0


def test_save_order_mocked(tmp_path, mocker):
    mock_makedirs = mocker.patch(
        "testing_simple_ecommerce.simple_ecommerce.orders.os.makedirs"
    )
    order = {"customer": "Jane", "total": 45.0}
    filepath = tmp_path / "mocked.json"
    save_order(filepath, order)
    mock_makedirs.assert_called_once()
    assert json.loads(filepath.read_text()) == order


def test_apply_discount():
    cart = [{"price": 50, "quantity": 2}]
    assert apply_discount(cart, 10) == 90.0


def test_apply_discount_invalid():
    cart = [{"price": 50, "quantity": 2}]
    with pytest.raises(ValueError):
        apply_discount(cart, 150)


def test_generate_order_id_format():
    order_id = generate_order_id()
    assert order_id.startswith("ORD-")


def test_create_order_success():
    cart = [{"id": 1, "price": 10, "quantity": 2}]
    order = create_order("Alice", cart)
    assert order["customer"] == "Alice"
    assert "order_id" in order
    assert "timestamp" in order
    assert order["total"] == 20.0


def test_create_order_invalid_product():
    cart = [{"id": 1, "price": -10, "quantity": 1}]
    with pytest.raises(InvalidProductError):
        create_order("Bob", cart)

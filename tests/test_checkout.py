import app as app_module

def seed_cart(client):
    client.post("/add-to-cart", data={"title": "1984", "quantity": "2"}, follow_redirects=True)

def test_discount_codes_case_insensitive(client):
    # Arrange: subtotal = 2 * 8.99 = 17.98
    seed_cart(client)
    resp = client.post("/process-checkout", data={
        "name": "Alice",
        "email": "alice@example.com",
        "address": "1 Road",
        "city": "Town",
        "zip_code": "12345",
        "payment_method": "credit_card",
        "card_number": "4242424242424242",
        "expiry_date": "12/30",
        "cvv": "123",
        "discount_code": "save10",  # lower-case on purpose
    }, follow_redirects=True)
    assert resp.status_code == 200

    # Get the most recent order without using session
    assert app_module.orders, "No orders found after checkout"
    order = max(app_module.orders.values(), key=lambda o: o.order_date)

    # With 10% off, expected total = 17.98 * 0.90 = 16.182
    expected_total = 17.98 * 0.90
    # Compare to 2 decimals to match money
    assert round(order.total_amount, 2) == round(expected_total, 2), \
        f"Expected {expected_total:.2f}, got {order.total_amount:.2f}"


def test_checkout_redirects_when_empty(client):
    resp = client.get("/checkout", follow_redirects=True)
    assert resp.status_code == 200
    assert b"Your cart is empty!" in resp.data



def test_payment_failure_for_1111(client):
    seed_cart(client)
    resp = client.post("/process-checkout", data={
        "name": "Bob",
        "email": "bob@example.com",
        "address": "2 Road",
        "city": "Town",
        "zip_code": "12345",
        "payment_method": "credit_card",
        "card_number": "4111111111111111",
        "expiry_date": "12/30",
        "cvv": "123",
    }, follow_redirects=True)
    assert resp.status_code == 200
    assert b"Payment failed" in resp.data

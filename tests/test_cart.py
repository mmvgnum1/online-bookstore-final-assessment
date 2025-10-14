import app as app_module

def test_add_to_cart_valid(client):
    resp = client.post("/add-to-cart", data={"title": "1984", "quantity": "2"}, follow_redirects=True)
    assert resp.status_code == 200
    # Assert cart state instead of flash text
    assert app_module.cart.get_total_items() == 2
    # Optional: visit /cart to ensure 1984 appears somewhere
    resp = client.get("/cart")
    assert resp.status_code == 200
    assert b"1984" in resp.data

def test_add_to_cart_non_numeric_quantity_graceful(client):
    resp = client.post("/add-to-cart", data={"title": "1984", "quantity": "abc"}, follow_redirects=True)
    assert resp.status_code == 200
    # Non-numeric should default to 1 (as implemented in app.py)
    assert app_module.cart.get_total_items() == 1

def test_update_cart_zero_removes_item(client):
    client.post("/add-to-cart", data={"title": "1984", "quantity": "2"}, follow_redirects=True)
    resp = client.post("/update-cart", data={"title": "1984", "quantity": "0"}, follow_redirects=True)
    assert resp.status_code == 200
    # Item should be removed entirely
    assert app_module.cart.get_total_items() == 0
    # And page should render without the book
    resp = client.get("/cart")
    assert b"1984" not in resp.data

def test_remove_from_cart(client):
    client.post("/add-to-cart", data={"title": "1984", "quantity": "1"}, follow_redirects=True)
    resp = client.post("/remove-from-cart", data={"title": "1984"}, follow_redirects=True)
    assert resp.status_code == 200
    assert app_module.cart.get_total_items() == 0

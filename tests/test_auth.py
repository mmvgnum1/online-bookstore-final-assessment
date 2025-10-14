def test_register_requires_valid_email_format(client):
    resp = client.post("/register", data={
        "email": "not-an-email",
        "password": "pw",
        "name": "User",
        "address": "Somewhere"
    }, follow_redirects=True)
    assert resp.status_code == 200
    assert b"Invalid email format" in resp.data

def test_register_duplicate_email_case_insensitive(client):
    client.post("/register", data={
        "email": "Case@Test.com",
        "password": "pw",
        "name": "Case",
        "address": ""
    }, follow_redirects=True)
    resp = client.post("/register", data={
        "email": "case@test.com",
        "password": "pw",
        "name": "Case2",
        "address": ""
    }, follow_redirects=True)
    assert b"already exists" in resp.data

def test_login_success_and_logout(client):
    # Uses demo user created in app.py (now stored by lowercase key)
    resp = client.post("/login", data={"email": "demo@bookstore.com", "password": "demo123"}, follow_redirects=True)
    assert b"Logged in successfully!" in resp.data
    resp = client.get("/logout", follow_redirects=True)
    assert b"Logged out successfully!" in resp.data

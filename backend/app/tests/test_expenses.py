from datetime import date


def test_health_check(client):
    """Test the health check endpoint."""
    response = client.get("/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "healthy"
    assert "timestamp" in data


def test_create_expense(client):
    """Test creating a new expense."""
    expense_data = {
        "merchant": "Test Store",
        "amount": 25.50,
        "category": "groceries",
        "date": "2026-01-14",
        "notes": "Test purchase"
    }
    
    response = client.post("/api/expenses", json=expense_data)
    assert response.status_code == 201
    
    data = response.json()
    assert data["merchant"] == "Test Store"
    assert data["amount"] == 25.50
    assert data["category"] == "groceries"
    assert "id" in data


def test_list_expenses(client):
    """Test listing expenses."""
    # Create some test expenses
    expenses = [
        {"merchant": "Store A", "amount": 10.0, "category": "food", "date": "2026-01-10"},
        {"merchant": "Store B", "amount": 20.0, "category": "groceries", "date": "2026-01-11"},
        {"merchant": "Store C", "amount": 30.0, "category": "transport", "date": "2026-01-12"},
    ]
    
    for expense in expenses:
        client.post("/api/expenses", json=expense)
    
    # List all expenses
    response = client.get("/api/expenses")
    assert response.status_code == 200
    
    data = response.json()
    assert len(data) == 3


def test_filter_expenses_by_category(client):
    """Test filtering expenses by category."""
    # Create test expenses
    client.post("/api/expenses", json={
        "merchant": "Food Place", "amount": 15.0, "category": "food", "date": "2026-01-10"
    })
    client.post("/api/expenses", json={
        "merchant": "Grocery Store", "amount": 50.0, "category": "groceries", "date": "2026-01-11"
    })
    
    # Filter by food category
    response = client.get("/api/expenses?category=food")
    assert response.status_code == 200
    
    data = response.json()
    assert len(data) == 1
    assert data[0]["category"] == "food"


def test_get_expense(client):
    """Test getting a specific expense."""
    # Create an expense
    create_response = client.post("/api/expenses", json={
        "merchant": "Test", "amount": 100.0, "category": "other", "date": "2026-01-14"
    })
    expense_id = create_response.json()["id"]
    
    # Get the expense
    response = client.get(f"/api/expenses/{expense_id}")
    assert response.status_code == 200
    
    data = response.json()
    assert data["id"] == expense_id
    assert data["merchant"] == "Test"


def test_update_expense(client):
    """Test updating an expense."""
    # Create an expense
    create_response = client.post("/api/expenses", json={
        "merchant": "Old Name", "amount": 50.0, "category": "food", "date": "2026-01-14"
    })
    expense_id = create_response.json()["id"]
    
    # Update the expense
    update_data = {"merchant": "New Name", "amount": 75.0}
    response = client.put(f"/api/expenses/{expense_id}", json=update_data)
    assert response.status_code == 200
    
    data = response.json()
    assert data["merchant"] == "New Name"
    assert data["amount"] == 75.0


def test_delete_expense(client):
    """Test deleting an expense."""
    # Create an expense
    create_response = client.post("/api/expenses", json={
        "merchant": "To Delete", "amount": 10.0, "category": "other", "date": "2026-01-14"
    })
    expense_id = create_response.json()["id"]
    
    # Delete the expense
    response = client.delete(f"/api/expenses/{expense_id}")
    assert response.status_code == 204
    
    # Verify it's gone
    get_response = client.get(f"/api/expenses/{expense_id}")
    assert get_response.status_code == 404


def test_get_categories(client):
    """Test getting all categories."""
    response = client.get("/api/categories")
    assert response.status_code == 200
    
    data = response.json()
    assert len(data) > 0
    assert any(cat["id"] == "food" for cat in data)


def test_spending_summary(client):
    """Test getting spending summary."""
    # Create test expenses
    client.post("/api/expenses", json={
        "merchant": "Store A", "amount": 100.0, "category": "food", "date": "2026-01-10"
    })
    client.post("/api/expenses", json={
        "merchant": "Store B", "amount": 50.0, "category": "food", "date": "2026-01-11"
    })
    client.post("/api/expenses", json={
        "merchant": "Store C", "amount": 75.0, "category": "groceries", "date": "2026-01-12"
    })
    
    # Get summary
    response = client.get("/api/analytics/summary?start_date=2026-01-01&end_date=2026-01-31")
    assert response.status_code == 200
    
    data = response.json()
    assert data["total"] == 225.0
    assert len(data["by_category"]) == 2
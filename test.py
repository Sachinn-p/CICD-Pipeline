import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from main import app, Base, get_db, ItemDB

# Create a test database
SQLALCHEMY_DATABASE_URL = "sqlite:///./test_db.db"
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base.metadata.create_all(bind=engine)

def override_get_db():
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()

app.dependency_overrides[get_db] = override_get_db
client = TestClient(app)

@pytest.fixture(autouse=True)
def clear_db():
    """Clear database before each test"""
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    yield

class TestRoot:
    def test_read_root(self):
        response = client.get("/")
        assert response.status_code == 200
        assert response.json() == {"message": "Welcome to FastAPI!"}

class TestItems:
    def test_get_empty_items(self):
        """Test getting items when database is empty"""
        response = client.get("/items/")
        assert response.status_code == 200
        assert response.json() == []

    def test_create_item(self):
        """Test creating a new item"""
        item_data = {
            "name": "Laptop",
            "price": 999.99,
            "description": "A powerful laptop"
        }
        response = client.post("/items/", json=item_data)
        assert response.status_code == 200
        data = response.json()
        assert data["name"] == "Laptop"
        assert data["price"] == 999.99
        assert data["description"] == "A powerful laptop"
        assert "id" in data

    def test_create_item_without_description(self):
        """Test creating an item without description"""
        item_data = {
            "name": "Mouse",
            "price": 29.99
        }
        response = client.post("/items/", json=item_data)
        assert response.status_code == 200
        data = response.json()
        assert data["name"] == "Mouse"
        assert data["price"] == 29.99
        assert data["description"] is None

    def test_get_item_by_id(self):
        """Test getting a specific item by ID"""
        # Create an item first
        item_data = {"name": "Keyboard", "price": 79.99, "description": "Mechanical keyboard"}
        create_response = client.post("/items/", json=item_data)
        item_id = create_response.json()["id"]
        
        # Get the item
        response = client.get(f"/items/{item_id}")
        assert response.status_code == 200
        data = response.json()
        assert data["id"] == item_id
        assert data["name"] == "Keyboard"
        assert data["price"] == 79.99

    def test_get_nonexistent_item(self):
        """Test getting an item that doesn't exist"""
        response = client.get("/items/999")
        assert response.status_code == 404
        assert response.json() == {"detail": "Item not found"}

    def test_get_all_items(self):
        """Test getting all items"""
        # Create multiple items
        items = [
            {"name": "Item1", "price": 10.0},
            {"name": "Item2", "price": 20.0},
            {"name": "Item3", "price": 30.0}
        ]
        for item in items:
            client.post("/items/", json=item)
        
        # Get all items
        response = client.get("/items/")
        assert response.status_code == 200
        data = response.json()
        assert len(data) == 3
        assert data[0]["name"] == "Item1"
        assert data[1]["name"] == "Item2"
        assert data[2]["name"] == "Item3"

    def test_update_item(self):
        """Test updating an item"""
        # Create an item
        item_data = {"name": "Monitor", "price": 199.99, "description": "4K Monitor"}
        create_response = client.post("/items/", json=item_data)
        item_id = create_response.json()["id"]
        
        # Update the item
        updated_data = {"name": "Monitor 4K", "price": 249.99, "description": "Updated 4K Monitor"}
        response = client.put(f"/items/{item_id}", json=updated_data)
        assert response.status_code == 200
        data = response.json()
        assert data["id"] == item_id
        assert data["name"] == "Monitor 4K"
        assert data["price"] == 249.99
        assert data["description"] == "Updated 4K Monitor"

    def test_update_nonexistent_item(self):
        """Test updating an item that doesn't exist"""
        item_data = {"name": "Headphones", "price": 99.99}
        response = client.put("/items/999", json=item_data)
        assert response.status_code == 404
        assert response.json() == {"detail": "Item not found"}

    def test_delete_item(self):
        """Test deleting an item"""
        # Create an item
        item_data = {"name": "Speaker", "price": 149.99}
        create_response = client.post("/items/", json=item_data)
        item_id = create_response.json()["id"]
        
        # Delete the item
        response = client.delete(f"/items/{item_id}")
        assert response.status_code == 200
        assert response.json() == {"message": "Item deleted successfully"}
        
        # Verify it's deleted
        get_response = client.get(f"/items/{item_id}")
        assert get_response.status_code == 404

    def test_delete_nonexistent_item(self):
        """Test deleting an item that doesn't exist"""
        response = client.delete("/items/999")
        assert response.status_code == 404
        assert response.json() == {"detail": "Item not found"}

class TestHealth:
    def test_health_check(self):
        """Test health check endpoint"""
        response = client.get("/health")
        assert response.status_code == 200
        assert response.json() == {"status": "healthy"}

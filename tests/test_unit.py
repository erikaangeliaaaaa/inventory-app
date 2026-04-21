import pytest
from app import app, db
from services.inventory_service import InventoryService
from models.item import Item

@pytest.fixture
def setup_db():
    """Fixture untuk menyiapkan database sementara di memori."""
    app.config['TESTING'] = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
    with app.app_context():
        db.create_all()
        yield db
        db.session.remove()
        db.drop_all()

# --- UNIT TESTS (15 CASES) ---

# 1-3. Add Item Cases
def test_add_item_success(setup_db):
    item = InventoryService.add_item("Laptop", 10)
    assert item.id is not None
    assert item.nama == "Laptop"

def test_add_item_empty_name(setup_db):
    with pytest.raises(ValueError, match="Name cannot be empty"):
        InventoryService.add_item("", 10)

def test_add_item_negative_stock(setup_db):
    with pytest.raises(ValueError, match="Stock cannot be negative"):
        InventoryService.add_item("Barang A", -5)

# 4-6. Update Item Cases
def test_update_item_success(setup_db):
    item = InventoryService.add_item("Lama", 5)
    updated = InventoryService.update_item(item.id, "Baru", 15)
    assert updated.nama == "Baru"
    assert updated.jumlah == 15

def test_update_item_empty_name(setup_db):
    item = InventoryService.add_item("Test", 5)
    with pytest.raises(ValueError, match="Name cannot be empty"):
        InventoryService.update_item(item.id, "", 10)

def test_update_item_negative_stock(setup_db):
    item = InventoryService.add_item("Test", 5)
    with pytest.raises(ValueError, match="Stock cannot be negative"):
        InventoryService.update_item(item.id, "Test", -1)

# 7-9. Delete Item Cases
def test_delete_item_success(setup_db):
    item = InventoryService.add_item("Hapus", 1)
    result = InventoryService.delete_item(item.id)
    assert result is True

def test_delete_item_not_found(setup_db):
    result = InventoryService.delete_item(999)
    assert result is False

def test_delete_item_and_verify(setup_db):
    item = InventoryService.add_item("Verify", 1)
    InventoryService.delete_item(item.id)
    found = Item.query.get(item.id)
    assert found is None

# 10-12. Validation & Edge Cases
def test_add_item_whitespace_name(setup_db):
    with pytest.raises(ValueError, match="Name cannot be empty"):
        InventoryService.add_item("   ", 10)

def test_stock_as_string_digit(setup_db):
    # Flask form mengirim string, service harus bisa menangani/validasi
    item = InventoryService.add_item("String Stock", "25")
    assert item.jumlah == 25

def test_invalid_stock_type(setup_db):
    with pytest.raises(ValueError): # Sesuai dengan int() conversion error
        InventoryService.add_item("Barang", "abc")

# 13-15. Business Logic / Default Values
def test_stock_edge_case_zero(setup_db):
    item = InventoryService.add_item("Barang Nol", 0)
    assert item.jumlah == 0

def test_get_all_items_logic(setup_db):
    InventoryService.add_item("A", 1)
    InventoryService.add_item("B", 2)
    items = InventoryService.get_all_items()
    assert len(items) == 2

def test_get_item_by_id(setup_db):
    item = InventoryService.add_item("Cari", 1)
    found = InventoryService.get_item_by_id(item.id)
    assert found.nama == "Cari"
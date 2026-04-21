import pytest
from app import app, db
from models.item import Item

@pytest.fixture
def client():
    app.config['TESTING'] = True
    # Menggunakan SQLite memory agar testing tidak merusak database MySQL asli Anda
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
    with app.test_client() as client:
        with app.app_context():
            db.create_all()
            yield client

# --- INTEGRATION TESTS (5 CASES) ---

def test_index_route(client):
    """Test 1: Memastikan halaman utama bisa diakses dan tabel muncul"""
    response = client.get('/')
    assert response.status_code == 200
    assert b"Inventory Management" in response.data

def test_add_item_integration(client):
    """Test 2: Memastikan data yang di-post masuk ke database"""
    client.post('/add', data={'name': 'Buku', 'stock': '20'})
    item = Item.query.filter_by(nama='Buku').first()
    assert item is not None
    assert item.jumlah == 20

def test_delete_item_integration(client):
    """Test 3: Memastikan item benar-benar terhapus"""
    # Tambah dulu
    item = Item(nama="Hapus Aku", jumlah=1)
    db.session.add(item)
    db.session.commit()
    # Hapus
    client.get(f'/delete/{item.id}')
    deleted_item = Item.query.get(item.id)
    assert deleted_item is None

def test_edit_item_integration(client):
    """Test 4: Memastikan edit merubah data di DB"""
    item = Item(nama="Lama", jumlah=5)
    db.session.add(item)
    db.session.commit()
    client.post(f'/edit/{item.id}', data={'name': 'Baru', 'stock': '10'})
    updated_item = Item.query.get(item.id)
    assert updated_item.nama == "Baru"

def test_full_flow_integration(client):
    """Test 5: Alur lengkap Add -> Lihat -> Delete secara dinamis"""
    # 1. Tambah Barang
    client.post('/add', data={'name': 'FlowTest', 'stock': '100'})
    
    with app.app_context():
        item = Item.query.filter_by(nama='FlowTest').first()
        item_id = item.id

    # 2. Pastikan muncul di awal
    res = client.get('/')
    assert b"FlowTest" in res.data
    
    # 3. Hapus
    client.get(f'/delete/{item_id}')
    
    # --- TAMBAHKAN INI: Pastikan DB benar-benar bersih ---
    with app.app_context():
        db.session.expire_all() # Memaksa SQLAlchemy mengambil data fresh dari DB
    # ---------------------------------------------------

    # 4. Cek apakah sudah hilang
    res_after = client.get('/')
    assert b"FlowTest" not in res_after.data
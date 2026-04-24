from models.item import Item
from app import db

class InventoryService:
    @staticmethod
    def add_item(name, stock):
        # 1. Validasi Nama (Menangani spasi kosong)
        if not name or not name.strip():
            raise ValueError("Name cannot be empty")
        
        # 2. Konversi & Validasi Stok
        try:
            stock = int(stock)
        except (ValueError, TypeError):
            raise ValueError("Stock must be a number")
            
        if stock < 0:
            raise ValueError("Stock cannot be negative")
            
        item = Item(nama=name.strip(), jumlah=stock)
        db.session.add(item)
        db.session.commit()
        return item

    @staticmethod
    def update_item(item_id, name, stock):
        item = Item.query.get(item_id)
        if not item:
            raise ValueError("Item not found")
            
        if not name or not name.strip():
            raise ValueError("Name cannot be empty")
            
        try:
            stock = int(stock)
        except (ValueError, TypeError):
            raise ValueError("Stock must be a number")
            
        if stock < 0:
            raise ValueError("Stock cannot be negative")
            
        item.nama = name.strip()
        item.jumlah = stock
        db.session.commit()
        return item

    @staticmethod
    def delete_item(item_id):
        item = Item.query.get(item_id)
        if item:
            db.session.delete(item)
            db.session.commit()
            return True
        return False

    @staticmethod
    def get_all_items():
        return Item.query.all()

    # Tambahkan fungsi ini agar test_get_item_by_id tidak error
    @staticmethod
    def get_item_by_id(item_id):
        return Item.query.get(item_id)
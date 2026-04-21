from models.item import Item, db

class InventoryService:
    # Kita tidak butuh __init__ lagi karena data disimpan di Database
    
    @staticmethod
    def add_item(name, stock):
        if not name:
            raise ValueError("Name cannot be empty")
        if stock < 0:
            raise ValueError("Stock cannot be negative")

        item = Item(nama=name, jumlah=stock)
        db.session.add(item)
        db.session.commit()
        return item

    @staticmethod
    def get_all_items():
        # Tanpa 'self', langsung query ke database
        return Item.query.all()

    @staticmethod
    def delete_item(item_id):
        item = Item.query.get(item_id)
        if item:
            db.session.delete(item)
            db.session.commit()
            return True
        return False

    @staticmethod
    def update_item(item_id, name, stock):
        if not name:
            raise ValueError("Name cannot be empty")
        if stock < 0:
            raise ValueError("Stock cannot be negative")

        item = Item.query.get(item_id)
        if item:
            item.nama = name
            item.jumlah = stock
            db.session.commit()
            return item
        raise ValueError("Item not found")
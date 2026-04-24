from app import db

class Item(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nama = db.Column(db.String(100), nullable=False)
    jumlah = db.Column(db.Integer, nullable=False)

    def to_dict(self):
        return {"id": self.id, "nama": self.nama, "jumlah": self.jumlah, "deskripsi": self.deskripsi}
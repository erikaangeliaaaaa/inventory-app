from flask import Flask, render_template, request, redirect, url_for
from models.item import db, Item  # Tambahkan Item di sini
from services.inventory_service import InventoryService

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_STAY_TRACKING'] = False
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:@localhost/inventory_db'

db.init_app(app)

# Buat database saat aplikasi pertama kali dijalankan
with app.app_context():
    db.create_all()

@app.route('/')
def index():
    items = InventoryService.get_all_items()
    return render_template('index.html', items=items)

@app.route('/add', methods=['POST'])
def add():
    try:
        # Mengambil dari form HTML
        name_from_form = request.form['name'] 
        stock_from_form = int(request.form['stock'])
        
        # Kirim ke Service
        InventoryService.add_item(name_from_form, stock_from_form)
    except ValueError as e:
        return str(e), 400 
    return redirect(url_for('index'))

@app.route('/edit/<int:id>', methods=['GET', 'POST'])
def edit(id):
    if request.method == 'POST':
        try:
            name = request.form['name']
            stock = int(request.form['stock'])
            InventoryService.update_item(id, name, stock)
            return redirect(url_for('index'))
        except ValueError as e:
            return str(e), 400
            
    # Jika method GET, cari data item untuk ditampilkan di form edit
    item_to_edit = Item.query.get_or_404(id)
    return render_template('edit.html', item=item_to_edit)

@app.route('/delete/<int:id>')
def delete(id):
    InventoryService.delete_item(id)
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
from flask import Flask, render_template, request, redirect
import os
from extensions import db   # 🔥 ambil dari sini

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv(
    "DATABASE_URL",
    "sqlite:///local.db"
)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)   # 🔥 penting
# import setelah db dibuat
from models.item import Item
from services.inventory_service import InventoryService


@app.route('/')
def index():
    items = InventoryService.get_all_items()
    return render_template('index.html', items=items)


@app.route('/add', methods=['POST'])
def add_item():
    name = request.form.get('name')
    stock = request.form.get('stock')

    try:
        InventoryService.add_item(name, stock)
    except Exception as e:
        print(e)

    return redirect('/')


@app.route('/delete/<int:item_id>')
def delete_item(item_id):
    InventoryService.delete_item(item_id)
    return redirect('/')


@app.route('/edit/<int:item_id>', methods=['GET', 'POST'])
def edit_item(item_id):
    item = InventoryService.get_item_by_id(item_id)

    if not item:
        return "Item not found", 404

    if request.method == 'POST':
        name = request.form.get('name')
        stock = request.form.get('stock')

        try:
            InventoryService.update_item(item_id, name, stock)
        except Exception as e:
            print(e)

        return redirect('/')

    return render_template('edit.html', item=item)


if __name__ == '__main__':
    with app.app_context():
        db.create_all()  # 🔥 penting buat local run
    app.run(debug=True)
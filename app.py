from flask import Flask, request, jsonify
from db import db
from models import Store, Item

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///data.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db.init_app(app)


@app.route("/store", methods=["POST"])
def create_store():
    data = request.get_json()
    new_store = Store(name=data["name"])
    db.session.add(new_store)
    db.session.commit()
    return jsonify({"message": "Store created", "store": {"id": new_store.id, "name": new_store.name}}), 201


@app.route("/item", methods=["POST"])
def create_item():
    data = request.get_json()
    new_item = Item(name=data["name"], price=data["price"], store_id=data["store_id"])
    db.session.add(new_item)
    db.session.commit()
    return jsonify({"message": "Item created", "item": {
        "id": new_item.id,
        "name": new_item.name,
        "price": new_item.price,
        "store_id": new_item.store_id
    }}), 201


@app.route("/stores", methods=["GET"])
def get_stores():
    stores = Store.query.all()
    return jsonify([{"id": store.id, "name": store.name} for store in stores])


@app.route("/items", methods=["GET"])
def get_items():
    items = Item.query.all()
    return jsonify([{
        "id": item.id,
        "name": item.name,
        "price": item.price,
        "store_id": item.store_id
    } for item in items])


if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True)

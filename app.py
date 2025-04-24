from flask import Flask, request
from db import db
from models import StoreModel, ItemModel

def create_app():
    app = Flask(__name__)
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///data.db"
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    db.init_app(app)

    @app.route("/")
    def home():
        return "Hello from SQLAlchemy!"

    @app.route("/store/<string:name>", methods=["POST"])
    def create_store(name):
        if StoreModel.query.filter_by(name=name).first():
            return {"message": "Store already exists."}, 400

        new_store = StoreModel(name=name)
        db.session.add(new_store)
        db.session.commit()
        return {"message": f"Store '{name}' created successfully."}, 201

    @app.route("/stores", methods=["GET"])
    def get_stores():
        stores = StoreModel.query.all()
        return {
            "stores": [
                {"id": store.id, "name": store.name}
                for store in stores
            ]
        }

    @app.route("/item", methods=["POST"])
    def create_item():
        data = request.get_json()
        name = data.get("name")
        price = data.get("price")
        store_id = data.get("store_id")

        if not all([name, price, store_id]):
            return {"message": "Missing data (name, price, store_id required)."}, 400

        item = ItemModel(name=name, price=price, store_id=store_id)
        db.session.add(item)
        db.session.commit()
        return {"message": f"Item '{name}' created successfully."}, 201

    @app.route("/items", methods=["GET"])
    def get_items():
        items = ItemModel.query.all()
        return {
            "items": [
                {
                    "id": item.id,
                    "name": item.name,
                    "price": item.price,
                    "store_id": item.store_id
                }
                for item in items
            ]
        }

    @app.route("/store/<int:store_id>/items", methods=["GET"])
    def get_store_items(store_id):
        store = StoreModel.query.get(store_id)
        if not store:
            return {"message": "Store not found."}, 404

        return {
            "store": store.name,
            "items": [
                {"id": item.id, "name": item.name, "price": item.price}
                for item in store.items
            ]
        }

    with app.app_context():
        db.create_all()

    return app

if __name__ == "__main__":
    app = create_app()
    app.run(debug=True)

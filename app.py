from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager, create_access_token, jwt_required
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///data.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["JWT_SECRET_KEY"] = "super-secret"  # заміни на щось безпечніше у продакшн

db = SQLAlchemy(app)
jwt = JWTManager(app)

# ======= МОДЕЛІ ========
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)

class Item(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80))
    price = db.Column(db.Float)
    store_id = db.Column(db.Integer, nullable=False)

# ======= ЕНДПОІНТИ ========

@app.post('/register')
def register():
    data = request.get_json()
    if User.query.filter_by(username=data["username"]).first():
        return {"message": "User already exists"}, 400
    hashed_pw = generate_password_hash(data["password"])
    new_user = User(username=data["username"], password=hashed_pw)
    db.session.add(new_user)
    db.session.commit()
    return {"message": "User created"}, 201

@app.post('/login')
def login():
    data = request.get_json()
    user = User.query.filter_by(username=data["username"]).first()
    if user and check_password_hash(user.password, data["password"]):
        access_token = create_access_token(identity=user.id)
        return {"access_token": access_token}
    return {"message": "Invalid credentials"}, 401

@app.get('/items')
@jwt_required()
def get_items():
    items = Item.query.all()
    return jsonify([{"id": i.id, "name": i.name, "price": i.price} for i in items])

# ======= СТАРТ СЕРВЕРА ========
if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)

from myproject import db, login_manager
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(64), unique=True, index=True)
    password_hash = db.Column(db.String(128))
    admin = db.Column(db.Boolean)
    inventory_items = db.relationship('Inventory', backref='user', lazy=True)

    def __init__(self, email, password):
        self.email = email
        self.password_hash = generate_password_hash(password)
        if email == 'razaashai@gmail.com':
            self.admin = True
        else:
            self.admin = False

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)


class Brand(db.Model):
    __tablename__ = 'brand'
    id = db.Column(db.Integer, primary_key=True)
    manufacturer = db.Column(db.String(40), unique=True, nullable=False)
    country = db.Column(db.String(40), unique=False, nullable=False)
    models = db.relationship('ModelCar', backref='brand', lazy=True)

    def __init__(self, manufacturer, country):
        self.manufacturer = manufacturer
        self.country = country

    def __repr__(self):
        return f'manufacturer: {self.manufacturer}, country of origin: {self.country}'


class ModelCar(db.Model):
    __tablename__ = 'modelcar'
    id = db.Column(db.Integer, primary_key=True)
    brand_id = db.Column(db.Integer, db.ForeignKey('brand.id'))
    name = db.Column(db.String(40), nullable=False)
    trims = db.relationship('Trim', backref='modelcar', lazy=True)

    def __init__(self, name, brand_id):
        self.name = name
        self.brand_id = brand_id

    def __repr__(self):
        return f"Model name: {self.name}, brand id: {self.brand_id}"


class Trim(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    model_id = db.Column(db.Integer, db.ForeignKey('modelcar.id'))
    name = db.Column(db.String(40), nullable=False)

    def __init__(self, name, model_id):
        self.name = name
        self.model_id = model_id

    def __repr__(self):
        return f"Trim name: {self.name}, model_id: {self.model_id}"


class Inventory(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    trim_id = db.Column(db.Integer, db.ForeignKey('trim.id'))
    listed_data = db.Column(db.String(255), nullable=True)
    ask_price = db.Column(db.Integer, nullable=False)
    # will be based on numerical system corresponding to textual condition in JS
    condition = db.Column(db.Integer, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    def __init__(self, trim_id, listed_data, ask_price, condition, user_id):
        self.trim_id = trim_id
        self.listed_data = listed_data
        self.ask_price = ask_price
        self.condition = condition
        self.user_id = user_id

    def __repr__(self):
        return f"Listing id {self.id}; asking price: {self.ask_price}"

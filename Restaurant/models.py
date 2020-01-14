from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin

db = SQLAlchemy()


class User(UserMixin, db.Model):
    """User model"""

    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(25), unique=True, nullable=False)
    password = db.Column(db.String(), nullable=False)

# Restaurant table


class Restaurant(UserMixin, db.Model):
    __tablename__ = 'restaurants'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)

    def __init__(self, id, name):
        self.id = id
        self.name = name

    def __repr__(self):
        return 'The id is {}, Name is is {}'.format(self.id, self.name)

# menus table


class Menu(UserMixin, db.Model):
    __tablename__ = 'menus'

    id = db.Column(db.Integer, primary_key=True)
    menu_name = db.Column(db.String(500), nullable=False)
    address = db.Column(db.String(100))
    phone = db.Column(db.String(100))
    price = db.Column(db.Float)
    picture = db.Column(db.String(100))

    # ESTABLISH A RELATIONSHIP BETWEEN restaurants AND menus TABLES
    res_id = db.Column(db.Integer, db.ForeignKey('restaurants.id'))

    def __init__(self, menu_name, address, phone, price, picture, res_id):

        self.menu_name = menu_name
        self.address = address
        self.phone = phone
        self.price = price
        self.picture = picture
        self.res_id = res_id

    def __repr__(self):
        return "Menu: {}; Phone: {}; Price: $ {}".format(self.menu_name, self.phone, self.price)

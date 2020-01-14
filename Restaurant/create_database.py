from flask import Flask, render_template, redirect, url_for, flash
from passlib.hash import pbkdf2_sha256
from wtform_fields import *
from models import *
from flask_login import LoginManager, login_user, current_user, login_required, logout_user
#-------------------------------#
from flask import Flask, render_template, redirect, request, url_for, flash
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

# Configure database
app.config.update(

    SECRET_KEY='whatever',
    SQLALCHEMY_DATABASE_URI='postgresql://localhost/RestaurantMenusDB',
    SQLALCHEMY_TRACK_MODIFICATIONS=False
)

db = SQLAlchemy(app)


class User(db.Model):
    """User model"""

    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(25), unique=True, nullable=False)
    password = db.Column(db.String(), nullable=False)


# Restaurant table


class Restaurant(db.Model):
    __tablename__ = 'restaurants'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)

    def __init__(self, id, name):
        self.id = id
        self.name = name

    def __repr__(self):
        return 'The id is {}, Name is is {}'.format(self.id, self.name)

# menus table


class Menu(db.Model):
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


# ---------------------------------------------
# User Authentication: Configure flask login
login = LoginManager(app)
login.init_app(app)


@login.user_loader
def load_user(id):
    return User.query.get(int(id))

# The "index()" method is the "Registration" method. So I could also name it "registration()".
@app.route("/", methods=['GET', 'POST'])
def index():
    reg_form = RegistrationForm()
    # Collect the "username" and "password" from the "RegistrationForm".
    # Update database if validation success.
    if reg_form.validate_on_submit():
        username = reg_form.username.data
        password = reg_form.password.data
        # Hash password
        hashed_pswd = pbkdf2_sha256.hash(password)

        # Check if the "username" exist using "Flask SQLAlchemy"
        # NOTE: The query below returns only one row(list) containing the "id", "username", & "password"
        # user_object = User.query.filter_by(username=username).first()

        # The if statement says that "user_object" already exist in the database table.
        # if user_object:
        #    return "Someone else has taken this username!"

        # Add the user to the database if "user_object" does not exist in the database table.
        # Also add the hashed password to the database.
        user = User(username=username, password=hashed_pswd)
        db.session.add(user)
        db.session.commit()

        flash('Registered successfully. Please login.', 'success')

        return redirect(url_for('login'))

    return render_template('index.html', form=reg_form)


@app.route("/login", methods=['GET', 'POST'])
def login():

    login_form = LoginForm()

    # Allow login if validation is successful
    if login_form.validate_on_submit():
        # "user_object" contains a one row list of "username" & "password". "login_user()" function logs in the user.
        user_object = User.query.filter_by(username=login_form.username.data).first()
        # user_object = User.query.filter_by(username=login_form.username.data).first()
        login_user(user_object)
        # if current_user.is_authenticated:
        # return "Logged in, finally!"
        # return redirect(url_for('chat')) #
        return redirect(url_for('display_menus'))
        # return "Not logged in"
    return render_template("login.html", form=login_form)
#-------------------------------------------------------------------------#
# The "chat" page cannot be viewed unless the "user" logs in.
# @app.route("/chat", methods=['GET', 'POST'])
# def chat():
    # if not current_user.is_authenticated:
    #     flash('Please login.', 'danger')
    #     return redirect(url_for('login'))
    # return "Chat with me"
    # return render_template("chat.html", username=current_user.username.username, rooms=ROOMS)

#-------------------------------------------------------------------------#
# "log out" the user
@app.route("/logout", methods=['GET'])
def logout():
    logout_user()
    flash('You have logged out successfully', 'success')
    return "You are now logged out"
    # return redirect(url_for('login'))


# display all the menus
@app.route('/display_menus', methods=['GET', 'POST'])
# @app.route('/display_menus')
def display_menus():
    menuses = menus.query.all()
    # return 'home'
    return render_template('home.html', menus=menuses)

# @app.route('/display/restaurant/<restaurant_id>')
# def display_restaurant(restaurant_id):
#    restaurant = Restaurant.query.filter_by(id=restaurant_id).first()
#    restaurant_menus = Menu.query.filter_by(res_id=restaurant.id).all()
#    return render_template('restaurant.html', restaurant=restaurant, restaurant_menus=restaurant_menus)


# ---------------------------------------------
if __name__ == '__main__':
    # db.create_all()
    app.run(debug=True)

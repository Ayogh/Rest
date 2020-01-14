from flask_wtf import FlaskForm
from flask_login import current_user
from flask_wtf.file import FileField, FileAllowed
from wtforms import StringField, PasswordField, SubmitField, IntegerField, FloatField
from wtforms.validators import DataRequired, InputRequired, Length, EqualTo, ValidationError
from models import User
from passlib.hash import pbkdf2_sha256
#-------------------------------------------#


# Below we have the custom validation function called "invalid_credentials" which
# is used to make sure the "username & password" entered by the "user" are found
# in the database table.


def invalid_credentials(form, field):
    """ Username and password checker """

    # Get the "username" and "password" from the "form"
    # entered by the user; form extracts username while
    # field extracts the password.
    username_entered = form.username.data  # username_entered = username the user enters
    password_entered = field.data  # password_entered = password the user enters

    # Check if the username is invalid
    user_object = User.query.filter_by(username=username_entered).first()
    # if user_object is None: means the "username & password" entered are not found in the database table.
    if user_object is None:
        raise ValidationError("Username or password is incorrect")
    elif not pbkdf2_sha256.verify(password_entered, user_object.password):
        raise ValidationError("Username or password is incorrect")
    # elif password_entered != user_object.password:
    #    raise ValidationError("Username or password is incorrect")

    # Check password in invalid
    # elif not pbkdf2_sha256.verify(password_entered, user_object.hashed_pswd):
    #    raise ValidationError("Username or password is incorrect")


class RegistrationForm(FlaskForm):
    """ Registration form"""

    username = StringField('username', validators=[InputRequired(message="Username required"),
                                                   Length(min=4, max=25, message="Username must be between 4 and 25 characters")])
    password = PasswordField('password', validators=[InputRequired(message="Password required"),
                                                     Length(min=4, max=25, message="Password must be between 4 and 25 characters")])
    confirm_pswd = PasswordField('confirm_pswd', validators=[InputRequired(
        message="Password required"), EqualTo('password', message="Passwords must match")])
    submit_button = SubmitField('Create')

    # The "validate_username" makes it possible to check if "user_object = username & password" exist in
    # the database table without using "Flask SQLAlchemy" in application.py.
    def validate_username(self, username):
        user_object = User.query.filter_by(username=username.data).first()
        # "if user_object": means if "username & password" are found in database table, raise a "ValidationError"
        # because the "user" must choose Register with unique "username & password"
        if user_object:
            raise ValidationError("Username already exists. Select a different username.")


class LoginForm(FlaskForm):
    """ Login form """

    username = StringField('username', validators=[InputRequired(message="Username required")])
    # "invalid_credentials method" will be used for custom validation.
    password = PasswordField('password', validators=[InputRequired(message="Password required"), invalid_credentials])
    submit_button = SubmitField('Login')


class CreateMenuForm(FlaskForm):
    menu_name = StringField('Menu_Name', validators=[DataRequired()])
    address = StringField('Address', validators=[DataRequired()])
    phone = FloatField('Phone', validators=[DataRequired()])
    price = FloatField('Price', validators=[DataRequired()])
    picture_url = StringField('Picture', validators=[DataRequired()])
    res_id = IntegerField('MenuID', validators=[DataRequired()])
    submit = SubmitField('Create')


# class CreateMenuForm(FlaskForm):
#    menu_name = StringField('Menu_Name', validators=[DataRequired()])
#    address = StringField('Address', validators=[DataRequired()])
#    phone = FloatField('Phone', validators=[DataRequired()])
#    price = FloatField('Price', validators=[DataRequired()])
#    picture_url = StringField('Picture', validators=[DataRequired()])
#    res_id = IntegerField('MenuID', validators=[DataRequired()])
#    submit = SubmitField('Create')


class EditMenuForm(FlaskForm):
    menu_name = StringField('Menu_Name', validators=[DataRequired()])
    address = StringField('Address', validators=[DataRequired()])
    phone = StringField('Phone', validators=[DataRequired()])
    price = FloatField('Price', validators=[DataRequired()])
    submit = SubmitField('Update')

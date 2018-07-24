from wtforms import StringField, SelectField, validators, SubmitField, IntegerField, PasswordField, ValidationError
from flask_wtf import FlaskForm
from myproject.models import User

# We'll add users later
# class AddUser(FlaskForm):
#     username = StringField('Username', [validators.DataRequired(), validators.Length(min=4, max=16)])
#     email = StringField('Email', [validators.DataRequired(), validators.Length(min=4, max=25)])
#     password = PasswordField('Password', [validators.DataRequired(), validators.Length(min=4, max=25)])
#     admin = BooleanField('Admin?', [validators.DataRequired()])
#
class LoginForm(FlaskForm):
    email = StringField('Email', [validators.InputRequired(), validators.Email()])
    password = PasswordField('Password', [validators.InputRequired()])
    submit = SubmitField('Log in!')

class RegistrationForm(FlaskForm):
    email = StringField('Email', [validators.InputRequired(), validators.Email()])
    password = PasswordField('Password', [validators.InputRequired(),
                                          validators.EqualTo('pass_confirm', message='Passwords must match')])
    pass_confirm = PasswordField('Confirm your password', [validators.InputRequired()])
    submit = SubmitField('Register!')

    def check_email(self):
        if User.query.filter_by(email=self.email.data).first():
            return False;


class SelectionForm(FlaskForm):
    manufacturer_selection = SelectField("Select your manufacturer", coerce=int)
    model_selection = SelectField("Select your desired model", coerce=int)
    trim_selection = SelectField("Select your desired trim", coerce=int)
    submit = SubmitField("Search database")


class AddVehicleListingForm(FlaskForm):
    manufacturer = SelectField("Select a manufacturer", [validators.InputRequired()], coerce=int)
    model = SelectField("Select a model: ", [validators.InputRequired()], coerce=int)
    trim = SelectField("Select a trim: ", [validators.InputRequired()], coerce=int)
    listed_data = StringField('Enter some information about the listing', [validators.InputRequired()])
    ask_price = IntegerField("Enter the asking price of the vehicle", [validators.InputRequired()])
    condition = SelectField("Select the condition of the vehicle", [validators.InputRequired()], coerce=int)
    submit = SubmitField("Add Listing!")


class AddManufacturerForm(FlaskForm):
    manufacturer = StringField("Enter the name of the manufacturer")
    country = StringField('Enter the country of origin of this manufacturer')
    submit = SubmitField("Add manufacturer option")


class AddModelForm(FlaskForm):
    manufacturer = SelectField("Select the manufacturer to which you would like to add a make:", coerce=int)
    model = StringField("Enter the model of the vehicle")
    submit = SubmitField("Add this model as an option")


class AddTrimForm(FlaskForm):
    manufacturer = SelectField("Select the manufacturer of the model of the trim you'd like to add",
                               [validators.InputRequired()], coerce=int)
    model = SelectField("Select the model with the trim you would like to add", [validators.InputRequired()],
                        coerce=int)
    trim = StringField("What is the trim you would like to add", [validators.InputRequired()])
    submit = SubmitField("Add this trim as an option")


class RemoveInventoryListing(FlaskForm):
    id = IntegerField('Inventory id of listing to be removed', [validators.DataRequired()])
    submit = SubmitField("Submit")

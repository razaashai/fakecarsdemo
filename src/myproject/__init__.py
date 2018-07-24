from flask import Flask, flash, redirect
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager

# Application setup
login_manager = LoginManager()
app = Flask(__name__)
app.config['SECRET_KEY'] = 'mykey'
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:LL&AAiR#n1v#eRZsGVIS0#uZB@localhost/fakecars'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)







Migrate(app, db)

login_manager.init_app(app)
login_manager.login_view = 'login'
@login_manager.unauthorized_handler
def unauthorized_login():
    flash('Please log in before trying to access this page')
    return redirect('/login')

# Possible bug discovered in Flask: Using validate on submit method to check for a valid string
# causes a form error because any dynamically created options on the form are considered invalid input
# as such, you must simply check if the form is posting or not

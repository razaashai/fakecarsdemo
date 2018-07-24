from flask import render_template, jsonify, redirect, flash, url_for, request
from flask_login import login_user, login_required, logout_user, current_user
from myproject import app, db
from myproject.forms import (AddManufacturerForm, AddModelForm, AddTrimForm, AddVehicleListingForm,
                             RemoveInventoryListing, SelectionForm, RegistrationForm, LoginForm)
from myproject.models import Brand, ModelCar, Trim, Inventory, User


# JSON REST Apis

# END OF REST APIS

# Helper functions


# User authentication functions
def not_admin():
    flash("You are not an admin")
    return redirect(url_for('index'))



@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()

        if user.check_password(form.password.data) and user is not None:
            login_user(user, remember=True)
            flash("Logged in successfully!")

            next = request.args.get('next')
            if next is None or not next[0] == '/':
                next = url_for('index')
            return redirect(next)
    return render_template('login.html', form=form, current_user=current_user)


@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()

    if form.validate_on_submit():
        if not form.check_email():
            flash(f"{form.email.data} already exists!")
            return redirect(url_for('register'))
        else:
            user = User(email=form.email.data, password=form.password.data)
            db.session.add(user)
            db.session.commit()

            flash("Thanks for registering")
            return redirect(url_for('login'))

    return render_template('register.html',form=form, current_user=current_user)


@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash("You successfully logged out!")
    return redirect(url_for('index'))


@app.route('/', methods=['GET', 'POST'])
def index():
    # create form objects
    form = SelectionForm()
    form.manufacturer_selection.choices = [(item.id, item.manufacturer) for item in Brand.query.all()]
    form.model_selection.choices = [(item.id, item.name) for item in ModelCar.query.filter_by(brand_id=1)]
    form.trim_selection.choices = [(item.id, item.name) for item in
                                   Trim.query.filter_by(model_id=form.model_selection.choices[0][0])]
    if request.method == "POST":
        form.model_selection.choices = [(item.id, item.name) for item in
                                        ModelCar.query.filter_by(brand_id=form.manufacturer_selection.data)]
        form.trim_selection.choices = [(item.id, item.name) for item in
                                       Trim.query.filter_by(model_id=form.model_selection.data)]
        if form.validate():
            print("Reached validate")
            return results(form.trim_selection.data)
    return render_template('index.html', select_form=form, current_user=current_user)


# routes for dynamic selection, ideal API
@app.route('/models/<manufacturer_id>')
def models(manufacturer_id):
    models_data = ModelCar.query.filter_by(brand_id=manufacturer_id).all()
    models_arr = []
    for model in models_data:
        models_obj = dict()
        models_obj['id'] = model.id
        models_obj['name'] = model.name
        models_arr.append(models_obj)
    return jsonify({'models': models_arr})


# Passes trims via JSON format for the selection form
@app.route('/trims/<model_id>')
def trims(model_id):
    trims_info = Trim.query.filter_by(model_id=model_id).all()
    trims_arr = []
    for trim in trims_info:
        trims_obj = dict()
        trims_obj['id'] = trim.id
        trims_obj['name'] = trim.name
        trims_arr.append(trims_obj)
    return jsonify({"trims": trims_arr})


# routes for dynamic selection ends
@app.route('/admin')
@login_required
def admin():
    # use this to create models, trims, etc
    if not current_user.admin:
        return not_admin()
    return render_template('admin.html', current_user=current_user)


# Get the condition in the string format
def condition_getter(condition_value):
    options = ['Poor', 'Good', 'Very Good', 'Excellent']
    return options[condition_value]


# Fill results
@app.route('/results/<trim_id>')
def results(trim_id):
    trim_info = Trim.query.with_entities(Trim.name, Trim.model_id).filter_by(id=trim_id).all()
    trim_name = trim_info[0][0]
    model_info = ModelCar.query.with_entities(ModelCar.name, ModelCar.brand_id).filter_by(id=trim_info[0][1]).all()
    model_name = model_info[0][0]
    manufacturer_name = Brand.query.with_entities(Brand.manufacturer).filter_by(id=model_info[0][1]).all()[0][0]
    available_inventory = Inventory.query.filter_by(trim_id=trim_id).all()
    # inventory id --> Listed data --> Asking price --> Condition
    inventory_list = []
    for item in available_inventory:
        # had to subract 1 from item condition because values of select are indexed at one, not at zero
        item_obj = (item.id, item.listed_data, item.ask_price, condition_getter(item.condition - 1))
        inventory_list.append(item_obj)
    return render_template('results.html', acceptable_inventory=inventory_list,
                           manufacturer_name=manufacturer_name, model_name=model_name, trim_name=trim_name,
                           current_user=current_user)


@app.route('/add_listing', methods=['GET', 'POST'])
@login_required
def add_listing():
    # create use this to add listings from existing models, trims, etc
    form = AddVehicleListingForm()
    form.condition.choices = [(1, "Poor"), (2, "Good"), (3, "Very good"), (4, "Excellent")]
    form.manufacturer.choices = [(item.id, item.manufacturer) for item in Brand.query.all()]
    form.model.choices = [(item.id, item.name) for item in ModelCar.query.filter_by(brand_id=1)]
    form.trim.choices = [(item.id, item.name) for item in Trim.query.filter_by(model_id=form.model.choices[0][0])]
    print("Entered add_listing function")
    if request.method == "POST":
        print("Entered Post function")
        form.model.choices = [(item.id, item.name) for item in
                              ModelCar.query.filter_by(brand_id=form.manufacturer.data)]
        form.trim.choices = [(item.id, item.name) for item in
                             Trim.query.filter_by(model_id=form.model.data)]

        if form.validate():
            print("Entered validation")
            selected_trim = form.trim.data
            listed_data = form.listed_data.data
            ask_price = form.ask_price.data
            condition = form.condition.data
            listing = Inventory(selected_trim, listed_data, ask_price, condition, current_user.id)

            db.session.add(listing)
            db.session.commit()
            flash(f"You successfully added inventory with the following information:\nTrim ID: {form.trim.data}\n" +
                  f"Listed data: {form.listed_data.data}\nAsking price: {form.ask_price.data}\n " +
                  f"Condition: {form.condition.data}")
        else:
            flash("Invalid submission. Please check your listing details and try again")

        redirect(url_for('add_listing'))
    return render_template('add_inventory.html', add_listing=form, current_user=current_user)


@app.route('/add_manufacturer', methods=['GET', 'POST'])
@login_required
def add_manufacturer():
    if not current_user.admin:
        return not_admin()
    form = AddManufacturerForm()
    if form.validate_on_submit():
        manufacturer = Brand(form.manufacturer.data, form.country.data)
        db.session.add(manufacturer)
        db.session.commit()
        flash(f"You successfully added a manufacturer {form.manufacturer.data} from {form.country.data}")
        return redirect(url_for('add_manufacturer'))
    return render_template('add_manufacturer.html', add_manufacturer_form=form, current_user=current_user)


# Adds model to the database
@app.route('/add_model', methods=['GET', 'POST'])
@login_required
def add_model():
    if not current_user.admin:
        return not_admin()
    form = AddModelForm()
    form.manufacturer.choices = [(item.id, item.manufacturer) for item in Brand.query.all()]
    if form.validate_on_submit():
        # brand id refers to the manufacturer
        brand_id = form.manufacturer.data
        model_data = form.model.data
        new_make = ModelCar(model_data, brand_id)
        db.session.add(new_make)
        db.session.commit()
        flash(f"You successfully added the model named {model_data}")
        redirect(url_for('add_model'))
    return render_template('add_model.html', add_model_form=form, current_user=current_user)


@app.route('/add_trim', methods=['GET', 'POST'])
@login_required
def add_trim():
    if not current_user.admin:
        return not_admin()
    form = AddTrimForm()
    form.manufacturer.choices = [(item.id, item.manufacturer) for item in Brand.query.all()]
    form.model.choices = [(item.id, item.name) for item in ModelCar.query.filter_by(brand_id=1)]
    print(form.manufacturer.data)
    if request.method == "POST":
        print("Hello1")
        form.model.choices = [(item.id, item.name) for item in ModelCar.query.filter_by(
            brand_id=form.manufacturer.data)]
        if form.validate():
            model_id = form.model.data
            trim_data = form.trim.data
            new_trim = Trim(trim_data, model_id)
            db.session.add(new_trim)
            db.session.commit()
            flash(f"You successfully added the following trim: {trim_data}")
            redirect(url_for('add_trim'))
        else:
            flash("Invalid choice")
            redirect(url_for('add_trim'))

    return render_template('add_trim.html', add_trim_form=form, current_user=current_user)


# removes the listing from the database
@app.route("/remove_listing", methods=['GET', 'POST'])
@login_required
def remove_listing():
    if not current_user.admin:
        return not_admin()

    form = RemoveInventoryListing()
    if form.validate_on_submit():
        to_remove = Inventory.query.get(form.id.data)
        db.session.delete(to_remove)
        db.session.commit()
        flash("You successfully removed the listing")
        redirect(url_for('remove_listing'))
    if request.method == "POST" and not form.validate():
        flash("You failed to remove the listing")
        redirect(url_for('remove_listing'))
    return render_template('remove_listing.html', remove_listing_form=form, current_user=current_user)


if __name__ == '__main__':
    app.run()

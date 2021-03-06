from flask import render_template,request,redirect,session,flash
from flask_app import app
from flask_bcrypt import Bcrypt
bcrypt = Bcrypt(app)

from flask_app.models.user import User
from flask_app.models.car import Car

@app.route('/')
def login_reg_page():
    return render_template('index.html')

@app.route('/logout')
def logout():
    session.clear()
    return redirect('/')

@app.route('/register/user', methods=['POST'])
def register():
    if not User.validate_user(request.form):
        return redirect('/')
    # create the hash
    pw_hash = bcrypt.generate_password_hash(request.form['password'])
    print(pw_hash)

    data = {
        "first_name": request.form['first_name'],
        "last_name": request.form['last_name'],
        "email": request.form['email'],
        "password" : pw_hash
    }

    user_id = User.add_user(data)
    # store user id into session
    session['user_id'] = user_id
    session['first_name'] = request.form['first_name']
    first_name = request.form['first_name']
    last_name = request.form['last_name']
    session['name'] = f'{first_name} {last_name}'
    print(session['name'])
    return redirect("/dashboard")

@app.route('/login', methods=['POST'])
def login():

    data = { "email" : request.form["email"] }
    user_in_db = User.get_by_email(data)

    if not user_in_db:
        flash("Invalid Email/Password")
        return redirect("/")
    if not bcrypt.check_password_hash(user_in_db.password, request.form['password']):

        flash("Invalid Email/Password")
        return redirect('/')

    session['user_id'] = user_in_db.id
    session['first_name'] = user_in_db.first_name
    first_name = user_in_db.first_name
    last_name = user_in_db.last_name
    session["name"] = f'{first_name} {last_name}'

    return redirect("/dashboard")

@app.route('/purchase/<int:car_id>')
def like_show(car_id):
    data = {
        'user_id': session['user_id'],
        'car_id': car_id
    }
    User.buy_car(data)
    data1={
        'id':car_id,
        'sold': 1
    }
    Car.car_purchase(data1)
    return redirect("/dashboard")

@app.route('/view_purchases')
def view_purchases():
    data = {
        'id':session['user_id']
    }
    cars_purchased = User.get_purchases(data)
    return render_template('user_purchase.html',my_cars = cars_purchased)

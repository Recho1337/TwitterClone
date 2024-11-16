from flask_login import current_user
from flask import render_template, redirect, url_for, flash, request
from . import db
from .models import User
from flask_login import login_user, login_required, logout_user

from flask import Blueprint

main = Blueprint('main', __name__)

# Home Route (login page or welcome page)
@main.route('/')
def home():
    return render_template('home.html')

# Register Route
@main.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form.get('username')
        email = request.form.get('email')
        password = request.form.get('password')
        password_confirm = request.form.get('confirm_password')

        if password != password_confirm:
            flash('Passwords do not match!', 'danger')
            return redirect(url_for('main.register'))

        existing_user = User.query.filter((User.username == username) | (User.email == email)).first()
        if existing_user:
            flash('Username or email already exists!', 'danger')
            return redirect(url_for('main.register'))

        new_user = User(username=username, email=email)
        new_user.set_password(password)

        db.session.add(new_user)
        db.session.commit()

        flash('Registration successful! You can now log in.', 'success')
        return redirect(url_for('main.login'))  # Redirect to login page (or home page)

    return render_template('register.html')

# Login Route
@main.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        user = User.query.filter_by(email=email).first()
        if user and user.check_password(password):
            login_user(user)
            flash('Login successful!', 'success')

            return redirect(url_for('main.dashboard'))

        else:
            flash('Login failed. Check your email and/or password.', 'danger')

    return render_template('login.html')

# Dashboard Route (next page after login)
@main.route('/dashboard')
@login_required
def dashboard():
    return render_template('dashboard.html', name=current_user.username)

# Logout Route
@main.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You have been logged out.', 'info')
    return redirect(url_for('main.home'))

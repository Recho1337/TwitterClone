from flask_login import current_user
from flask import render_template, redirect, url_for, flash, request, jsonify
from . import db
from .models import User, followers, Post
from .forms import PostForm
from flask_login import login_user, login_required, logout_user
from werkzeug.utils import secure_filename
from flask import Blueprint
import os
from flask import current_app

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

# Logout Route
@main.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You have been logged out.', 'info')
    return redirect(url_for('main.home'))

@main.route('/details', methods=['GET', 'POST'])
@login_required
def details():
    if request.method == 'GET':
        return render_template('details.html')

@main.route('/update_details', methods=['POST'])
@login_required
def update_details():
    # Get the data from the form
    username = request.form.get('username')
    email = request.form.get('email')
    bio = request.form.get('bio')

    # Update the current user's details
    current_user.username = username
    current_user.email = email
    current_user.bio = bio

    # Commit the changes to the database
    db.session.commit()

    # Flash a success message
    flash('Your details have been updated!', 'success')

    # Redirect to the profile page
    return redirect(url_for('main.profile', user_id=current_user.id))

@main.route('/search_users', methods=['GET'])
@login_required
def search_users():
    query = request.args.get('query')  # Get the search query from the request
    results = []

    if query:
        # Search for users whose username contains the query string
        results = User.query.filter(User.username.ilike(f'%{query}%')).all()

    return render_template('dashboard.html', results=results)

@main.route('/follow/<int:user_id>')
@login_required
def follow(user_id):
    user = User.query.get_or_404(user_id)
    if user == current_user:
        flash('You cannot follow yourself.', 'danger')
        return redirect(url_for('main.profile', user_id=user.id))
    
    current_user.follow(user)
    db.session.commit()
    flash(f'You are now following {user.username}.', 'success')
    return redirect(url_for('main.profile', user_id=user.id))

@main.route('/unfollow/<int:user_id>')
@login_required
def unfollow(user_id):
    user = User.query.get_or_404(user_id)
    if user == current_user:
        flash('You cannot unfollow yourself.', 'danger')
        return redirect(url_for('main.profile', user_id=user.id))
    
    current_user.unfollow(user)
    db.session.commit()
    flash(f'You have unfollowed {user.username}.', 'info')
    return redirect(url_for('main.profile', user_id=user.id))


@main.route('/dashboard', methods=['GET', 'POST'])
@login_required
def dashboard():
    # Handle search query if provided
    search_query = request.args.get('search', '')  # Get the search query from the URL
    
    # Search for users by username
    users = User.query.filter(User.username.contains(search_query)).all()

    # Fetch posts from followed users
    followed_posts = Post.query.join(followers, (followers.c.followed_id == Post.user_id)) \
        .filter(followers.c.follower_id == current_user.id) \
        .order_by(Post.timestamp.desc()).all()

    return render_template('dashboard.html', posts=followed_posts, users=users, search_query=search_query)

@main.route('/create_post', methods=['GET', 'POST'])
@login_required
def create_post():
    form = PostForm()

    if form.validate_on_submit():
        new_post = Post(content=form.content.data, user_id=current_user.id)
        db.session.add(new_post)
        db.session.commit()
        return redirect(url_for('main.dashboard'))  # Redirect to the dashboard after post creation

    return render_template('create_post.html', form=form)  # Render the form for post creation

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in current_app.config['ALLOWED_EXTENSIONS']


# Profile route: handles both GET and POST
@main.route('/profile', methods=['GET', 'POST'])
@login_required
def profile():
    if request.method == 'POST':
        # Handle profile picture upload
        if 'profile_picture' in request.files:
            file = request.files['profile_picture']
            if file and allowed_file(file.filename):  # Check if the file is allowed
                filename = secure_filename(file.filename)
                filepath = os.path.join(current_app.config['UPLOAD_FOLDER'], filename)

                # Ensure the upload folder exists
                if not os.path.exists(current_app.config['UPLOAD_FOLDER']):
                    os.makedirs(current_app.config['UPLOAD_FOLDER'])

                file.save(filepath)  # Save the file

                # Update the user's profile picture path in the database
                current_user.profile_picture = filename

        # Update other user details (username, email, bio)
        if 'username' in request.form:
            current_user.username = request.form['username']
        if 'email' in request.form:
            current_user.email = request.form['email']
        if 'bio' in request.form:
            current_user.bio = request.form['bio']
        
        db.session.commit()  # Commit the changes to the database
        flash('Your profile has been updated!', 'success')
        return redirect(url_for('main.profile'))  # Redirect to the profile page after submission

    # GET request: render the profile page
    return render_template('profile.html', user=current_user)

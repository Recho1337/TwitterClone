from flask import Blueprint, request, jsonify
from app.models import db, User
from werkzeug.security import generate_password_hash
from flask_jwt_extended import create_access_token
from flask import request

main_routes = Blueprint('main_routes', __name__)

@main_routes.route('/api/register', methods=['POST'])
def register():
    data = request.json
    username = data.get('username')
    email = data.get('email')
    password = data.get('password')

    if not username or not email or not password:
        return jsonify({'error': 'All fields are required'}), 400

    hashed_password = generate_password_hash(password)
    user = User(username=username, email=email, password=hashed_password)
    
    db.session.add(user)
    db.session.commit()
    return jsonify({'message': 'User registered successfully!'}), 201

@main_routes.route('/api/login', methods=['POST'])
def login():
    data = request.json
    user = User.query.filter_by(email=data['email']).first()
    
    if user and user.check_password(data['password']):
        token = create_access_token(identity=user.id)
        return jsonify({'access_token': token})
    
    return jsonify({'error': 'Invalid credentials'}), 401

@main_routes.route('/api/tweets', methods=['GET'])
def get_tweets():
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 10, type=int)
    tweets = Tweet.query.paginate(page, per_page, False).items

    return jsonify([tweet.to_dict() for tweet in tweets])
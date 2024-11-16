from app import create_app, db
from app.models import User, Tweet

app = create_app()

with app.app_context():
    db.create_all()

    user1 = User(username="john_doe", email="john@example.com", password="hashed_password")
    user2 = User(username="jane_doe", email="jane@example.com", password="hashed_password")

    db.session.add(user1)
    db.session.add(user2)

    tweet1 = Tweet(content="Hello World!", user_id=1)
    tweet2 = Tweet(content="My first tweet!", user_id=2)

    db.session.add(tweet1)
    db.session.add(tweet2)

    db.session.commit()

class Config:
    SECRET_KEY = 'caeb1f821be868e82275597648c9ac4c'
    SQLALCHEMY_DATABASE_URI = 'sqlite:///app.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False  # To disable Flask-SQLAlchemy modification tracking
    UPLOAD_FOLDER = 'app/static/uploads'
    ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

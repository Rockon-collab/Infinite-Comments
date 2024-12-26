

from flask import Flask
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_wtf.csrf import CSRFProtect
from flask_cors import CORS


db = SQLAlchemy()
bcrypt = Bcrypt()
migrate = Migrate()
app = Flask(__name__)
# csrf = CSRFProtect(app)

def create_app(config_name='default'):
    
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///comments.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['SECRET_KEY'] = 'my_secret_key_007'
    app.config['WTF_CSRF_ENABLED'] = False
    app.config['SESSION_COOKIE_SECURE'] = False
    app.config['SESSION_COOKIE_SAMESITE'] = 'Lax'
    app.config['SESSION_COOKIE_HTTPONLY'] = True
    app.config['SESSION_TYPE'] = 'filesystem'
    
    # Example: Load different configurations based on config_name
    if config_name == 'testing':
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test_comm.db'


    CORS(app, supports_credentials=True, resources={r"/*": {"origins": "http://localhost:3000"}})
    # CORS(app, supports_credentials=True, origins=["http://localhost:3000"])

    db.init_app(app)
    migrate.init_app(app, db)
    bcrypt.init_app(app)

    from .routes import routes
    app.register_blueprint(routes)

    with app.app_context():
        from .models import User, Comment

    return app



# Create virtrual evn
# python3 -m venv env
# Activate env
# source env/bin/activate

# Install Requirement
# pip install -r requirements.txt

# Migration Commands
#  



# To run the application:
# python run.py

#for test case
#python -m unittest discover task_app/test



from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from flask_session import Session
from os import path
from flask_login import LoginManager, login_manager

db = SQLAlchemy()
sess = Session()
cors = CORS()

DB_NAME = "database.db"


def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'pee pee poo poo'
    app.config['SESSION_TYPE'] = 'filesystem'
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DB_NAME}'

    sess.init_app(app)
    cors.init_app(app)
    db.init_app(app)

    from .api import api
    from .auth import auth

    app.register_blueprint(api, url_prefix='/')
    app.register_blueprint(auth, url_prefix='/')

    from .models import User, Document

    create_database(app)

    login_manager = LoginManager()
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(id):
        return User.query.get(int(id))

    return app

def create_database(app):
    if not path.exists('website/' + DB_NAME):
        db.create_all(app=app)
        print('Created database!')
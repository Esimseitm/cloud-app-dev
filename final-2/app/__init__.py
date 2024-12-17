from flask import Flask
from app.extensions import db, bcrypt, jwt
from app.config import Config
from app.routes import init_routes

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    # Инициализация расширений
    db.init_app(app)
    bcrypt.init_app(app)
    jwt.init_app(app)

    # Инициализация маршрутов
    init_routes(app)

    return app

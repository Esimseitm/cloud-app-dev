from .auth_routes import auth_bp
from .event_routes import event_bp
from .category_routes import category_bp

def init_routes(app):
    app.register_blueprint(auth_bp)
    app.register_blueprint(event_bp)
    app.register_blueprint(category_bp)

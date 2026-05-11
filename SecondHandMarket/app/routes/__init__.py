from app.routes.auth import auth_bp
from app.routes.items import items_bp
from app.routes.api import api_bp
from app.routes.profile import profile_bp


def register_blueprints(app):
    app.register_blueprint(items_bp)
    app.register_blueprint(auth_bp, url_prefix='/auth')
    app.register_blueprint(profile_bp, url_prefix='/profile')
    app.register_blueprint(api_bp, url_prefix='/api')
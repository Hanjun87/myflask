from flask import Flask
import os
from app.extensions import db, init_db


def create_app():
    app = Flask(__name__,
                template_folder='../templates',
                static_folder='../static')
    app.secret_key = 'your-secret-key-here'

    db_path = os.path.join(app.root_path, '..', 'app.db')
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{db_path}'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    UPLOAD_FOLDER = os.path.join(app.root_path, '../static/images')
    ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}
    app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
    app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024

    init_db(app)

    from app.routes import register_blueprints
    register_blueprints(app)

    @app.context_processor
    def inject_globals():
        from datetime import datetime
        return {
            'now': datetime.now(),
            'site_name': '中古·回想'
        }

    @app.errorhandler(404)
    def not_found(error):
        from flask import flash, redirect, url_for
        flash('页面不存在', 'danger')
        return redirect(url_for('items.index'))

    @app.errorhandler(500)
    def internal_error(error):
        from flask import flash, redirect, url_for
        flash('服务器内部错误', 'danger')
        return redirect(url_for('items.index'))

    os.makedirs(UPLOAD_FOLDER, exist_ok=True)

    return app
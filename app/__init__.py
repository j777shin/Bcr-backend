from flask import Flask, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS

db = SQLAlchemy()


def create_app(config=None):
    app = Flask(__name__)

    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///bcr.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    if config:
        app.config.update(config)

    CORS(app)
    db.init_app(app)

    from app.routes.global_routes import global_bp
    from app.routes.country_routes import country_bp
    from app.routes.project_routes import project_bp

    app.register_blueprint(global_bp, url_prefix='/api')
    app.register_blueprint(country_bp, url_prefix='/api')
    app.register_blueprint(project_bp, url_prefix='/api')

    @app.errorhandler(404)
    def not_found(e):
        return jsonify({'error': 'Not found'}), 404

    @app.errorhandler(500)
    def server_error(e):
        return jsonify({'error': 'Internal server error'}), 500

    return app

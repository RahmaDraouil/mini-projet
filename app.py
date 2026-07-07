from flask import Flask
from models.database import db
from routes.employee_routes import employee_bp
from config import Config

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    # 🔥 ADD THIS FIX
    app.config['TESTING'] = True
    app.config['WTF_CSRF_ENABLED'] = False
    app.config['SECRET_KEY'] = app.config.get('SECRET_KEY', 'test-secret')

    db.init_app(app)
    app.register_blueprint(employee_bp)

    with app.app_context():
        db.create_all()

    return app
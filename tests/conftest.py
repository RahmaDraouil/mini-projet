import pytest
from app import create_app
from models.database import db
from models.employee import Employee

@pytest.fixture
def app():
    app = create_app()
    app.config['TESTING'] = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
    
    with app.app_context():
        db.create_all()
        yield app
        db.session.remove()
        db.drop_all()

@pytest.fixture
def client(app):
    return app.test_client()

@pytest.fixture
def runner(app):
    return app.test_cli_runner()

@pytest.fixture
def sample_employee(app):
    with app.app_context():
        employee = Employee(
            full_name='John Doe',
            email='john.doe@example.com',
            department='Engineering',
            salary=75000.00
        )
        db.session.add(employee)
        db.session.commit()
        return employee.id

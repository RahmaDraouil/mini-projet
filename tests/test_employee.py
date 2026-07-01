import pytest
from models.employee import Employee
from models.database import db

def test_index_page(client):
    response = client.get('/')
    assert response.status_code == 200
    assert b'Employee List' in response.data

def test_add_employee_page(client):
    response = client.get('/employee/add')
    assert response.status_code == 200
    assert b'Add New Employee' in response.data

def test_add_employee_success(client, app):
    response = client.post('/employee/add', data={
        'full_name': 'Jane Smith',
        'email': 'jane.smith@example.com',
        'department': 'Marketing',
        'salary': '65000.00'
    }, follow_redirects=True)
    
    assert response.status_code == 200
    assert b'Employee added successfully!' in response.data
    
    with app.app_context():
        employee = Employee.query.filter_by(email='jane.smith@example.com').first()
        assert employee is not None
        assert employee.full_name == 'Jane Smith'

def test_add_employee_duplicate_email(client, sample_employee):
    response = client.post('/employee/add', data={
        'full_name': 'Another Person',
        'email': 'john.doe@example.com',
        'department': 'Sales',
        'salary': '60000.00'
    }, follow_redirects=True)
    
    assert b'Email already exists' in response.data

def test_add_employee_invalid_data(client):
    response = client.post('/employee/add', data={
        'full_name': 'A',
        'email': 'invalid-email',
        'department': 'IT',
        'salary': '-1000'
    }, follow_redirects=True)
    
    assert response.status_code == 200

def test_edit_employee_page(client, sample_employee):
    response = client.get(f'/employee/edit/{sample_employee}')
    assert response.status_code == 200
    assert b'Edit Employee' in response.data

def test_edit_employee_success(client, app, sample_employee):
    response = client.post(f'/employee/edit/{sample_employee}', data={
        'full_name': 'John Updated',
        'email': 'john.updated@example.com',
        'department': 'Management',
        'salary': '85000.00'
    }, follow_redirects=True)
    
    assert response.status_code == 200
    assert b'Employee updated successfully!' in response.data
    
    with app.app_context():
        employee = Employee.query.get(sample_employee)
        assert employee.full_name == 'John Updated'

def test_delete_employee(client, app, sample_employee):
    response = client.post(f'/employee/delete/{sample_employee}', follow_redirects=True)
    
    assert response.status_code == 200
    assert b'Employee deleted successfully!' in response.data
    
    with app.app_context():
        employee = Employee.query.get(sample_employee)
        assert employee is None

def test_api_get_employees(client, sample_employee):
    response = client.get('/api/employees')
    assert response.status_code == 200
    data = response.get_json()
    assert isinstance(data, list)
    assert len(data) > 0

def test_api_get_employee(client, sample_employee):
    response = client.get(f'/api/employee/{sample_employee}')
    assert response.status_code == 200
    data = response.get_json()
    assert data['full_name'] == 'John Doe'

from flask import Blueprint, render_template, request, redirect, url_for, flash, jsonify
from models.database import db
from models.employee import Employee
from email_validator import validate_email, EmailNotValidError

employee_bp = Blueprint('employee', __name__)

def validate_employee_data(data, is_update=False):
    errors = []
    
    if not data.get('full_name') or len(data['full_name'].strip()) < 2:
        errors.append('Full name must be at least 2 characters')
    
    email = data.get('email', '').strip()
    if not email:
        errors.append('Email is required')
    else:
        try:
            validate_email(email)
        except EmailNotValidError:
            errors.append('Invalid email format')
    
    if not data.get('department') or len(data['department'].strip()) < 2:
        errors.append('Department must be at least 2 characters')
    
    try:
        salary = float(data.get('salary', 0))
        if salary < 0:
            errors.append('Salary must be positive')
    except (ValueError, TypeError):
        errors.append('Invalid salary format')
    
    return errors

@employee_bp.route('/')
def index():
    employees = Employee.query.order_by(Employee.created_at.desc()).all()
    return render_template('index.html', employees=employees)

@employee_bp.route('/employee/add', methods=['GET', 'POST'])
def add_employee():
    if request.method == 'POST':
        errors = validate_employee_data(request.form)
        
        if errors:
            for error in errors:
                flash(error, 'danger')
            return render_template('add_employee.html')
        
        existing = Employee.query.filter_by(email=request.form['email']).first()
        if existing:
            flash('Email already exists', 'danger')
            return render_template('add_employee.html')
        
        try:
            employee = Employee(
                full_name=request.form['full_name'].strip(),
                email=request.form['email'].strip(),
                department=request.form['department'].strip(),
                salary=float(request.form['salary'])
            )
            db.session.add(employee)
            db.session.commit()
            flash('Employee added successfully!', 'success')
            return redirect(url_for('employee.index'))
        except Exception as e:
            db.session.rollback()
            flash(f'Error adding employee: {str(e)}', 'danger')
    
    return render_template('add_employee.html')

@employee_bp.route('/employee/edit/<int:id>', methods=['GET', 'POST'])
def edit_employee(id):
    employee = Employee.query.get_or_404(id)
    
    if request.method == 'POST':
        errors = validate_employee_data(request.form, is_update=True)
        
        if errors:
            for error in errors:
                flash(error, 'danger')
            return render_template('edit_employee.html', employee=employee)
        
        existing = Employee.query.filter(
            Employee.email == request.form['email'],
            Employee.id != id
        ).first()
        if existing:
            flash('Email already exists', 'danger')
            return render_template('edit_employee.html', employee=employee)
        
        try:
            employee.full_name = request.form['full_name'].strip()
            employee.email = request.form['email'].strip()
            employee.department = request.form['department'].strip()
            employee.salary = float(request.form['salary'])
            db.session.commit()
            flash('Employee updated successfully!', 'success')
            return redirect(url_for('employee.index'))
        except Exception as e:
            db.session.rollback()
            flash(f'Error updating employee: {str(e)}', 'danger')
    
    return render_template('edit_employee.html', employee=employee)

@employee_bp.route('/employee/delete/<int:id>', methods=['POST'])
def delete_employee(id):
    employee = Employee.query.get_or_404(id)
    try:
        db.session.delete(employee)
        db.session.commit()
        flash('Employee deleted successfully!', 'success')
    except Exception as e:
        db.session.rollback()
        flash(f'Error deleting employee: {str(e)}', 'danger')
    
    return redirect(url_for('employee.index'))

@employee_bp.route('/api/employees', methods=['GET'])
def get_employees():
    employees = Employee.query.all()
    return jsonify([emp.to_dict() for emp in employees])

@employee_bp.route('/api/employee/<int:id>', methods=['GET'])
def get_employee(id):
    employee = Employee.query.get_or_404(id)
    return jsonify(employee.to_dict())

from models.database import db
from datetime import datetime

class Employee(db.Model):
    __tablename__ = 'employees'
    
    id = db.Column(db.Integer, primary_key=True)
    full_name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    department = db.Column(db.String(50), nullable=False)
    salary = db.Column(db.Numeric(10, 2), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def to_dict(self):
        return {
            'id': self.id,
            'full_name': self.full_name,
            'email': self.email,
            'department': self.department,
            'salary': float(self.salary),
            'created_at': self.created_at.strftime('%Y-%m-%d %H:%M:%S')
        }
    
    def __repr__(self):
        return f'<Employee {self.full_name}>'

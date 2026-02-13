from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

class Student(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    roll_number = db.Column(db.String(50), unique=True, nullable=False)
    name = db.Column(db.String(100))
    passes = db.relationship('LunchPass', backref='student', lazy=True)

    def __repr__(self):
        return f'<Student {self.roll_number}>'

class LunchPass(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.Integer, db.ForeignKey('student.id'), nullable=False)
    token = db.Column(db.String(100), unique=True, nullable=False)
    generated_at = db.Column(db.DateTime, default=datetime.utcnow)
    used = db.Column(db.Boolean, default=False)
    used_at = db.Column(db.DateTime)

    def __repr__(self):
        return f'<LunchPass {self.token}>'

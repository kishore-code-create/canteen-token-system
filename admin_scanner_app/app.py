from flask import Flask, render_template, request, jsonify
from flask_sqlalchemy import SQLAlchemy
import os
import sys

# Add parent directory to path for shared models
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from models import db, Student, LunchPass
from datetime import datetime

app = Flask(__name__)

# Database Configuration
# Point to root directory for shared database between apps
ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DB_PATH = os.path.join(ROOT_DIR, 'canteen_data.db')
DATABASE_URL = os.getenv('DATABASE_URL', f'sqlite:///{DB_PATH}')
if DATABASE_URL.startswith('postgres://'):
    DATABASE_URL = DATABASE_URL.replace('postgres://', 'postgresql://', 1)

app.config['SQLALCHEMY_DATABASE_URI'] = DATABASE_URL
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'admin-secret-key-change-this')

db.init_app(app)

def create_tables():
    db.create_all()

# ==================== ADMIN PORTAL ====================
@app.route('/')
def admin_dashboard():
    """Admin home page"""
    return render_template('admin_home.html')

@app.route('/admin/login', methods=['POST'])
def admin_login():
    """Admin login"""
    password = request.get_json().get('password', '')
    admin_password = os.getenv('ADMIN_PASSWORD', 'admin123')
    
    if password == admin_password:
        return jsonify({'success': True})
    return jsonify({'error': 'Invalid password'}), 401

@app.route('/admin/manage')
def admin_manage():
    """Manage students"""
    return render_template('admin_manage.html')

@app.route('/admin/api/students', methods=['GET', 'POST'])
def admin_students():
    """Get all students or add new"""
    if request.method == 'GET':
        students = Student.query.all()
        return jsonify([{
            'id': s.id,
            'roll_number': s.roll_number,
            'name': s.name,
            'passes_used': len([p for p in s.passes if p.used]),
            'passes_total': len(s.passes)
        } for s in students])
    
    # POST - Add new student
    data = request.get_json()
    roll_number = data.get('roll_number', '').strip().upper()
    name = data.get('name', '').strip()
    
    if not roll_number or not name:
        return jsonify({'error': 'Roll number and name required'}), 400
    
    if Student.query.filter_by(roll_number=roll_number).first():
        return jsonify({'error': 'Roll number already exists'}), 400
    
    new_student = Student(roll_number=roll_number, name=name)
    db.session.add(new_student)
    db.session.commit()
    
    return jsonify({'success': True, 'id': new_student.id})

@app.route('/admin/api/students/<int:student_id>', methods=['DELETE'])
def delete_student(student_id):
    """Delete student"""
    student = Student.query.get(student_id)
    if not student:
        return jsonify({'error': 'Student not found'}), 404
    
    db.session.delete(student)
    db.session.commit()
    return jsonify({'success': True})

# ==================== SCANNER ====================
@app.route('/scan')
def scanner():
    """Scanner page"""
    return render_template('scanner.html')

@app.route('/api/validate-token', methods=['POST'])
def validate_token():
    """Validate lunch pass token"""
    token = request.get_json().get('token', '').strip()
    
    if not token:
        return jsonify({'error': 'Token required'}), 400
    
    lunch_pass = LunchPass.query.filter_by(token=token).first()
    
    if not lunch_pass:
        return jsonify({'error': 'Invalid token', 'valid': False}), 404
    
    if lunch_pass.used:
        return jsonify({
            'error': 'Token already used',
            'valid': False,
            'student_name': lunch_pass.student.name,
            'used_at': lunch_pass.used_at
        }), 400
    
    # Mark as used
    lunch_pass.used = True
    lunch_pass.used_at = datetime.utcnow()
    db.session.commit()
    
    return jsonify({
        'success': True,
        'valid': True,
        'student_name': lunch_pass.student.name,
        'roll_number': lunch_pass.student.roll_number,
        'message': 'Lunch pass valid! Entry granted.'
    })

# ==================== DASHBOARD ====================
@app.route('/dashboard')
def dashboard():
    """Dashboard"""
    return render_template('dashboard.html')

@app.route('/api/stats')
def get_stats():
    """Get statistics"""
    total_students = Student.query.count()
    total_passes_generated = LunchPass.query.count()
    total_passes_used = LunchPass.query.filter_by(used=True).count()
    passes_remaining = total_passes_generated - total_passes_used
    
    return jsonify({
        'total_students': total_students,
        'total_passes_generated': total_passes_generated,
        'total_passes_used': total_passes_used,
        'passes_remaining': passes_remaining,
        'usage_percentage': round((total_passes_used / total_passes_generated * 100) if total_passes_generated > 0 else 0, 1)
    })

if __name__ == '__main__':
    with app.app_context():
        create_tables()
        print("\n👨‍💼 ADMIN & SCANNER PORTAL Running!")
        print("📊 Dashboard at: http://localhost:5001")
        print("🔍 Scanner at: http://localhost:5001/scan")
        print("👥 Admin at: http://localhost:5001/admin/manage")
        print("Press Ctrl+C to stop\n")
    
    app.run(debug=True, host='0.0.0.0', port=5001)

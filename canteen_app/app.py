from flask import Flask, render_template, request, jsonify, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
import qrcode
import io
import base64
import secrets
import string
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///canteen.db'
app.config['SECRET_KEY'] = 'your-secret-key-change-this'

db = SQLAlchemy(app)

# Database Models
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

# ==================== STUDENT PORTAL ====================
@app.route('/')
def student_home():
    """Student landing page"""
    return render_template('student_home.html')

@app.route('/student/generate', methods=['GET', 'POST'])
def student_generate():
    """Student generates lunch pass"""
    if request.method == 'POST':
        data = request.get_json()
        roll_number = data.get('roll_number', '').strip().upper()
        
        if not roll_number:
            return jsonify({'error': 'Roll number required'}), 400
        
        # Check if student exists
        student = Student.query.filter_by(roll_number=roll_number).first()
        
        if not student:
            return jsonify({'error': 'Roll number not found in system'}), 404
        
        # Check if already has unused pass
        existing_pass = LunchPass.query.filter_by(student_id=student.id, used=False).first()
        if existing_pass:
            return jsonify({'error': 'You already have an active lunch pass!'}), 400
        
        # Generate new token
        token = secrets.token_urlsafe(32)
        new_pass = LunchPass(student_id=student.id, token=token)
        db.session.add(new_pass)
        db.session.commit()
        
        # Generate QR code
        qr = qrcode.QRCode(version=1, box_size=10, border=5)
        qr.add_data(token)
        qr.make(fit=True)
        
        img = qr.make_image(fill_color="black", back_color="white")
        img_io = io.BytesIO()
        img.save(img_io, 'PNG')
        img_io.seek(0)
        img_base64 = base64.b64encode(img_io.getvalue()).decode()
        
        return jsonify({
            'success': True,
            'token': token,
            'qr_code': f'data:image/png;base64,{img_base64}',
            'message': f'Welcome {student.name}! Your lunch pass is ready.'
        })
    
    return render_template('student_generate.html')

# ==================== ADMIN PORTAL ====================
@app.route('/admin')
def admin_dashboard():
    """Admin login/dashboard"""
    return render_template('admin_login.html')

@app.route('/admin/login', methods=['POST'])
def admin_login():
    """Admin login (simple password)"""
    password = request.get_json().get('password', '')
    # Change this to your admin password
    if password == 'admin123':
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

# ==================== SCANNER/VALIDATION ====================
@app.route('/scan')
def scanner():
    """Scanner page to validate barcodes"""
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
    """Dashboard with statistics"""
    return render_template('dashboard.html')

@app.route('/api/stats')
def get_stats():
    """Get dashboard statistics"""
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

# ==================== Initialize Database ====================
@app.before_request
def create_tables():
    """Create tables if they don't exist"""
    db.create_all()

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
        
        # Add sample students if database is empty
        if Student.query.count() == 0:
            sample_students = [
                Student(roll_number='1602', name='Anand Sharma'),
                Student(roll_number='1603', name='Priya Singh'),
                Student(roll_number='1604', name='Rahul Kumar'),
                Student(roll_number='1605', name='Deepak Verma'),
                Student(roll_number='1606', name='Neha Gupta'),
            ]
            for student in sample_students:
                db.session.add(student)
            db.session.commit()
            print("Sample students added!")
    
    print("\n🚀 Canteen Token System Running!")
    print("📱 Student Portal: http://localhost:5000/student/generate")
    print("👨‍💼 Admin Portal: http://localhost:5000/admin")
    print("📊 Dashboard: http://localhost:5000/dashboard")
    print("🔍 Scanner: http://localhost:5000/scan")
    print("\nPress Ctrl+C to stop\n")
    
    app.run(debug=True, host='0.0.0.0', port=5000)

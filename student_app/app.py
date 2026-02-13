from flask import Flask, render_template, request, jsonify
from flask_sqlalchemy import SQLAlchemy
import qrcode
import io
import base64
import secrets
import os
from datetime import datetime
import sys

# Add parent directory to path for shared models
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from models import db, Student, LunchPass

app = Flask(__name__)

# Database Configuration
# Point to root directory for shared database between apps
ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DB_PATH = os.path.join(ROOT_DIR, 'canteen_data.db')
DATABASE_URL = os.getenv('DATABASE_URL', f'sqlite:///{DB_PATH}')
if DATABASE_URL.startswith('postgres://'):
    DATABASE_URL = DATABASE_URL.replace('postgres://', 'postgresql://', 1)

app.config['SQLALCHEMY_DATABASE_URI'] = DATABASE_URL
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'student-secret-key-change-this')

db.init_app(app)

def create_tables():
    db.create_all()

# ==================== STUDENT PORTAL ====================
@app.route('/')
def student_home():
    """Student home page"""
    return render_template('student_home.html')

@app.route('/generate', methods=['GET', 'POST'])
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

if __name__ == '__main__':
    with app.app_context():
        create_tables()
        print("\n🎓 STUDENT PORTAL Running!")
        print("📱 Access at: http://localhost:5000")
        print("Press Ctrl+C to stop\n")
    
    app.run(debug=True, host='0.0.0.0', port=5000)

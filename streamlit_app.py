import streamlit as st
import sys
import os
from datetime import datetime
import secrets
import qrcode
import io
import base64
from PIL import Image
import pandas as pd

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from models import db, Student, LunchPass
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

# Initialize Flask app and SQLAlchemy
flask_app = Flask(__name__)
ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(ROOT_DIR, 'canteen_data.db')
DATABASE_URL = f'sqlite:///{DB_PATH}'
flask_app.config['SQLALCHEMY_DATABASE_URI'] = DATABASE_URL
flask_app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(flask_app)

# Create tables if they don't exist
with flask_app.app_context():
    db.create_all()

# Streamlit page config
st.set_page_config(
    page_title="Canteen Token System",
    page_icon="🍽️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
    <style>
        .main-header {
            font-size: 3em;
            font-weight: bold;
            text-align: center;
            color: #2E86AB;
            margin-bottom: 1em;
        }
        .success-box {
            background-color: #D4EDDA;
            border: 2px solid #28A745;
            padding: 1em;
            border-radius: 0.5em;
            color: #155724;
        }
        .error-box {
            background-color: #F8D7DA;
            border: 2px solid #F5C6CB;
            padding: 1em;
            border-radius: 0.5em;
            color: #721C24;
        }
        .info-box {
            background-color: #E2E3E5;
            border: 2px solid #D6D8DB;
            padding: 1em;
            border-radius: 0.5em;
        }
    </style>
""", unsafe_allow_html=True)

# Sidebar navigation
st.sidebar.markdown("# 🍽️ Canteen Token System")
st.sidebar.markdown("---")

page = st.sidebar.radio(
    "Navigate to:",
    ["📱 Student Portal", "👨‍💼 Admin Panel", "📊 Dashboard"]
)

st.sidebar.markdown("---")
st.sidebar.markdown("**System Status:** ✅ Active")
st.sidebar.markdown(f"**Last Updated:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

# ================== STUDENT PORTAL ==================
if page == "📱 Student Portal":
    st.markdown('<div class="main-header">🎓 Student QR Code Generator</div>', unsafe_allow_html=True)
    st.markdown("Generate your lunch access pass with QR code")
    st.markdown("---")
    
    col1, col2 = st.columns([1, 1], gap="large")
    
    with col1:
        st.subheader("📝 Enter Your Details")
        roll_number = st.text_input(
            "Roll Number",
            placeholder="e.g., 1602-25-735-018",
            key="student_roll"
        )
        
        if st.button("🔑 Generate QR Code", type="primary", use_container_width=True):
            if not roll_number:
                st.error("❌ Please enter your roll number")
            else:
                with flask_app.app_context():
                    student = Student.query.filter_by(roll_number=roll_number).first()
                    
                    if not student:
                        st.error(f"❌ Roll number '{roll_number}' not found in system")
                        st.info("Contact admin if your roll number is incorrect")
                    else:
                        # Check if already has unused pass
                        existing_pass = LunchPass.query.filter_by(
                            student_id=student.id, 
                            used=False
                        ).first()
                        
                        if existing_pass:
                            st.warning("⚠️ You already have an active lunch pass!")
                            st.info(f"Token: {existing_pass.token}")
                        else:
                            # Generate new token
                            token = secrets.token_urlsafe(32)
                            new_pass = LunchPass(
                                student_id=student.id,
                                token=token
                            )
                            db.session.add(new_pass)
                            db.session.commit()
                            
                            # Generate QR code
                            qr = qrcode.QRCode(
                                version=1,
                                box_size=10,
                                border=5
                            )
                            qr.add_data(token)
                            qr.make(fit=True)
                            
                            img = qr.make_image(
                                fill_color="black",
                                back_color="white"
                            )
                            
                            # Convert to base64
                            img_io = io.BytesIO()
                            img.save(img_io, 'PNG')
                            img_io.seek(0)
                            img_base64 = base64.b64encode(img_io.getvalue()).decode()
                            
                            st.success(f"✅ QR Code Generated for {student.name}!")
                            st.session_state.qr_code = img_base64
                            st.session_state.token = token
                            st.session_state.student_name = student.name
    
    with col2:
        st.subheader("🎫 Your QR Code")
        if 'qr_code' in st.session_state:
            st.markdown(f"**Name:** {st.session_state.student_name}")
            st.markdown(f"**Token:** `{st.session_state.token}`")
            st.markdown("---")
            
            # Display QR
            qr_html = f'<img src="data:image/png;base64,{st.session_state.qr_code}" width="300">'
            st.markdown(qr_html, unsafe_allow_html=True)
            
            st.success("✅ Show this QR code at the canteen")
            st.info("⚠️ Each QR code can only be used once!")
        else:
            st.info("🔍 Enter your roll number and click 'Generate QR Code' to get started")

# ================== ADMIN PANEL ==================
elif page == "👨‍💼 Admin Panel":
    st.markdown('<div class="main-header">👨‍💼 Admin Management</div>', unsafe_allow_html=True)
    
    # Admin password verification
    if 'admin_logged_in' not in st.session_state:
        st.session_state.admin_logged_in = False
    
    if not st.session_state.admin_logged_in:
        st.warning("🔐 Admin access required")
        password = st.text_input("Enter admin password:", type="password")
        
        if st.button("Login", type="primary", use_container_width=True):
            if password == "admin123":
                st.session_state.admin_logged_in = True
                st.success("✅ Logged in!")
                st.rerun()
            else:
                st.error("❌ Invalid password")
    else:
        col1, col2 = st.columns(2)
        
        with col1:
            if st.button("🔚 Logout", use_container_width=True):
                st.session_state.admin_logged_in = False
                st.rerun()
        
        st.markdown("---")
        
        # Tabs for different admin functions
        admin_tab1, admin_tab2, admin_tab3 = st.tabs([
            "👥 View Students",
            "➕ Add Student",
            "🗑️ Delete Student"
        ])
        
        with admin_tab1:
            st.subheader("All Registered Students")
            
            with flask_app.app_context():
                students = Student.query.all()
                
                if students:
                    df = pd.DataFrame([
                        {
                            'Roll Number': s.roll_number,
                            'Name': s.name,
                            'Active Passes': LunchPass.query.filter_by(
                                student_id=s.id,
                                used=False
                            ).count()
                        }
                        for s in students
                    ])
                    
                    st.dataframe(df, use_container_width=True, hide_index=True)
                    st.info(f"Total Students: {len(students)}")
                else:
                    st.warning("No students found")
        
        with admin_tab2:
            st.subheader("Add New Student")
            
            col1, col2 = st.columns(2)
            with col1:
                new_roll = st.text_input("Roll Number", key="new_roll")
            with col2:
                new_name = st.text_input("Full Name", key="new_name")
            
            if st.button("✅ Add Student", type="primary", use_container_width=True):
                if not new_roll or not new_name:
                    st.error("❌ Please fill all fields")
                else:
                    with flask_app.app_context():
                        existing = Student.query.filter_by(roll_number=new_roll).first()
                        if existing:
                            st.error(f"❌ Roll number {new_roll} already exists")
                        else:
                            new_student = Student(roll_number=new_roll, name=new_name)
                            db.session.add(new_student)
                            db.session.commit()
                            st.success(f"✅ Student {new_name} added!")
                            st.rerun()
        
        with admin_tab3:
            st.subheader("Delete Student")
            
            with flask_app.app_context():
                students = Student.query.all()
                student_options = {
                    f"{s.roll_number} - {s.name}": s.id 
                    for s in students
                }
            
            if student_options:
                selected = st.selectbox(
                    "Select student to delete:",
                    options=student_options.keys()
                )
                
                if st.button("🗑️ Delete", type="secondary", use_container_width=True):
                    student_id = student_options[selected]
                    with flask_app.app_context():
                        student = Student.query.get(student_id)
                        db.session.delete(student)
                        db.session.commit()
                    st.success(f"✅ Student deleted!")
                    st.rerun()
            else:
                st.info("No students to delete")

# ================== DASHBOARD ==================
elif page == "📊 Dashboard":
    st.markdown('<div class="main-header">📊 Live Statistics</div>', unsafe_allow_html=True)
    st.markdown("Real-time system statistics and analytics")
    st.markdown("---")
    
    with flask_app.app_context():
        total_students = Student.query.count()
        total_passes = LunchPass.query.count()
        used_passes = LunchPass.query.filter_by(used=True).count()
        active_passes = total_passes - used_passes
        
        # Metrics
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric(
                "👥 Total Students",
                total_students,
                delta=None
            )
        
        with col2:
            st.metric(
                "📋 Total Passes Generated",
                total_passes,
                delta=None
            )
        
        with col3:
            st.metric(
                "✅ Active Passes",
                active_passes,
                delta=f"-{used_passes} used"
            )
        
        with col4:
            if total_passes > 0:
                usage_percent = (used_passes / total_passes) * 100
                st.metric(
                    "📈 Usage Rate",
                    f"{usage_percent:.1f}%",
                    delta=None
                )
            else:
                st.metric("📈 Usage Rate", "0%", delta=None)
        
        st.markdown("---")
        
        # Charts
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("Pass Usage Status")
            usage_data = {
                'Status': ['Used', 'Available'],
                'Count': [used_passes, active_passes]
            }
            usage_df = pd.DataFrame(usage_data)
            st.bar_chart(usage_df.set_index('Status'))
        
        with col2:
            st.subheader("Student Distribution")
            st.info(f"""
            - Total registered students: {total_students}
            - Generated passes: {total_passes}
            - Passes per student: {total_passes / max(total_students, 1):.2f}
            """)
        
        st.markdown("---")
        st.markdown("### Recent Activity")
        
        recent_passes = LunchPass.query.order_by(LunchPass.generated_at.desc()).limit(10).all()
        
        if recent_passes:
            activity_data = []
            for p in recent_passes:
                student = Student.query.get(p.student_id)
                activity_data.append({
                    'Roll Number': student.roll_number,
                    'Student Name': student.name,
                    'Generated': p.generated_at.strftime("%Y-%m-%d %H:%M"),
                    'Status': "Used" if p.used else "Active",
                    'Used At': p.used_at.strftime("%Y-%m-%d %H:%M") if p.used_at else "-"
                })
            
            activity_df = pd.DataFrame(activity_data)
            st.dataframe(activity_df, use_container_width=True, hide_index=True)
        else:
            st.info("No passes generated yet")
        
        st.markdown("---")
        st.caption("Data updates in real-time")

# 🍽️ Canteen Token System - Python Web App

A complete Python Flask web application for managing lunch passes in a canteen with QR code generation and scanning.

## 🎯 Features

- **👨‍🎓 Student Portal**: Generate unique QR code lunch passes
- **👨‍💼 Admin Panel**: Manage students and system
- **🔍 Scanner**: Real-time QR code validation
- **📊 Dashboard**: Live statistics and analytics
- **🛡️ Secure**: Token-based system prevents fraud

## 🏗️ 3-Portal Architecture

1. **Student Portal** (`/student/generate`)
   - Students enter roll number
   - Generate unique QR code pass
   - One-time use per day

2. **Admin Portal** (`/admin`)
   - Manage student database
   - Add/remove students
   - View student statistics

3. **Scanner Portal** (`/scan`)
   - Scan QR codes with camera
   - Real-time validation
   - Green/Red response

4. **Dashboard** (`/dashboard`)
   - Live statistics
   - Usage analytics
   - Student count tracking

## 📋 System Requirements

- Python 3.7+
- Windows/Mac/Linux

## 🚀 Quick Start

### Step 1: Install Dependencies

```bash
cd canteen_app
pip install -r requirements.txt
```

### Step 2: Run the Application

```bash
python app.py
```

You should see:
```
🚀 Canteen Token System Running!
📱 Student Portal: http://localhost:5000/student/generate
👨‍💼 Admin Portal: http://localhost:5000/admin
📊 Dashboard: http://localhost:5000/dashboard
🔍 Scanner: http://localhost:5000/scan
```

### Step 3: Access Portals

Open your browser and visit:
- **Home**: http://localhost:5000
- **Student**: http://localhost:5000/student/generate
- **Admin**: http://localhost:5000/admin (Password: `admin123`)
- **Dashboard**: http://localhost:5000/dashboard
- **Scanner**: http://localhost:5000/scan

## 📱 Sample Login Credentials

**Admin Password**: `admin123`

(Change this in `app.py` line: `if password == 'admin123':`)

## 📚 Sample Students

The system comes pre-loaded with 5 sample students:
- Roll: 1602, Name: Anand Sharma
- Roll: 1603, Name: Priya Singh
- Roll: 1604, Name: Rahul Kumar
- Roll: 1605, Name: Deepak Verma
- Roll: 1606, Name: Neha Gupta

## 🔄 Complete Workflow

```
1. Student scans QR code posted near canteen
   ↓
2. Student visits website at http://localhost:5000/student/generate
   ↓
3. Student enters roll number (e.g., 1602)
   ↓
4. System generates UNIQUE QR code + token
   ↓
5. Student shows QR code to you
   ↓
6. You open Scanner at http://localhost:5000/scan
   ↓
7. You point phone camera at student's QR
   ↓
8. System validates token:
   - ✅ VALID → Student enters
   - ❌ ALREADY USED → Error
   - ❌ INVALID → Error
```

## 🗄️ Database

SQLite database (`canteen.db`) is automatically created with:
- **Students Table**: roll_number, name, id
- **LunchPass Table**: token, student_id, used, timestamp

## 🛠️ Project Structure

```
canteen_app/
├── app.py                  # Main Flask application
├── requirements.txt        # Python dependencies
├── README.md              # This file
├── canteen.db             # SQLite database (auto-created)
├── templates/             # HTML pages
│   ├── student_home.html
│   ├── student_generate.html
│   ├── admin_login.html
│   ├── admin_manage.html
│   ├── scanner.html
│   └── dashboard.html
└── static/                # CSS & JavaScript
    ├── css/
    └── js/
```

## 🔐 Security Features

✅ Token-based pass system (not just roll number)
✅ One-time use tokens
✅ Admin password protection
✅ Timestamp tracking
✅ Prevents duplicate entries
✅ Unique token generation

## 📊 Real-Time Dashboard

The dashboard auto-refreshes every 5 seconds showing:
- Total students
- Total passes generated
- Total passes used
- Remaining passes
- Usage percentage chart

## 🚨 Customization

### Change Admin Password
Edit `app.py` line ~168:
```python
if password == 'YOUR_NEW_PASSWORD':
```

### Change Port
Edit `app.py` last line:
```python
app.run(debug=True, host='0.0.0.0', port=5000)  # Change 5000 to desired port
```

### Add More Students
Use Admin Panel or edit directly in database.

## 🐛 Troubleshooting

**Port 5000 already in use?**
```bash
# Windows
netstat -ano | findstr :5000
taskkill /PID <PID> /F

# Mac/Linux
lsof -i :5000
kill -9 <PID>
```

**Camera not working?**
- Make sure browser has camera permission
- Try different browser (Chrome recommended)
- Check camera hardware

**Database corrupted?**
```bash
# Delete the database
rm canteen.db
# Restart app - new database will be created
python app.py
```

## 📱 Mobile Support

✅ Works on mobile browsers
✅ Camera access from phone
✅ Responsive design
✅ Touch-friendly buttons

## 🌐 Network Access

To access from other devices on same network:

Find your computer's IP:
```bash
# Windows
ipconfig

# Mac/Linux
ifconfig
```

Then access from other device:
```
http://YOUR_IP:5000
```

## 📝 License

This project is free to use and modify for educational purposes.

## 🤝 Support

For issues or improvements, feel free to modify the code!

---

**Made with ❤️ for smart canteen management**

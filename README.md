# 🍽️ Canteen Token System - Cloud Ready

A complete Python Flask application for managing canteen lunch passes with QR code generation and real-time validation. **Two separate apps** deployed to the cloud.

[![Python](https://img.shields.io/badge/Python-3.10-blue)](https://www.python.org/)
[![Flask](https://img.shields.io/badge/Flask-2.3.2-green)](https://flask.palletsprojects.com/)
[![Status](https://img.shields.io/badge/Status-Production%20Ready-brightgreen)]()

## 📱 Two Independent Applications

### 1️⃣ Student App (Port 5000)
- Students enter roll number
- Generate unique QR code lunch pass
- One-time use per day
- Simple, clean interface

**Deploy to:** `student-canteen-app.herokuapp.com`

### 2️⃣ Admin & Scanner App (Port 5001)
- **Admin Panel**: Manage 213 students
- **Scanner**: Real-time QR validation
- **Dashboard**: Live statistics
- **Features**: Add/remove students, track usage

**Deploy to:** `admin-scanner-app.herokuapp.com`

## 🗄️ Database
- **213 students** from Excel file
- SQLite (local) or PostgreSQL (cloud)
- Automatic migrations

## 🚀 Quick Start (Local)

### Student App
```bash
cd student_app
pip install -r requirements.txt
python app.py
# Access: http://localhost:5000
```

### Admin & Scanner App
```bash
cd admin_scanner_app
pip install -r requirements.txt
python app.py
# Access: http://localhost:5001
```

## ☁️ Cloud Deployment (Heroku)

### Student App
```bash
cd student_app
heroku create student-canteen-app
heroku config:set DATABASE_URL=postgresql://...
heroku config:set SECRET_KEY=your-secret-key
git push heroku main
```

### Admin & Scanner App
```bash
cd admin_scanner_app
heroku create admin-scanner-app
heroku config:set DATABASE_URL=postgresql://...
heroku config:set ADMIN_PASSWORD=your-admin-password
git push heroku main
```

## 📊 Student Database
- **Total Students**: 213 (from IEEE NEXUS 2026 registrations)
- **Columns**: Roll Number, Name
- **Auto-loaded** on app startup

## 🔑 Environment Variables

### Student App (.env)
```
DATABASE_URL=sqlite:///canteen_data.db
SECRET_KEY=student-secret-key
FLASK_ENV=production
```

### Admin & Scanner App (.env)
```
DATABASE_URL=sqlite:///canteen_data.db
SECRET_KEY=admin-secret-key
ADMIN_PASSWORD=admin123
FLASK_ENV=production
```

## 📁 Project Structure

```
canteen-token-system/
├── student_app/                    # 👨‍🎓 Student Portal
│   ├── app.py
│   ├── requirements.txt
│   ├── Procfile
│   ├── runtime.txt
│   └── templates/
│       └── student_home.html
│
├── admin_scanner_app/              # 👨‍💼 Admin & Scanner
│   ├── app.py
│   ├── requirements.txt
│   ├── Procfile
│   ├── runtime.txt
│   └── templates/
│       ├── admin_home.html
│       ├── admin_manage.html
│       ├── scanner.html
│       └── dashboard.html
│
├── models.py                       # Shared database models
├── .gitignore
└── README.md
```

## 🔐 Security Features

✅ **Token-based system** (not just roll number)
✅ **One-time use tokens**
✅ **Admin password protection**
✅ **Timestamp tracking**
✅ **Duplicate prevention**
✅ **Unique token generation**

## 📊 Dashboard Features

Real-time statistics:
- Total students in system
- Total lunch passes generated
- Total passes used
- Remaining passes
- Usage percentage chart
- Auto-refresh every 5 seconds

## 🔍 Scanner Features

- 📱 Mobile-friendly camera access
- ✅ Green screen on valid pass
- ❌ Red screen on invalid/used
- 🔊 Optional sound alerts
- ⚡ Real-time validation

## 👥 Admin Panel

Manage students:
- Add new students
- View all 213 students
- Delete students
- Check usage statistics
- Track individual passes

## 🌐 Network Access

Access from any device on network:
```
Student App: http://<YOUR_IP>:5000
Admin App: http://<YOUR_IP>:5001
```

## 📱 Mobile Support

✅ Fully responsive design
✅ Touch-friendly buttons
✅ Mobile browser camera access
✅ Optimized for phones

## 🐛 Troubleshooting

**Port already in use?**
```bash
# Find and kill process
netstat -ano | findstr :5000
taskkill /PID <PID> /F
```

**Database issues?**
```bash
# Delete and recreate
rm canteen_data.db
python app.py  # Auto-creates new DB
```

**Camera not working?**
- Check browser permissions
- Use Chrome (best support)
- Allow camera access when prompted

## 🚀 Production Deployment

### Deploy to Heroku

1. **Install Heroku CLI**
2. **Login**: `heroku login`
3. **Create apps**:
   ```bash
   heroku create student-canteen-app
   heroku create admin-scanner-app
   ```
4. **Set environment variables**:
   ```bash
   heroku config:set -a student-canteen-app DATABASE_URL=postgresql://...
   heroku config:set -a admin-scanner-app DATABASE_URL=postgresql://...
   heroku config:set -a admin-scanner-app ADMIN_PASSWORD=your-password
   ```
5. **Deploy**:
   ```bash
   git push heroku main
   ```

### Deploy to AWS / Google Cloud

See cloud-specific deployment guides in `docs/deployment.md`

## 📞 Support

For issues, check the logs:
```bash
heroku logs -a student-canteen-app --tail
heroku logs -a admin-scanner-app --tail
```

## 📄 License

This project is open source and available under the MIT License.

---

**Built with ❤️ for IEEE NEXUS 2026**

**Version**: 2.0 (Cloud-Ready, Two Apps)
**Last Updated**: Feb 13, 2026

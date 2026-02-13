# 📋 Project Structure & Files

## Root Directory
```
canteen-token-system/
├── student_app/                    # 👨‍🎓 Student Portal App
├── admin_scanner_app/              # 👨‍💼 Admin & Scanner Portal App
├── canteen_app/                    # Original monolithic app (deprecated)
├── models.py                       # Shared database models
├── README.md                       # Main documentation
├── CLOUD_DEPLOYMENT.md             # Cloud deployment guide
├── DEPLOYMENT_CHECKLIST.md         # This file
├── .gitignore                      # Git ignore file
├── setup_github.bat                # Windows GitHub setup
├── setup_github.sh                 # Linux/Mac GitHub setup
└── Registrations for IEEE NEXUS 2026.xlsx  # Student data (213 students)
```

## Student App Structure
```
student_app/
├── app.py                          # Flask application (5000)
├── requirements.txt               # Python dependencies
├── Procfile                       # Heroku deployment config
├── runtime.txt                    # Python version
├── .env.example                   # Environment variables template
├── templates/
│   ├── student_home.html         # Main page
│   └── student_generate.html     # QR generation (redirects)
└── static/                        # CSS & JavaScript
    ├── css/
    └── js/
```

## Admin & Scanner App Structure
```
admin_scanner_app/
├── app.py                          # Flask application (5001)
├── requirements.txt               # Python dependencies
├── Procfile                       # Heroku deployment config
├── runtime.txt                    # Python version
├── .env.example                   # Environment variables template
├── templates/
│   ├── admin_home.html           # Home page
│   ├── admin_manage.html         # Student management
│   ├── scanner.html              # QR code scanner
│   └── dashboard.html            # Live statistics
└── static/                        # CSS & JavaScript
    ├── css/
    └── js/
```

## Database
- Shared models in `models.py`
- SQLite: `canteen_data.db` (local)
- PostgreSQL (cloud)
- **213 students** from Excel file

## Key Files

| File | Purpose |
|------|---------|
| `models.py` | Shared Student & LunchPass models |
| `student_app/app.py` | Student portal - QR generation |
| `admin_scanner_app/app.py` | Admin + Scanner portal |
| `requirements.txt` | Python packages |
| `Procfile` | Cloud deployment config |
| `runtime.txt` | Python version 3.10 |
| `.env.example` | Environment template |
| `README.md` | Main documentation |
| `CLOUD_DEPLOYMENT.md` | Cloud deployment steps |

## Environment Variables

### Student App
- `DATABASE_URL`: Database connection
- `SECRET_KEY`: Flask secret key
- `FLASK_ENV`: development/production

### Admin & Scanner App
- `DATABASE_URL`: Database connection
- `SECRET_KEY`: Flask secret key
- `ADMIN_PASSWORD`: Admin login password
- `FLASK_ENV`: development/production

## Deployment Targets

| App | Local | Cloud |
|-----|-------|-------|
| **Student** | localhost:5000 | https://student-canteen-app.herokuapp.com |
| **Admin/Scanner** | localhost:5001 | https://admin-scanner-app.herokuapp.com |

## Database Schema

### Students Table
```sql
CREATE TABLE student (
    id INTEGER PRIMARY KEY,
    roll_number VARCHAR(50) UNIQUE NOT NULL,
    name VARCHAR(100)
);
```

### LunchPass Table
```sql
CREATE TABLE lunch_pass (
    id INTEGER PRIMARY KEY,
    student_id INTEGER FOREIGN KEY,
    token VARCHAR(100) UNIQUE NOT NULL,
    generated_at DATETIME,
    used BOOLEAN DEFAULT FALSE,
    used_at DATETIME
);
```

## API Endpoints

### Student App
- `GET /` - Home page
- `GET /generate` - QR generation page
- `POST /generate` - Generate QR code

### Admin & Scanner App
- `GET /` - Home page
- `GET /admin/manage` - Student management
- `POST /admin/login` - Admin authentication
- `GET /admin/api/students` - List all students
- `POST /admin/api/students` - Add student
- `DELETE /admin/api/students/<id>` - Delete student
- `GET /scan` - Scanner page
- `POST /api/validate-token` - Validate QR token
- `GET /dashboard` - Dashboard
- `GET /api/stats` - Statistics API

## Technology Stack

- **Backend**: Python 3.10, Flask 2.3.2
- **Database**: SQLite (local), PostgreSQL (cloud)
- **Frontend**: Bootstrap 5, HTML5, JavaScript
- **QR Code**: qrcode library
- **Images**: Pillow
- **Environment**: python-dotenv
- **Server**: Gunicorn (production)
- **Deployment**: Heroku

## Statistics

- **Total Students**: 213 (from IEEE NEXUS 2026)
- **Database Size**: ~50KB (SQLite)
- **Cloud Dyno Type**: hobby-dev (free tier on Heroku)
- **Response Time**: < 100ms

## Deployment Checklist

See `DEPLOYMENT_CHECKLIST.md` for step-by-step guide.

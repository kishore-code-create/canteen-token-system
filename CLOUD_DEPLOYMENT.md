# Cloud Deployment Guide

## 🚀 Deploying to Heroku

### Prerequisites
- Heroku CLI installed
- GitHub account
- PostgreSQL account (optional for production DB)

### Step 1: Create GitHub Repository

1. Go to https://github.com/new
2. Repository name: `canteen-token-system`
3. Create repository
4. Push code:
```bash
git remote add origin https://github.com/YOUR_USERNAME/canteen-token-system.git
git branch -M main
git push -u origin main
```

### Step 2: Deploy Student App

```bash
cd student_app

# Login to Heroku
heroku login

# Create app
heroku create student-canteen-app

# Set environment variables
heroku config:set \
  SECRET_KEY=$(openssl rand -hex 16) \
  FLASK_ENV=production

# Deploy
git push heroku main

# View logs
heroku logs -a student-canteen-app --tail
```

**Access at**: `https://student-canteen-app.herokuapp.com`

### Step 3: Deploy Admin & Scanner App

```bash
cd ../admin_scanner_app

# Create app
heroku create admin-scanner-app

# Set environment variables
heroku config:set \
  SECRET_KEY=$(openssl rand -hex 16) \
  ADMIN_PASSWORD=your-secure-password \
  FLASK_ENV=production

# Deploy
git push heroku main

# View logs
heroku logs -a admin-scanner-app --tail
```

**Access at**: `https://admin-scanner-app.herokuapp.com`

### Step 4: Share PostgreSQL Database (Optional)

To use same database for both apps:

```bash
# Create PostgreSQL database
heroku addons:create heroku-postgresql:hobby-dev -a student-canteen-app

# Get connection string
heroku config -a student-canteen-app | grep DATABASE_URL

# Copy to admin app
heroku config:set DATABASE_URL=<connection-string> -a admin-scanner-app
```

### Step 5: Seed Database with Students

```bash
# From local machine
python -c "
import sys
sys.path.insert(0, 'student_app')
from models import db, Student
from app import app
import pandas as pd

with app.app_context():
    db.create_all()
    
    # Read Excel file
    df = pd.read_excel('Registrations for IEEE NEXUS 2026 (Responses) (1).xlsx')
    
    for _, row in df.iterrows():
        if pd.notna(row['Roll Number']):
            roll = str(row['Roll Number']).strip().upper()
            name = str(row['Name ']).strip() if pd.notna(row['Name ']) else 'N/A'
            
            if not Student.query.filter_by(roll_number=roll).first():
                student = Student(roll_number=roll, name=name)
                db.session.add(student)
    
    db.session.commit()
    print('Database seeded!')
"
```

## 🌐 AWS Deployment

### Using Elastic Beanstalk

```bash
# Install EB CLI
pip install awsebcli

# Initialize
eb init canteen-token-system --platform python-3.10

# Create environment
eb create canteen-student --instance-type t2.micro
eb create canteen-admin --instance-type t2.micro

# Deploy
eb deploy
```

## 🔧 Configuration on Cloud

### Environment Variables (Student App)
```
DATABASE_URL=postgresql://...
SECRET_KEY=random-secure-key
FLASK_ENV=production
```

### Environment Variables (Admin & Scanner App)
```
DATABASE_URL=postgresql://...
SECRET_KEY=random-secure-key
ADMIN_PASSWORD=secure-password
FLASK_ENV=production
```

## 🔄 Continuous Deployment

Enable automatic deployment from GitHub:

1. Go to Heroku app settings
2. Click "GitHub" under Deployment method
3. Connect GitHub account
4. Select `canteen-token-system` repository
5. Enable "Automatic deploys from main"

## 📊 Database Backup & Restore

```bash
# Backup
heroku pg:backups:capture -a student-canteen-app

# Download backup
heroku pg:backups:download -a student-canteen-app

# Restore
heroku pg:backups:restore <backup-url> -a student-canteen-app
```

## 🐛 Production Debugging

```bash
# View app logs
heroku logs -a student-canteen-app --tail

# Check app status
heroku ps -a student-canteen-app

# View config variables
heroku config -a student-canteen-app

# Scale dynos
heroku ps:scale web=2 -a student-canteen-app
```

## 🚨 Common Issues

**App crashes on startup:**
```bash
heroku logs -a app-name --tail
# Check DATABASE_URL and SECRET_KEY are set
```

**Database connection error:**
```bash
# Verify Heroku PostgreSQL addon
heroku addons -a app-name

# Reset database
heroku pg:reset -a app-name
```

**Port binding error:**
```bash
# Check Procfile uses correct port
# Heroku uses PORT env variable automatically
```

---

**For more help**: https://devcenter.heroku.com/articles/getting-started-with-python

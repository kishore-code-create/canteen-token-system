# ✅ Deployment Checklist

## Phase 1: Local Testing

- [ ] **Student App runs on localhost:5000**
  ```bash
  cd student_app
  python app.py
  ```

- [ ] **Admin & Scanner App runs on localhost:5001**
  ```bash
  cd admin_scanner_app
  python app.py
  ```

- [ ] **All 213 students loaded in database**
  ```bash
  python check_students.py
  ```

- [ ] **Student QR generation works**
  - Enter roll number
  - Get QR code
  - Verify token generated

- [ ] **Admin login works**
  - Password: admin123
  - Access student management

- [ ] **Scanner works**
  - Camera opens
  - Scan QR code
  - Validation works (green/red)

- [ ] **Dashboard shows stats**
  - Student count
  - Passes generated
  - Passes used
  - Auto-refresh works

## Phase 2: Prepare for Cloud

- [ ] **GitHub account created**
  - username: YOUR_USERNAME
  - email configured

- [ ] **Heroku account created**
  - verified email
  - payment method added

- [ ] **Git initialized locally**
  ```bash
  git init
  git add .
  git commit -m "Initial commit"
  ```

- [ ] **Environment variables set**
  - `.env.example` files created
  - Copy to `.env` for local testing

- [ ] **Procfile verified**
  - `web: gunicorn app:app` in both apps

- [ ] **requirements.txt verified**
  - All dependencies listed
  - gunicorn included

- [ ] **runtime.txt verified**
  - Python 3.10.6 specified

- [ ] **Database backup created**
  ```bash
  cp canteen_data.db canteen_data.db.backup
  ```

## Phase 3: GitHub Setup

- [ ] **Create GitHub repository**
  - Name: canteen-token-system
  - Public (for easy access)
  - No template

- [ ] **Add remote origin**
  ```bash
  git remote add origin https://github.com/YOUR_USERNAME/canteen-token-system.git
  ```

- [ ] **Push to GitHub**
  ```bash
  git branch -M main
  git push -u origin main
  ```

- [ ] **Verify on GitHub**
  - All files present
  - No sensitive data exposed
  - .gitignore working

## Phase 4: Deploy Student App to Heroku

- [ ] **Login to Heroku**
  ```bash
  heroku login
  ```

- [ ] **Create Heroku app**
  ```bash
  heroku create student-canteen-app
  ```

- [ ] **Set environment variables**
  ```bash
  heroku config:set \
    SECRET_KEY=<random-key> \
    FLASK_ENV=production
  ```

- [ ] **Deploy from GitHub**
  ```bash
  git push heroku main
  ```
  *(From student_app directory)*

- [ ] **Check app status**
  ```bash
  heroku ps -a student-canteen-app
  heroku logs -a student-canteen-app --tail
  ```

- [ ] **Test app**
  - Open: https://student-canteen-app.herokuapp.com
  - Enter roll number
  - Verify QR code generated

- [ ] **Enable automatic deploys** (Optional)
  - GitHub > Settings > Automatic deploys

## Phase 5: Deploy Admin & Scanner App to Heroku

- [ ] **Create Heroku app**
  ```bash
  heroku create admin-scanner-app
  ```

- [ ] **Set environment variables**
  ```bash
  heroku config:set \
    SECRET_KEY=<random-key> \
    ADMIN_PASSWORD=<secure-password> \
    FLASK_ENV=production
  ```

- [ ] **Setup shared database** (Optional)
  ```bash
  # If sharing DB with Student app:
  heroku config:set DATABASE_URL=$(heroku config -a student-canteen-app --json | jq -r '.DATABASE_URL') -a admin-scanner-app
  ```

- [ ] **Deploy from GitHub**
  ```bash
  git push heroku main
  ```
  *(From admin_scanner_app directory)*

- [ ] **Check app status**
  ```bash
  heroku ps -a admin-scanner-app
  heroku logs -a admin-scanner-app --tail
  ```

- [ ] **Test app**
  - Open: https://admin-scanner-app.herokuapp.com
  - Login with admin password
  - Check student list (~213 students)
  - Try scanner
  - Check dashboard

## Phase 6: Production Setup

- [ ] **Enable PostgreSQL** (if using Heroku free tier)
  ```bash
  heroku addons:create heroku-postgresql:hobby-dev -a student-canteen-app
  heroku config -a student-canteen-app | grep DATABASE_URL
  ```

- [ ] **Monitor logs daily**
  ```bash
  heroku logs -a student-canteen-app --tail
  heroku logs -a admin-scanner-app --tail
  ```

- [ ] **Setup error tracking** (Optional)
  - Sentry integration
  - Email alerts

- [ ] **Domain mapping** (Optional)
  ```bash
  heroku domains:add student.yourdomain.com -a student-canteen-app
  heroku domains:add admin.yourdomain.com -a admin-scanner-app
  ```

- [ ] **SSL/TLS enabled**
  - Automatic on Heroku
  - Verify HTTPS works

- [ ] **Backup database weekly**
  ```bash
  heroku pg:backups:capture -a student-canteen-app
  ```

## Phase 7: Testing

- [ ] **Functional Testing**
  - [ ] Student QR generation
  - [ ] Admin login
  - [ ] Add new student
  - [ ] Delete student
  - [ ] Scanner validation
  - [ ] Dashboard updates

- [ ] **Load Testing**
  - [ ] Multiple concurrent users
  - [ ] Database performance
  - [ ] API response times

- [ ] **Security Testing**
  - [ ] Admin password works
  - [ ] SQLi prevention
  - [ ] XSS prevention
  - [ ] CSRF protection

- [ ] **Edge Cases**
  - [ ] Invalid roll number
  - [ ] Duplicate token scan
  - [ ] Missing camera permission
  - [ ] Network timeout

## Phase 8: Documentation

- [ ] **README.md updated**
  - Cloud URLs included
  - Deployment steps documented

- [ ] **CLOUD_DEPLOYMENT.md created**
  - Step-by-step guide
  - Troubleshooting section

- [ ] **API documentation created** (Optional)
  - Endpoint descriptions
  - Request/response examples

- [ ] **User guide created** (Optional)
  - Student instructions
  - Admin instructions
  - Scanner instructions

## Phase 9: Launch

- [ ] **Announce to students**
  - Provide Student App URL
  - Instructions for QR generation

- [ ] **Announce to admin**
  - Provide Admin App URL
  - Credentials provided securely

- [ ] **Monitor first day**
  - Check logs for errors
  - Be available for support
  - Monitor database size

- [ ] **Gather feedback**
  - Ask students for issues
  - Ask admin for suggestions
  - Plan improvements

## Phase 10: Maintenance

- [ ] **Weekly backups**
  ```bash
  # Every Monday
  heroku pg:backups:capture -a student-canteen-app
  ```

- [ ] **Monthly log review**
  - Check for errors
  - Analyze usage patterns
  - Plan optimizations

- [ ] **Security updates**
  - Update Python packages
  - Update dependencies
  - Review dependencies

- [ ] **Performance monitoring**
  - Response times
  - Database queries
  - Dyno utilization

---

## ✨ Success Criteria

- ✅ Both apps deployed and running
- ✅ All 213 students accessible
- ✅ QR generation working
- ✅ Scanner validation working
- ✅ Dashboard showing stats
- ✅ Admin panel functional
- ✅ No errors in logs
- ✅ Response times < 200ms
- ✅ Database connections stable
- ✅ HTTPS working

---

**Status**: Ready for deployment! 🚀

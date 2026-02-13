#!/bin/bash

# Canteen Token System - GitHub Setup Script

echo "🚀 Setting up GitHub repository..."

# Initialize git if not already done
if [ ! -d .git ]; then
    git init
    echo "✅ Git initialized"
fi

# Add all files
git add .
echo "✅ Files staged"

# Create initial commit
git commit -m "Initial commit: Two separate apps (Student + Admin/Scanner) with 213 students from Excel"
echo "✅ Initial commit created"

# Instructions for user
echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "📝 Next Steps:"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""
echo "1️⃣  Create GitHub repository at: github.com/new"
echo "   Name: canteen-token-system"
echo ""
echo "2️⃣  Connect to remote:"
echo "   git remote add origin https://github.com/YOUR_USERNAME/canteen-token-system.git"
echo "   git branch -M main"
echo "   git push -u origin main"
echo ""
echo "3️⃣  Deploy to Heroku:"
echo "   heroku login"
echo "   cd student_app"
echo "   heroku create student-canteen-app"
echo "   git push heroku main"
echo ""
echo "   cd ../admin_scanner_app"
echo "   heroku create admin-scanner-app"
echo "   git push heroku main"
echo ""
echo "✨ System is ready for cloud deployment!"
echo ""

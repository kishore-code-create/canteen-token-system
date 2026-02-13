"""
Cloud Database Initialization Script
Run this on Heroku after deployment
"""

import os
import sys
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

def init_cloud_database():
    """Initialize database on cloud (Heroku, AWS, etc)"""
    
    # Import Flask app
    try:
        from app import app, db
        
        with app.app_context():
            # Create all tables
            db.create_all()
            print("✅ Database tables created successfully")
            
            # Check if students exist (should be seeded from local db)
            from models import Student
            count = Student.query.count()
            print(f"✅ Students in database: {count}")
            
            if count == 0:
                print("⚠️  Warning: No students found. Please seed the database.")
                print("   Run: python seed_database.py")
            
            return True
    
    except Exception as e:
        print(f"❌ Error: {str(e)}")
        return False

if __name__ == '__main__':
    print("🌐 Initializing Cloud Database...")
    success = init_cloud_database()
    sys.exit(0 if success else 1)

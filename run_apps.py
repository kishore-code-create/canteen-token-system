#!/usr/bin/env python3
"""
Run both Flask apps in Replit
Student app on port 5000
Admin app on port 5001
"""
import os
import sys
import subprocess
import time
import threading

def run_student_app():
    """Start student app"""
    print("\n" + "="*60)
    print("Starting STUDENT APP on port 5000...")
    print("="*60 + "\n")
    
    os.chdir("student_app")
    subprocess.run([sys.executable, "app.py"], env={
        **os.environ,
        "FLASK_ENV": "production",
        "FLASK_APP": "app.py"
    })

def run_admin_app():
    """Start admin app"""
    # Give student app time to start
    time.sleep(3)
    
    print("\n" + "="*60)
    print("Starting ADMIN & SCANNER APP on port 5001...")
    print("="*60 + "\n")
    
    os.chdir("../admin_scanner_app")
    subprocess.run([sys.executable, "app.py"], env={
        **os.environ,
        "FLASK_ENV": "production",
        "FLASK_APP": "app.py"
    })

if __name__ == "__main__":
    print("\n" + "🎉 "*20)
    print("\nCANTEEN TOKEN SYSTEM - STARTING BOTH APPS")
    print("\n" + "🎉 "*20 + "\n")
    
    # Start student app in background thread
    student_thread = threading.Thread(target=run_student_app, daemon=False)
    student_thread.start()
    
    # Start admin app in main thread
    run_admin_app()

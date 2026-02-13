#!/bin/bash
# Start both Flask apps on Replit

echo "=========================================="
echo "CANTEEN TOKEN SYSTEM"
echo "Starting Both Apps..."
echo "=========================================="

# Install dependencies
echo ""
echo "Installing dependencies..."
pip install -q flask flask-sqlalchemy qrcode pillow gunicorn python-dotenv psycopg2-binary

echo ""
echo "=========================================="
echo "STUDENT APP (Port 5000)"
echo "=========================================="
echo ""

# Start Student App in background
cd student_app
python app.py &
STUDENT_PID=$!

# Wait for student app to start
sleep 2

echo ""
echo "=========================================="
echo "ADMIN & SCANNER APP (Port 5001)"
echo "=========================================="
echo ""

# Start Admin App in background
cd ../admin_scanner_app
python app.py &
ADMIN_PID=$!

echo ""
echo "=========================================="
echo "BOTH APPS RUNNING!"
echo "=========================================="
echo ""
echo "Student Portal: http://localhost:5000"
echo "Admin Portal:   http://localhost:5001"
echo ""
echo "Press Ctrl+C to stop"
echo ""

# Keep both running
wait $STUDENT_PID $ADMIN_PID

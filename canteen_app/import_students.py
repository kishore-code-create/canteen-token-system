import pandas as pd
import os
from app import app, db, Student

# Read the Excel file
excel_file = r"c:\Users\nanda\OneDrive\Desktop\canteen tokkens\Registrations for IEEE NEXUS 2026 (Responses) (1).xlsx"

try:
    # Read Excel file
    print("📖 Reading Excel file...")
    df = pd.read_excel(excel_file)
    
    print("\n📋 Excel Columns Found:")
    print(df.columns.tolist())
    
    print("\n📊 First few rows:")
    print(df.head())
    
    # Find roll number column (try different possible names)
    roll_col = None
    possible_names = ['Roll Number', 'roll number', 'Roll No', 'roll no', 'RollNo', 'Roll', 'roll']
    
    for col in possible_names:
        if col in df.columns:
            roll_col = col
            print(f"\n✅ Found Roll Number Column: '{roll_col}'")
            break
    
    if not roll_col:
        print("\n❌ Roll number column not found!")
        print("Available columns:", df.columns.tolist())
        exit(1)
    
    # Filter out empty rows
    df_clean = df[df[roll_col].notna()].copy()
    df_clean[roll_col] = df_clean[roll_col].astype(str).str.strip().str.upper()
    
    print(f"\n📝 Found {len(df_clean)} valid students")
    
    # Add students to database
    with app.app_context():
        added = 0
        skipped = 0
        
        for idx, row in df_clean.iterrows():
            roll_number = str(row[roll_col]).strip().upper()
            
            # Skip if empty
            if not roll_number or roll_number == 'NAN':
                skipped += 1
                continue
            
            # Check if already exists
            existing = Student.query.filter_by(roll_number=roll_number).first()
            if existing:
                skipped += 1
                continue
            
            # Get name if available (try different name columns)
            name = "N/A"
            for name_col in ['Name', 'name', 'Student Name', 'student name']:
                if name_col in df.columns and pd.notna(row[name_col]):
                    name = str(row[name_col]).strip()
                    break
            
            # Add to database
            student = Student(roll_number=roll_number, name=name)
            db.session.add(student)
            added += 1
            
            if added % 10 == 0:
                print(f"  Added: {added} students...")
        
        db.session.commit()
        
        print(f"\n✅ Import Complete!")
        print(f"   ✔️  Added: {added} students")
        print(f"   ⏭️  Skipped: {skipped} (duplicates/empty)")
        
        # Show total students
        total = Student.query.count()
        print(f"\n📊 Total students in database: {total}")

except Exception as e:
    print(f"\n❌ Error: {str(e)}")
    import traceback
    traceback.print_exc()

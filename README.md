# Canteen Token System

A digital QR-code based canteen management system for institutions. Replaces physical lunch tokens with unique QR passes, validated in real time by scanner operators. Includes three dedicated interfaces for students, operators, and admins.

**Stack:** Python · Flask · Streamlit · SQLite · Docker · qrcode · pyzbar

---

## Overview

Physical token systems are slow and fraud-prone. This system digitises the entire workflow — students generate a one-time QR pass, operators scan it at the counter, and admins monitor attendance and usage in real time from a dashboard.

## Interfaces

| App | Purpose |
|-----|---------|
| Student App | Generate unique QR lunch token by roll number |
| Scanner App | Camera-based QR validation at the counter |
| Admin Dashboard | Live attendance tracking and export |

## Features

- One-token-per-student enforcement to prevent fraud
- Real-time QR validation via device camera
- Admin analytics with CSV export
- Cloud-deployable on Streamlit Cloud, Railway, or Docker

## Getting Started

```bash
git clone https://github.com/kishore-code-create/canteen-token-system.git
cd canteen-token-system
pip install -r requirements.txt
python run_apps.py
```

**Run individual apps:**
```bash
streamlit run canteen_app/app.py
streamlit run admin_scanner_app/app.py
```

**Docker:**
```bash
docker-compose up --build
```

## Project Structure

```
canteen-token-system/
├── canteen_app/          # Student token interface
├── admin_scanner_app/    # Admin and scanner interface
├── student_app/          # Student portal
├── models.py             # Database models
├── run_apps.py           # Multi-app launcher
├── Dockerfile.*          # Docker configurations
└── requirements.txt
```

## Author

**Nanda Kishore** — [nandakishoredevarashetti@gmail.com](mailto:nandakishoredevarashetti@gmail.com)  
[GitHub](https://github.com/kishore-code-create) · [LinkedIn](https://linkedin.com/in/nanda-kishore-devarashetti)

---

MIT License

# 🍽️ Canteen Token System

> QR-code based canteen lunch pass management system — built with Python, Flask and Streamlit

![Python](https://img.shields.io/badge/Python-3.10-blue?logo=python) ![Flask](https://img.shields.io/badge/Flask-2.x-black?logo=flask) ![Streamlit](https://img.shields.io/badge/Streamlit-deployed-red?logo=streamlit) ![Docker](https://img.shields.io/badge/Docker-ready-blue?logo=docker)

## 🏫 Overview

A complete digital canteen management system that replaces physical tokens with QR codes. Built for college/institutional use, it streamlines lunch pass generation, validation, and attendance tracking across three roles: students, scanner operators, and admins.

## ✨ Features

- 🎫 **QR Token Generation** — Students generate unique QR lunch passes
- 📷 **Real-time Scanner** — Operator app validates tokens via camera
- 👨‍💼 **Admin Dashboard** — Full attendance and usage analytics
- ☁️ **Cloud Ready** — Deployable on Streamlit Cloud, Railway, or Docker
- 🔒 **One-time Use** — Each token is single-use to prevent fraud
- 📊 **Live Reports** — Real-time attendance tracking

## 🛠️ Tech Stack

| Component | Technology |
|-----------|-----------|
| Backend | Python, Flask |
| Web Apps | Streamlit |
| Database | SQLite |
| QR Codes | qrcode, pyzbar |
| Deployment | Docker, Railway, Streamlit Cloud |

## 🚀 Quick Start

```bash
# Clone the repo
git clone https://github.com/kishore-code-create/canteen-token-system.git
cd canteen-token-system

# Install dependencies
pip install -r requirements.txt

# Run all apps together
python run_apps.py
```

### Individual Apps
```bash
streamlit run canteen_app/app.py      # Student app
streamlit run admin_scanner_app/app.py # Scanner/Admin app
```

## 📁 Project Structure

```
canteen-token-system/
├── canteen_app/          # Student-facing token app
├── admin_scanner_app/    # Admin and scanner app
├── student_app/          # Student portal
├── models.py             # Database models
├── run_apps.py           # Launch all apps
├── streamlit_app.py      # Unified Streamlit entry
├── Dockerfile.*          # Docker configurations
└── requirements.txt
```

## 👨‍💻 Author

**Nanda Kishore** — AI/ML Engineer  
📧 nandakishoredevarashetti@gmail.com  
🔗 [GitHub](https://github.com/kishore-code-create) | [LinkedIn](https://linkedin.com/in/nanda-kishore-devarashetti)

## 📄 License

MIT License


# Northstar Employee Management System

A Django employee directory with authentication, dashboard analytics, departments, reports, CSV export, Philippine phone validation, peso salary display, and profile photos.

## Setup

```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
pip install -r requirements.txt
Copy-Item .env.example .env
```

Set the values in `.env`, create the MySQL database, then run:

```powershell
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```

Open `http://127.0.0.1:8000/`.

## GitHub upload

```powershell
git add .
git commit -m "Initial employee management system"
git branch -M main
git remote add origin https://github.com/Hazeee23/employee_management_system.git
git push -u origin main
```

Never commit `.env`, `db.sqlite3`, `venv`, uploaded media, or passwords.

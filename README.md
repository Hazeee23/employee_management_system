# Northstar Employee Management System

Northstar is a Django-based employee management system for organizing employee records, departments, reports, and workforce information in one workspace.

The interface is designed for simple daily use by HR teams and administrators, with a dashboard-first layout, clear navigation, search and filters, and staff-only management actions.

## Features

- Dashboard with employee, department, salary, and hiring summaries
- Employee directory with search, filtering, sorting, and pagination
- Department overview with headcount, average salary, and latest hire data
- Reports page with hiring trends, salary range, and department summaries
- Add, edit, view, and securely delete employee records
- Staff-only bulk deletion with CSRF protection
- CSV export for employee data
- Login and logout using Django authentication
- Staff users can manage records; regular users have read-only access
- Philippine mobile number validation and normalization to `+639...`
- Philippine peso salary display using `₱`
- Optional profile photos, emergency contacts, and employee notes
- Responsive UI with dashboard, directory, department, and report navigation
- Northstar browser-tab favicon and branded sidebar

## Technology

- Python 3.13+
- Django 5.2
- MySQL
- Pillow for profile photo uploads
- HTML, CSS, and Django templates

## Requirements

Install the following before setup:

- Python 3.13 or newer
- MySQL Server
- Git

## Local setup

Clone the repository and enter the project directory:

```powershell
git clone https://github.com/Hazeee23/employee_management_system.git
cd employee_management_system
```

Create and activate a virtual environment:

```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
```

Install dependencies:

```powershell
pip install -r requirements.txt
```

Create a local environment file:

```powershell
Copy-Item .env.example .env
```

Update `.env` with your local MySQL credentials:

```env
DJANGO_SECRET_KEY=replace-with-a-long-random-secret
DJANGO_DEBUG=True
DJANGO_ALLOWED_HOSTS=127.0.0.1,localhost
DB_NAME=employee_management
DB_USER=root
DB_PASSWORD=your-mysql-password
DB_HOST=localhost
DB_PORT=3306
```

Create the MySQL database, then apply migrations:

```powershell
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```

Open the application at `http://127.0.0.1:8000/`.

## Main routes

| Page | URL |
| --- | --- |
| Sign in | `/login/` |
| Dashboard | `/employees/` |
| People directory | `/employees/directory/` |
| Departments | `/employees/departments/` |
| Reports | `/employees/reports/` |
| Add employee | `/employees/add/` |

## User permissions

All employee pages require authentication.

- **Staff users:** add, edit, delete, bulk-delete, export, and view employees
- **Regular users:** view employees, departments, dashboard, and reports

Create an administrator account with:

```powershell
python manage.py createsuperuser
```

## Testing

Run the full test suite with:

```powershell
python manage.py check
python manage.py test
```

## Static files and media

Static assets are stored in `static/`. Uploaded employee profile photos are stored in `media/` during development.

For production, configure a persistent media location and run:

```powershell
python manage.py collectstatic
```

## Deployment notes

Before deploying:

1. Set `DJANGO_DEBUG=False`.
2. Generate a strong `DJANGO_SECRET_KEY`.
3. Set the production domain in `DJANGO_ALLOWED_HOSTS`.
4. Configure production MySQL credentials through environment variables.
5. Run `python manage.py migrate`.
6. Run `python manage.py collectstatic`.
7. Configure persistent storage for uploaded media.

Never commit `.env`, `db.sqlite3`, `venv`, uploaded media, or passwords.

## License

This project is intended for educational and internal employee-management use.

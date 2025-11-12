# Quiz & Events App (Django)

This repository contains a simple Django project (`quizapp`) that
provides quizzes and an events list. The project already includes a
virtual environment at `.venv` and a pinned `requirements.txt`.

This README explains how to set up the development environment on
Windows (PowerShell) and how to load sample data so you can try the
site quickly.

## Prerequisites

- Windows with PowerShell
- Python 3.12 installed
- (Optional) Git

Note: The project uses a local virtual environment at the workspace
root `.venv`. If you prefer a different location, update commands
below accordingly.

## Quick setup (PowerShell)

Open PowerShell and run the following from the Django project root
(`E:\internship project\quizapp`):

```powershell
# go to project folder
Set-Location -LiteralPath 'E:\internship project\quizapp'

# Activate the virtual environment
.\.venv\Scripts\Activate.ps1

# Upgrade pip (optional)
python -m pip install --upgrade pip

# Install dependencies (if not already installed)
python -m pip install -r requirements.txt

# Create database migrations and apply them
python manage.py makemigrations
python manage.py migrate

# Create a superuser (interactively)
python manage.py createsuperuser

# Run development server
python manage.py runserver
```

Open your browser at http://127.0.0.1:8000/ . You should be
redirected to the login page. Log in with the superuser account you
created.

## Load sample data (quizzes & events)

We've included a helper script that creates a sample quiz with two
questions and a sample event. To run it, from the `quizapp` folder run:

```powershell
# ensure venv is active then
python manage.py shell < scripts/load_sample_data.py
```

That will create or reuse a `Sample Quiz` and a `Sample Event`.
After loading, visit:

- http://127.0.0.1:8000/ (homepage after login)
- http://127.0.0.1:8000/quizlist/ (list of quizzes)
- http://127.0.0.1:8000/events/ (upcoming events)

## Troubleshooting

- If you see an execution policy error when activating the venv in
  PowerShell, run:

```powershell
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
.\.venv\Scripts\Activate.ps1
```

- If `pip` shows warnings about an "invalid distribution ~ip", remove
  any strangely named files or folders from
  `quizapp/.venv/Lib/site-packages` (these are usually leftover
  artifacts from an interrupted install).

## Next steps (suggestions)

- Add a registration page so users can sign up from the frontend.
- Replace the ad-hoc `user_name` in quiz submissions with linked
  authenticated users (requires model changes + migrations).
- Add unit tests for grading logic and view access.

#  superuser
- i have alredy created superuser
-if you want to  access admin pennel here is credetial
username-Darshil
pass-12345678



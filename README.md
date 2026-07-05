# PixelGram — Instagram Clone Post Management System (Django)

A full CRUD post-management app built with Django, SQLite, Bootstrap 5, and vanilla JS.

## Features
- User registration, login, logout
- Create / edit / delete posts (owner-only edit & delete)
- Image upload (Pillow + Django ImageField)
- Instagram-style card grid on the home page
- Search posts by title or caption
- Pagination
- Django admin panel for managing posts
- Responsive Bootstrap layout
- Success/error messages on every CRUD action
- Server-side + client-side form validation

## 1. Setup

```bash
# Create and activate a virtual environment
python3 -m venv venv
source venv/bin/activate        # Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

## 2. Database migrations

```bash
python manage.py makemigrations
python manage.py migrate
```

## 3. Create an admin user

```bash
python manage.py createsuperuser
```

## 4. Run the server

```bash
python manage.py runserver
```

Visit:
- App: http://127.0.0.1:8000/
- Admin: http://127.0.0.1:8000/admin/

## 5. Git workflow

```bash
git init
git add .
git commit -m "Initial commit: Instagram clone post management system"

# Connect to GitHub (create an empty repo there first)
git remote add origin https://github.com/<your-username>/pixelgram.git
git branch -M main
git push -u origin main

# Everyday workflow after that
git pull origin main
git add .
git commit -m "message describing the change"
git push origin main
```

## Project structure

```
instagram_clone/
├── manage.py
├── requirements.txt
├── db.sqlite3                 (created after migrate)
├── instagram_clone/           # project config
│   ├── settings.py
│   ├── urls.py
│   ├── wsgi.py
│   └── asgi.py
├── posts/                     # app
│   ├── models.py
│   ├── forms.py
│   ├── views.py
│   ├── urls.py
│   ├── admin.py
│   ├── migrations/
│   ├── templates/posts/
│   │   ├── base.html
│   │   ├── home.html
│   │   ├── post_form.html
│   │   ├── post_detail.html
│   │   ├── post_confirm_delete.html
│   │   ├── login.html
│   │   └── register.html
│   └── static/posts/
│       ├── css/style.css
│       └── js/script.js
└── media/post_images/         # uploaded images land here
```

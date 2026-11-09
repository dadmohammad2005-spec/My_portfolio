# Production-Ready Developer Portfolio & Personal Website

A modern, high-performance personal portfolio website built with **Python 3.12, Django 5, and Django REST Framework**. Featuring a modern dark navy and vibrant teal design system, dark/light mode toggle with theme persistence, customizable Django Admin portal, anti-spam contact form with email notifications, and deployment readiness for Render, Railway, and PythonAnywhere.

---

## 🌟 Key Highlights & Features

- **Dynamic Identity Management**: Control your name, headline, bio, profile photo, social links, and SEO metadata directly from the Django Admin singleton without touching code.
- **Modern Responsive Design**: Custom CSS design system with CSS custom properties (`--bg-body`, `--accent-teal`), glassmorphism, responsive navigation drawer, and fluid typography (`Plus Jakarta Sans`).
- **Dark & Light Mode Switcher**: Instant theme toggle with zero flash of unstyled content (FOUC), persisted in `localStorage` and synchronized with OS preferences.
- **Interactive Project Showcase**: Card grid with instant client-side category filtering, full-text search, detailed case study pages, and screenshot galleries.
- **Skills & Timeline**: Visual skill proficiency bars categorized by domain, plus interactive Career Experience and Education timelines.
- **Spam-Protected Contact Form**: Integrated with honeypot bot trap (`website_hp`), server-side validation, database logging, and automated email notifications (console backend in dev, SMTP in production).
- **Comprehensive REST API**: Full DRF endpoints for projects, skills, timeline, blog posts, and contact submissions (`/api/projects/`, `/api/skills/`, etc.) with CORS configured.
- **Downloadable & Printable Resume**: Downloadable PDF resume support (with uploaded PDF fallback) and print-optimized stylesheet.
- **12-Factor Production Ready**: Configured with WhiteNoise for compressed static files, Gunicorn WSGI server, and `dj-database-url` for instant SQLite in dev and PostgreSQL in production.

---

## 🛠️ Tech Stack

| Layer | Technology |
|---|---|
| **Backend** | Python 3.12, Django 5.1, Django REST Framework |
| **Database** | SQLite (Development) / PostgreSQL (Production ready) |
| **Static & Media** | WhiteNoise (Brotli compression), Pillow |
| **Frontend** | Semantic HTML5, Custom Modern CSS3 (Variables & Glassmorphism), Vanilla JavaScript |
| **WSGI Server** | Gunicorn |
| **Environment** | python-dotenv, dj-database-url, django-cors-headers |

---

## 📂 Project Architecture

```
portfolio/
├── .env.example                     # Environment template
├── .env                             # Local environment variables
├── .gitignore                       # Standard Django gitignore
├── manage.py                        # Django entrypoint
├── requirements.txt                 # Frozen dependencies
├── Procfile                         # Gunicorn process definition
├── runtime.txt                      # Python runtime
├── README.md                        # Documentation
├── config/                          # Project configuration
│   ├── settings.py                  # 12-factor settings
│   ├── urls.py                      # Master URL router
│   ├── wsgi.py                      # WSGI entrypoint
│   └── asgi.py                      # ASGI entrypoint
├── apps/
│   ├── core/                        # SiteSettings, Skill, Experience, Education
│   │   ├── models.py
│   │   ├── admin.py
│   │   ├── views.py
│   │   └── management/commands/seed_data.py
│   ├── projects/                    # Projects, Categories, Screenshots
│   │   ├── models.py
│   │   ├── admin.py
│   │   └── views.py
│   ├── blog/                        # Blog posts, reading times, tags
│   │   ├── models.py
│   │   ├── admin.py
│   │   └── views.py
│   ├── contact/                     # ContactMessage, ContactForm, Anti-spam
│   │   ├── models.py
│   │   ├── forms.py
│   │   └── views.py
│   ├── api/                         # REST API serializers and ViewSets
│   │   ├── serializers.py
│   │   └── views.py
│   └── dashboard/                   # Executive Control Center & Content CMS
│       ├── forms.py
│       ├── urls.py
│       └── views.py
├── static/                          # Static assets
│   ├── css/styles.css               # Design system & theme variables
│   ├── css/dashboard.css            # Executive admin dashboard styles
│   ├── css/admin_theme.css          # Modern dark/teal theme for Django admin
│   ├── js/main.js                   # Theme toggle, filter buttons
│   ├── js/dashboard.js              # Admin sidebar, toast alerts, previews
│   ├── js/contact.js                # AJAX contact form submitter
│   └── img/favicon.svg              # Modern SVG favicon
├── media/                           # User uploads & resume PDF
└── templates/                       # Jinja/Django HTML templates
    ├── base.html
    ├── partials/ (navbar, footer, messages)
    ├── dashboard/ (executive overview, projects, blog, skills, timeline, inbox, settings)
    ├── admin/ (custom branded base_site & index with quick launch buttons)
    ├── home.html                    # Editorial 2026 hero, orbital badges, tiered skills
    ├── about.html                   # Learning journey roadmap, authentic IUB profile
    ├── careers.html                 # International internships, ATS CV, verified portals
    ├── scholarships.html            # Graduate study profile, SOP draft, scholarship tracker
    ├── projects/ (project_list, project_detail)
    ├── blog/ (blog_list, blog_detail)
    ├── contact.html
    └── resume.html                  # ATS printable resume & PDF export
```

---

## 🚀 Quickstart: Running Locally

### 1. Prerequisites
Ensure you have Python 3.10+ installed.

### 2. Clone and Setup Environment
```bash
# Clone the repository
git clone <repository_url>
cd portfolio

# Create virtual environment
python -m venv venv

# Activate virtual environment
# Windows (PowerShell):
.\venv\Scripts\Activate.ps1
# macOS / Linux:
source venv/bin/activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Configure Environment Variables
Copy `.env.example` to `.env`:
```bash
cp .env.example .env
```
*(The default `.env` is already configured for local SQLite development and console email output).*

### 5. Apply Migrations & Seed Data
```bash
# Apply database migrations
python manage.py migrate

# Create your admin superuser account
python manage.py createsuperuser

# (Optional) Seed realistic sample projects, skills, timeline, and articles:
python manage.py seed_data
```

### 6. Start the Local Server
```bash
python manage.py runserver
```
Visit **[http://127.0.0.1:8000](http://127.0.0.1:8000)** in your browser!

---

## 🔐 Dual Admin Portal System & Management

This portfolio features a **Dual Admin Experience**:

### 1. ⚡ Dedicated Executive Dashboard (`/dashboard/`)
A custom, responsive frontend administration portal styled directly to match the dark navy & vibrant teal design system:
- **Direct URL:** **[http://127.0.0.1:8000/dashboard/](http://127.0.0.1:8000/dashboard/)**
- **Direct Navbar Shortcut:** When logged in as staff, a discreet `Admin` badge appears in the top navigation bar.
- **Key Features:**
  - Real-time KPI statistics (Projects, Published Articles, Inbound Inquiries, Skills).
  - Quick action bar to create projects, write articles, add skills, and update settings.
  - Interactive project manager with status badges (Completed, In Progress, Experimental), one-click homepage pin toggles, and case study editors.
  - Technical writing publishing studio with draft/publish toggling and read time computation.
  - Inbound messages inbox with unread badges, email reply shortcuts (`mailto:`), and message read tracking.
  - Site Settings editor with live avatar and resume PDF file uploads.

### 2. 🛡️ Restyled Built-in Django Admin (`/admin/`)
- **Direct URL:** **[http://127.0.0.1:8000/admin/](http://127.0.0.1:8000/admin/)**
- Completely overhauled with custom dark navy (`#090e1a`) and teal (`#00f5d4`) styling (`admin_theme.css`), branded headers, custom welcome dashboard, and one-click launch buttons into the frontend dashboard.

### Default Superuser Credentials:
- **Username:** `admin` (or `dadmohammad` / `admin@portfolio.dev`)
- **Password:** `admin123` *(Remember to change this in production!)*

---

## 📡 REST API Reference

All endpoints return JSON and are browsable in any browser:

| Endpoint | Method | Description |
|---|---|---|
| `/api/settings/` | `GET` | Site owner identity, bio, and social handles |
| `/api/skills/` | `GET` | List of all skills (supports `?category=backend`) |
| `/api/experience/` | `GET` | Career experience timeline items |
| `/api/education/` | `GET` | Education and certifications |
| `/api/categories/` | `GET` | Project categories |
| `/api/projects/` | `GET` | Projects list (supports `?category=slug&featured=true`) |
| `/api/projects/<slug>/` | `GET` | Detailed project case study with screenshots |
| `/api/blog/` | `GET` | Published blog posts |
| `/api/blog/<slug>/` | `GET` | Detailed blog post article |
| `/api/contact/` | `POST` | Submit contact message (with honeypot check) |

---

## ☁️ Deployment Guide

### Option 1: Deploy on Render (Recommended)
1. Push your repository to GitHub.
2. In [Render Dashboard](https://dashboard.render.com), create a **New Web Service** and connect your GitHub repo.
3. Select **Environment**: `Python`.
4. Configure Build & Start commands:
   - **Build Command**: `pip install -r requirements.txt && python manage.py collectstatic --noinput && python manage.py migrate`
   - **Start Command**: `gunicorn config.wsgi:application`
5. Add Environment Variables:
   - `SECRET_KEY`: Generate a secure random string
   - `DEBUG`: `False`
   - `ALLOWED_HOSTS`: `your-app-name.onrender.com`
   - `DATABASE_URL`: Add a Render PostgreSQL database and paste the Internal Database URL here.

### Option 2: Deploy on Railway
1. In [Railway](https://railway.app), click **New Project** &rarr; **Deploy from GitHub repo**.
2. Add a **PostgreSQL** service to the project.
3. In your Web Service settings, set `PORT` to `8000`.
4. Add environment variables (`DEBUG=False`, `ALLOWED_HOSTS=*`, `DATABASE_URL=${{Postgres.DATABASE_URL}}`).
5. Railway will automatically detect the `Procfile` and launch Gunicorn with WhiteNoise.

### Option 3: Deploy on PythonAnywhere
1. Create a Python 3.12 Web App (Manual Configuration).
2. Clone your repository into `/home/username/portfolio`.
3. In the virtualenv path, specify `/home/username/portfolio/venv`.
4. Edit the WSGI configuration file to point to `config.wsgi.application`:
   ```python
   import os, sys
   path = '/home/username/portfolio'
   if path not in sys.path:
       sys.path.insert(0, path)
   os.environ['DJANGO_SETTINGS_MODULE'] = 'config.settings'
   from django.core.wsgi import get_wsgi_application
   application = get_wsgi_application()
   ```
5. Run migrations: `python manage.py migrate`.

---

## 🧪 Running Automated Tests

Run the complete test suite:
```bash
python manage.py test
```
All 19 test cases verify view status codes, templates, category filters, anti-spam honeypot behavior, email dispatching, and REST API endpoints.

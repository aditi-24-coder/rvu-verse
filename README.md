# RVUverse

**A college-exclusive, private social media platform** designed specifically for RV University students to connect, share updates, collaborate, and engage in academic and extracurricular discussions within a secure, authenticated environment.

---
## Table of Contents

- [Overview](#overview)
- [Folder Structure](#folder-structure)
- [Quick Start](#quick-start)
- [Testing Strategy](#testing-strategy)
- [Docker & Containerisation](#docker--containerisation)
- [Deployment](#deployment)
- [Screenshots](#screenshots)
- [Dependencies](#dependencies)
- [License](#license)

---

## Overview

**RVUverse** addresses the need for a closed, secure campus social media workspace by restricting access strictly to students with official university credentials.

| Feature Category | What It Provides / Key Details |
|---|---|
| **Secure Authentication** | Limited exclusively to official `@rvu.edu.in` email addresses. |
| **Profile Management** | Automatic profile creation upon registration, custom avatars, and follow/unfollow mechanisms. |
| **Posts & Engagement** | Rich text & image posts, liking/commenting features, automated hashtag parsing, and search functionality. |
| **Academic Context** | Academic department mapping (e.g., SOCSE, SOLAS, SODI) and department-filtered feed views. |
| **Communication Layer** | Direct one-to-one messaging and live notifications for likes, comments, follows, and messages. |

---

## Folder Structure

```
RVUverse/
│
├── .github/
│   └── workflows/
│       ├── deploy.yml            # CI/CD deployment workflow (GitHub Actions)
│       └── main.yml              # Automated test execution workflow
│
├── core/                         # Main social network features application package
│   ├── migrations/               # Database model schema version history
│   ├── static/                   # Static resources
│   │   ├── css/                  # Layout stylesheets
│   │   ├── js/                   # Live AJAX & notifications scripts
│   │   └── svg/                  # Application logos & vector designs
│   ├── templates/core/           # HTML user interface layouts
│   ├── tests/                    # Automated testing suite
│   ├── admin.py                  # Model registration for Django Admin dashboard
│   ├── apps.py                   # App config registration
│   ├── context_processors.py     # Custom global variables processor
│   ├── forms.py                  # Creation and editing validation schemas
│   ├── middleware.py             # Custom log and session tracing middleware
│   ├── models.py                 # Application database entities
│   ├── signals.py                # Auto-profile creation signals hooks
│   ├── urls.py                   # App-level routing mapping
│   └── views.py                  # UI controller controllers
│
├── rvuverse/                     # Root configuration package
│   ├── __init__.py
│   ├── asgi.py                   # Entrypoint for ASGI-compatible servers
│   ├── settings.py               # Core application settings and configs
│   ├── urls.py                   # Root URL dispatcher
│   └── wsgi.py                   # Entrypoint for WSGI-compatible servers
│
├── .dockerignore
├── Dockerfile
├── docker-compose.yml
├── manage.py                     # Django management CLI utility script
├── pytest.ini                    # Pytest framework settings configuration
├── requirements.txt              # Project production dependencies
└── README.md                     # Main documentation page
```

---

## Quick Start

### Prerequisites

- Python 3.10+
- SQLite3 (enabled by default in Python)
- Docker (for containerised deployment)

### Local Development

```powershell
# Clone the repository
git clone https://github.com/Serendipity-scribe-dev/RVUverse.git
cd RVUverse

# Setup and activate virtual environment
python -m venv venv
venv\Scripts\activate

# Install application requirements
pip install -r requirements.txt

# Run database migrations
python manage.py migrate

# Create an administrator account
python manage.py createsuperuser

# Run local development server
python manage.py runserver
# Server will run on http://localhost:8000
```

---

## Testing Strategy

The project contains a thorough test suite of **12 automated tests** to guarantee system stability and core integrity.

### Run Automated Tests

```powershell
# Run the entire test suite
pytest

# Run tests in verbose mode
pytest -v

# Run a specific test module
pytest core/tests/test_post.py
```

### Coverage Scope

- **Verification:** User registration, domain validator checks, and email verification.
- **Data Integrity:** Database model validations and follower relationship constraints.
- **Features validation:** Likes counters, automatic hashtag parsing, comments, events, and registrations.

---

## Docker & Containerisation

### Build Container

```powershell
# Build application container
docker build -t rvuverse .

# Run container locally
docker run -p 8000:8000 rvuverse
```

### Docker Compose

```powershell
# Run services with docker-compose
docker-compose up --build
```

---

## Deployment

The application is configured to deploy automatically via **Render** integrated with GitHub Actions.

- **Live URL:** [https://rvuverse.onrender.com](https://rvuverse.onrender.com)
- **Deployment Process:** Handled via `.github/workflows/deploy.yml` which deploys build updates upon push to the main branch.

---

## Screenshots

<img width="827" height="410" alt="Screenshot 2026-01-10 110453" src="https://github.com/user-attachments/assets/19575a81-d680-411b-baac-33948769d821" />
<img width="826" height="409" alt="Screenshot 2026-01-10 110501" src="https://github.com/user-attachments/assets/490ac804-ce25-4352-94ec-ef60e88e3554" />

<img width="819" height="469" alt="Screenshot 2026-01-10 110533" src="https://github.com/user-attachments/assets/272d210d-aa2d-48bd-bc57-b06829cc7fd3" />

<img width="807" height="221" alt="Screenshot 2026-01-10 110545" src="https://github.com/user-attachments/assets/8427d417-ac6d-4294-bfe7-ca26c0e0a3f9" />
<img width="808" height="398" alt="Screenshot 2026-01-10 110553" src="https://github.com/user-attachments/assets/d4b168c8-cd38-40ac-9dc6-2315ab6a81ea" />

<img width="796" height="405" alt="Screenshot 2026-01-10 110607" src="https://github.com/user-attachments/assets/6ca27d20-f81b-4789-9095-2c289908cc9c" />

<img width="814" height="394" alt="Screenshot 2026-01-10 110617" src="https://github.com/user-attachments/assets/6b6abb37-9239-4a47-bc04-febaf6bdaac0" />

<img width="800" height="346" alt="Screenshot 2026-01-10 110627" src="https://github.com/user-attachments/assets/376dea6e-cda6-4456-bb82-deb53b99b550" />

<img width="814" height="404" alt="Screenshot 2026-01-10 110640" src="https://github.com/user-attachments/assets/b360e747-85a2-42a6-8627-83b08f648bb4" />
<img width="812" height="409" alt="Screenshot 2026-01-10 110649" src="https://github.com/user-attachments/assets/d49abf76-5c1f-4886-8d8d-efe479adb68a" />

---

## Dependencies

| Library | Version | Description |
|---|---|---|
| **Django** | `5.2` | Core High-level Python Web Framework |
| **gunicorn** | `23.0.0` | WSGI HTTP Server for production deployment |
| **pillow** | `11.1.0` | Image processing library for user uploads |
| **pytest** | Latest | Unit testing execution runner |
| **pytest-django** | Latest | Django testing integration for pytest |
| **python-dotenv** | Latest | Secret management file parsing |

---

## License

This project is licensed under the MIT License. See [LICENSE](LICENSE) for details.

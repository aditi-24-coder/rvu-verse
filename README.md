# RVUverse – A Campus Social Media Platform

RVUverse is a private, college-exclusive social media platform designed specifically for RV University students.
It enables students to connect, share updates, collaborate, and engage in academic and extracurricular discussions within a secure and authenticated environment.

## 🔗 Live Application:
Please create your accounts and try using it!
👉 https://rvuverse.onrender.com

## 📌 Project Overview

- **Domain:** Educational Social Media Platform

- **Target Users:** RV University students

- **Authentication:** Restricted to @rvu.edu.in email IDs

- **Architecture:** Full-stack web application

- **Methodology:** Agile + CI (Continuous Integration)

---

## Features
**User Management**

- RVU email–only registration

- Secure login/logout

- Auto-created user profiles

- Follow / unfollow users

**Posts & Engagement**

- Create posts (text + image support)

- Like and comment on posts

- Hashtag extraction and search

- Department-based filtering

**Communication**

- One-to-one messaging

- Real-time-like notifications for:

- Likes

- Comments

- Follows

- Messages

**Academic Context**

- Department mapping (SOCSE, SOLAS, SODI, etc.)

- Department-specific posts and events
---

## Tech Stack
**Backend**

- Django (Python)

- Django ORM

- SQLite (development & deployment)

 **Frontend**

- HTML

- CSS

- JavaScript

- Bootstrap

**Testing & QA**

- PyTest

- Django Test Framework

**DevOps / CI**

- GitHub Actions

- Automated test execution on every push and pull request

**Deployment**

- Render

- Static & media handling

---

## Testing Strategy

A total of 12 automated tests were written to validate core functionality.

**Test Coverage Includes:**

- User registration with RVU email validation

- Department code choice validation

- Post creation (with image upload)

- Comment creation

- Follow / unfollow functionality

- Hashtag extraction

- Model integrity checks

- Basic logic tests

**Testing Tools:**

- PyTest

- Django test database (SQLite)
  
---

## How to Run Locally
```
# Clone repository
git clone https://github.com/Serendipity-scribe-dev/RVUverse.git
cd RVUverse

# Create virtual environment
python -m venv venv
venv\Scripts\activate   # Windows

# Install dependencies
pip install -r requirements.txt

# Run migrations
python manage.py migrate

# Start server
python manage.py runserver
```
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


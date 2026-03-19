# Social Media API (Twitter-like Backend)

A RESTful backend API built with Django and Django REST Framework that powers a Twitter-like social media application. The system supports user authentication, post creation, user interactions, and personalized feeds.

---

## Features

* User registration and authentication
* Create, update, and delete posts
* Like posts
* Follow and unfollow users
* Personalized feed based on followed users
* Pagination for efficient data loading

---

## Tech Stack

* Python
* Django
* Django REST Framework
* PostgreSQL (or SQLite for development)

---

## API Endpoints (Sample)

Authentication:

* POST /api/auth/register
* POST /api/auth/login

Posts:

* GET /api/posts
* POST /api/posts
* GET /api/posts/{id}

Interactions:

* POST /api/posts/{id}/like
* POST /api/users/{id}/follow

Feed:

* GET /api/feed

---

## Example Response

```json
{
  "id": 1,
  "author": "emmanuel",
  "content": "Hello world",
  "likes": 3,
  "created_at": "2026-03-18T10:00:00Z"
}
```

---

## Setup Instructions

1. Clone the repository

```
git clone https://github.com/yourusername/social-media-api.git
cd social-media-api
```

2. Create virtual environment

```
python -m venv venv
source venv/bin/activate   # Mac/Linux
venv\Scripts\activate      # Windows
```

3. Install dependencies

```
pip install -r requirements.txt
```

4. Run migrations

```
python manage.py migrate
```

5. Start server

```
python manage.py runserver
```

---

## Project Structure

* accounts → user authentication and profiles
* posts → post creation and management
* interactions → likes and follow system

---

## Key Highlights

* Designed relational database models for users, posts, and interactions
* Built RESTful APIs with proper authentication and permissions
* Implemented feed logic based on user relationships
* Structured project into modular Django apps

---

Backend Developer (Django, REST APIs)

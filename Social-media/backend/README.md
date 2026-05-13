# Social Media API

A Twitter-inspired social media backend built with Django and Django REST Framework.

This API powers a social platform where users can create posts, interact with content, follow other users, and receive a personalized feed based on engagement and user relationships.

---

## Features

* JWT authentication
* User profiles
* Create and manage posts
* Like system
* Follow / unfollow users
* Personalized feed generation
* Media upload support
* Pagination for post feeds

---

## Tech Stack

* Python
* Django
* Django REST Framework
* PostgreSQL
* JWT Authentication

---

## API Overview

### Authentication

| Method | Endpoint              | Description       |
| ------ | --------------------- | ----------------- |
| POST   | `/api/auth/register/` | Register new user |
| POST   | `/api/auth/login/`    | Authenticate user |
| POST   | `/api/auth/logout/`   | Delete Request Cookies |
| POST   | `/api/auth/token/refresh/` | Refresh access token |

---

### Posts

| Method | Endpoint                       | Description        |
| ------ | ------------------------------ | ------------------ |
| GET    | `/api/posts/feed/`             | Personalized feed(authenticated) or All feed(unauthenticated) |
| POST   | `/api/posts/`                  | Create a new post  |
| POST   | `/api/posts/{id}/toggle_like/` | Like/unlike post   |

---

### Users

| Method | Endpoint                               | Description                |
| ------ | -------------------------------------- | -------------------------- |
| GET    | `/api/users/{username}/`               | User profile               |
| POST   | `/api/users/{username}/toggle_follow/` | Follow/unfollow user       |
| GET    | `/api/users/me/`                       | Current authenticated user |

---

## Feed Logic

The personalized feed endpoint returns:

* posts from followed users
* the authenticated user’s own posts
* results ranked by engagement and recency

---

## Example Response

```json
{
  "id": 1,
  "author": {
    "username": "emmanuel"
  },
  "content": "Hello world",
  "likes_count": 5,
  "is_liked": true,
  "created_at": "2026-05-11T14:00:00Z"
}
```

---

## Project Structure

```txt
accounts/       # authentication and user profiles
posts/          # posts, comments, feed logic
interactions/   # likes and follow system
config/         # django configuration
```

---

## Local Development

### Clone Repository

```bash
git clone https://github.com/LukoOG/Fullstack_projects.git
```

### Create Virtual Environment

```bash
python -m venv venv
```

### Install Dependencies

```bash
pip install -r requirements.txt
```

### Run Migrations

```bash
python manage.py migrate
```

### Start Development Server

```bash
python manage.py runserver
```

---

## Future Improvements

* Redis caching
* Real-time notifications
* WebSocket chat
* Feed recommendation algorithm
* Docker support

---

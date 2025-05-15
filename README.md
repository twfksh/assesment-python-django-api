# Django-Blog-API

A RESTful Blog API built with Django and Django REST Framework, supporting user authentication (with JWT), user profiles, posts, tags, comments, and post likes.

## Features

- **User Registration & Authentication**
  - Register, login, logout, and refresh JWT tokens (using HttpOnly cookies for security)
  - Custom user model with email as the primary identifier
  - User profile with avatar and bio

- **Blog Posts**
  - CRUD operations for posts (authenticated users can create, update, and delete their own posts)
  - Tagging system for posts
  - Like/unlike posts

- **Comments**
  - CRUD operations for comments on posts
  - Only authenticated users can comment

- **API Permissions**
  - Only authors can modify or delete their own posts/comments
  - Read-only access for unauthenticated users

- **CORS Support**
  - Configured for cross-origin requests

## Project Structure

```
.
├── apps/
│   ├── posts/
│   └── users/
├── config/
├── db.sqlite3
├── manage.py
├── requirements.txt
├── pyproject.toml
└── .env.sample
```

## Setup

1. **Clone the repository**

   ```sh
   git clone <your-repo-url>
   cd Django-Blog-API
   ```

2. **Create and activate a virtual environment**

   ```sh
   python3 -m venv .venv
   source .venv/bin/activate  # On Windows: .venv\Scripts\activate
   ```

3. **Install dependencies**

   ```sh
   pip install -r requirements.txt
   ```

4. **Configure environment variables**

   - Copy `.env.sample` to `.env` and fill in your values:

     ```
     DEBUG=True
     SECRET_KEY=your_secret_key
     ```

5. **Apply migrations**

   ```sh
   python manage.py migrate
   ```

6. **Create a superuser (optional, for admin access)**

   ```sh
   python manage.py createsuperuser
   ```

7. **Run the development server**

   ```sh
   python manage.py runserver
   ```

## API Endpoints

### User Endpoints

- `POST /api/users/register/` — Register a new user
- `POST /api/users/login/` — Login and receive JWT tokens (set as HttpOnly cookies)
- `POST /api/users/logout/` — Logout and blacklist refresh token
- `POST /api/users/refresh-token/` — Refresh JWT tokens
- `GET/PUT /api/users/` — Get or update user info
- `GET/PUT /api/users/profile/` — Get or update user profile
- `GET/PUT /api/users/profile/avatar/` — Get or update user avatar

### Post & Tag Endpoints

- `GET /api/posts/tags/` — List all tags
- `GET/POST /api/posts/` — List or create posts
- `GET/PUT/PATCH/DELETE /api/posts/<id>/` — Retrieve, update, or delete a post
- `POST /api/posts/like/<id>/` — Like or unlike a post

### Comment Endpoints

- `GET/POST /api/posts/<post_id>/comment/` — List or create comments for a post
- `GET/PUT/PATCH/DELETE /api/posts/<post_id>/comment/<id>/` — Retrieve, update, or delete a comment

## Customization

- **User model:** See [`apps.users.models.UserAccount`](apps/users/models.py)
- **Authentication:** Custom JWT authentication using HttpOnly cookies ([`apps.users.authentication.HttpOnlyJWTAuthentication`](apps/users/authentication.py))
- **Permissions:** Custom permission classes for post/comment authorship ([`apps.posts.permissions.IsAuthorOrReadOnly`](apps/posts/permissions.py))

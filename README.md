# FastAPI Social Media Backend

A production-ready RESTful API built with **FastAPI** and **PostgreSQL** that powers a social media platform. Features include user authentication, post management, and a voting/liking system with secure JWT-based authorization.

---

## Live API Documentation

- **Swagger UI**: [https://socialmediaapp-yt22.onrender.com/docs](https://socialmediaapp-yt22.onrender.com/docs)
- **ReDoc**: [https://socialmediaapp-yt22.onrender.com/redoc](https://socialmediaapp-yt22.onrender.com/redoc)

---

## Features

- **User Management** — Create users, retrieve user details by ID
- **Authentication** — OAuth2 password flow with JWT tokens
- **Post CRUD** — Create, read, update, and delete posts
- **Voting System** — Like/unlike posts with vote count tracking
- **Protected Routes** — Bearer token authentication for secure endpoints
- **Password Hashing** — Argon2 secure password hashing
- **Environment Variables** — Configuration via `.env` file
- **Database Migrations** — Alembic-powered schema versioning

---

## Tech Stack

| Category | Technology |
|----------|------------|
| Framework | FastAPI |
| Database | PostgreSQL |
| ORM | SQLAlchemy |
| Migrations | Alembic |
| Authentication | JWT (OAuth2 Password Flow) |
| Password Hashing | Passlib (Argon2) |
| Validation | Pydantic & Pydantic Settings |
| Server | Uvicorn |
| Deployment | Render |

---

## Architecture

```
API/
├── app/
│   ├── __init__.py           # App initialization
│   ├── mainsql.py            # Main FastAPI app with routers
│   ├── config.py             # Pydantic settings (environment variables)
│   ├── database.py           # SQLAlchemy engine & session setup
│   ├── models.py             # SQLAlchemy ORM models (User, Post, Vote)
│   ├── schemas.py            # Pydantic request/response schemas
│   ├── oauth2.py             # JWT token creation & verification
│   ├── utils.py              # Password hashing functions
│   └── routers/
│       ├── auth.py           # Login endpoint
│       ├── user.py           # User CRUD endpoints
│       ├── post.py           # Post CRUD endpoints
│       └── vote.py           # Voting endpoint
├── alembic/
│   ├── env.py                # Alembic migration environment
│   └── versions/             # Migration scripts
├── .env                      # Environment variables
├── requirements.txt          # Python dependencies
└── alembic.ini               # Alembic configuration
```

| File/Folder | Responsibility |
|-------------|----------------|
| `app/routers/` | API endpoint definitions |
| `app/models.py` | Database table definitions |
| `app/schemas.py` | Request/response validation models |
| `app/oauth2.py` | JWT token generation & validation |
| `app/utils.py` | Password hashing utilities |
| `app/config.py` | Environment variable management |
| `app/database.py` | SQLAlchemy engine & session |
| `alembic/` | Database migration scripts |

---

## API Endpoints

### Authentication

| Method | Endpoint | Description | Auth Required |
|--------|----------|-------------|---------------|
| POST | `/login` | Login with email & password | No |

### Users

| Method | Endpoint | Description | Auth Required |
|--------|----------|-------------|---------------|
| POST | `/users/` | Create a new user | No |
| GET | `/users/{id}` | Get user by ID | Yes |

### Posts

| Method | Endpoint | Description | Auth Required |
|--------|----------|-------------|---------------|
| GET | `/posts/` | Get all posts (with vote count, supports pagination & search) | Yes |
| POST | `/posts/` | Create a new post | Yes |
| GET | `/posts/{id}` | Get single post by ID (with vote count) | Yes |
| PUT | `/posts/{id}` | Update a post (owner only) | Yes |
| DELETE | `/posts/{id}` | Delete a post (owner only) | Yes |

### Votes

| Method | Endpoint | Description | Auth Required |
|--------|----------|-------------|---------------|
| POST | `/vote/` | Vote on a post (dir=1) or remove vote (dir=0) | Yes |

---

## Local Setup

### 1. Clone the Repository
```bash
git clone https://github.com/tanmayayayy/SocialMediaApp
cd API
```

### 2. Create Virtual Environment
```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
# venv\Scripts\activate   # Windows
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Configure Environment Variables

Create a `.env` file in the root directory:

```env
DATABASE_HOSTNAME=localhost
DATABASE_PORT=5432
DATABASE_PASSWORD=your_password
DATABASE_NAME=fastapi
DATABASE_USERNAME=postgres

SECRET_KEY=your_secret_key
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=60
```

### 5. Run Database Migrations
```bash
alembic upgrade head
```

### 6. Start the Server
```bash
uvicorn app.mainsql:app --reload
```

- **API Docs**: `http://localhost:8000/docs`
- **ReDoc**: `http://localhost:8000/redoc`

---

## Environment Variables

| Variable | Description | Example |
|----------|-------------|---------|
| `DATABASE_HOSTNAME` | PostgreSQL host | `localhost` or Render URL |
| `DATABASE_PORT` | PostgreSQL port | `5432` |
| `DATABASE_USERNAME` | Database username | `postgres` |
| `DATABASE_PASSWORD` | Database password | `your_password` |
| `DATABASE_NAME` | Database name | `fastapi` |
| `SECRET_KEY` | JWT signing key | `your_secret_key` |
| `ALGORITHM` | JWT algorithm | `HS256` |
| `ACCESS_TOKEN_EXPIRE_MINUTES` | Token validity | `60` |

---

## Deployment

This project is deployed on **Render**:

1. Create a PostgreSQL database on Render
2. Set environment variables in Render dashboard
3. Connect GitHub repository to Render
4. Set build command: `pip install -r requirements.txt`
5. Set start command: `uvicorn app.mainsql:app --host 0.0.0.0 --port $PORT`

---

## Future Improvements

- **Docker** — Containerize application for consistent deployment
- **Unit & Integration Tests** — pytest with coverage reports
- **CI/CD Pipeline** — GitHub Actions for automated testing
- **Redis** — Caching for improved performance
- **Pagination** — Cursor-based pagination for large datasets
- **WebSockets** — Real-time notifications
- **Rate Limiting** — Prevent API abuse
- **Email Verification** — Confirm user email addresses
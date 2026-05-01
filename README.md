# 🚂 GoTrain

A Django REST API for a railway ticketing system. Allows users to search for journeys, book and purchase tickets, manage orders, and view timetables.

---

## Tech Stack

- **Python 3.11**
- **Django 5.2** + **Django REST Framework**
- **PostgreSQL 16**
- **Celery** + **Redis** (async tasks)
- **Docker** + **Docker Compose**
- **JWT Authentication** (SimpleJWT)
- **drf-spectacular** (Swagger docs)

---

## Features

- User registration and JWT authentication
- Journey search by date, source, and destination station
- Ticket booking with seat class selection (First, Second, Economy)
- Passenger info per ticket
- Automatic ticket cancellation after 15 minutes if unpaid (Celery)
- Order management and payment via profile balance
- Timetable for arrivals and departures by station
- News/announcements auto-created on journey changes
- Profile with balance top-up
- Manager role for journey management
- Crew profiles

---

## Project Structure

```
GoTrain/
├── railway/          # Core: journeys, tickets, orders, trains, routes, stations
├── users/            # Custom user model, crew profiles
├── profiles/         # User profile, balance, phone verification
├── GoTrain/          # Project settings, urls, celery config
├── docker-compose.yml
├── Dockerfile
└── requirements.txt
```

---

## Getting Started

### Prerequisites

- Docker
- Docker Compose

### Setup

1. Clone the repository:
```bash
git clone https://github.com/Qellexi/GoTrain.git
cd GoTrain
```

2. Create `.env` file based on `.env.example`:
```bash
cp .env.example .env
```

3. Fill in `.env`:
```
POSTGRES_PASSWORD=railway
POSTGRES_USER=railway
POSTGRES_DB=railway
POSTGRES_HOST=db
POSTGRES_PORT=5432
PGDATA=/var/lib/postgresql/data
DJANGO_SECRET_KEY=your-secret-key
DEBUG=True
CELERY_BROKER_URL=redis://redis:6379/0
CELERY_RESULT_BACKEND=redis://redis:6379/0
```

4. Build and run:
```bash
docker compose up --build
```

5. Create superuser:
```bash
docker compose exec gotrain python manage.py createsuperuser
```

---

## API Documentation

After running the project, Swagger UI is available at:

```
http://localhost:8001/api/docs/
```

---

## Main Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/api/v1/users/token/` | Obtain JWT token |
| POST | `/api/v1/users/token/refresh/` | Refresh JWT token |
| POST | `/api/v1/users/users/` | Register user |
| GET | `/api/v1/journeys/` | List journeys (filter by date, source, destination) |
| GET | `/api/v1/journeys/departures/` | Departures by station |
| GET | `/api/v1/journeys/arrivals/` | Arrivals by station |
| GET | `/api/v1/trains/{id}/seats/` | Available seats by class |
| POST | `/api/v1/tickets/` | Book a ticket |
| PATCH | `/api/v1/tickets/{id}/` | Update or purchase a ticket |
| GET | `/api/v1/orders/` | List user orders |
| POST | `/api/v1/orders/` | Create order from booked tickets |
| POST | `/api/v1/orders/{id}/pay/` | Pay for order |
| GET | `/api/v1/profiles/profiles/me/` | Get own profile |
| PATCH | `/api/v1/profiles/profiles/me/` | Update profile |
| POST | `/api/v1/profiles/profiles/top-up/` | Top up balance |
| GET | `/api/v1/news/` | List news and announcements |

---

## Running Tests

```bash
docker compose exec gotrain python manage.py test
```

Run tests for a specific app:
```bash
docker compose exec gotrain python manage.py test users
docker compose exec gotrain python manage.py test railway
docker compose exec gotrain python manage.py test profiles
```

---

## Environment Variables

| Variable | Description |
|----------|-------------|
| `DJANGO_SECRET_KEY` | Django secret key |
| `DEBUG` | Debug mode (True/False) |
| `POSTGRES_DB` | Database name |
| `POSTGRES_USER` | Database user |
| `POSTGRES_PASSWORD` | Database password |
| `POSTGRES_HOST` | Database host |
| `POSTGRES_PORT` | Database port |
| `CELERY_BROKER_URL` | Redis broker URL |
| `CELERY_RESULT_BACKEND` | Redis result backend URL |

---

## Admin Panel

Available at `http://localhost:8001/admin/`

Manage: users, trains, train types, stations, routes, journeys, tickets, orders, news, crew profiles.

# Weather API

A Django REST Framework API that provides current weather and 5-day forecasts using the OpenWeatherMap API. Built with a clean service layer, caching, rate limiting, background tasks, and auto-generated Swagger documentation.

---

## Features

- Current weather by city name
- 5-day forecast with day filtering
- Geocoding — converts city name to lat/lon for accurate results
- In-memory caching with 30 minute TTL
- Background task that pre-warms cache for popular cities on startup
- Rate limiting — 10 requests/min for anonymous users
- Custom error handling with meaningful error messages
- Auto-generated Swagger UI documentation

---

## Tech Stack

- Python 3.13
- Django 6.0
- Django REST Framework
- OpenWeatherMap API (Geocoding + Weather + Forecast)
- drf-spectacular (Swagger UI)
- SimpleJWT (authentication)

---

## Project Structure

```
weather_project/
├── config/
│   ├── settings.py
│   └── urls.py
├── weather/
│   ├── apps.py           # starts background task on server boot
│   ├── exceptions.py     # custom exceptions
│   ├── urls.py           # paths 
│   ├── services.py       # all business logic and external API calls
│   ├── tasks.py          # background cache warming task
│   ├── throttles.py      # custom rate limit classes
│   └── views.py          # thin views, request/response only
├── .env
├── manage.py
└── requirements.txt
```

---

## Setup

### 1. Clone the repository

```bash
git clone https://github.com/mandip-adk/weather-api.git
cd weather-api
```

### 2. Create and activate virtual environment

```bash
python -m venv venv

# Windows
venv\Scripts\activate

# Mac/Linux
source venv/bin/activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Get an API key

Sign up at [openweathermap.org](https://openweathermap.org/api) and get a free API key.

### 5. Create `.env` file

```
OPENWEATHER_API_KEY=your_api_key_here
```

### 6. Run migrations

```bash
python manage.py migrate
```

### 7. Start the server

```bash
python manage.py runserver
```

---

## API Endpoints

### Current Weather

```
GET /api/weather/?city={city}
```

**Parameters**

| Parameter | Type   | Required | Default   | Description |
|-----------|--------|----------|-----------|-------------|
| city      | string | No       | Kathmandu | City name   |

**Example Request**

```
GET /api/weather/?city=London
```

**Example Response**

```json
{
    "city": "London",
    "country": "GB",
    "lat": 51.5073219,
    "lon": -0.1276474,
    "temperature": 15.33,
    "feels_like": 14.15,
    "temp_min": 13.88,
    "temp_max": 16.68,
    "humidity": 47,
    "condition": "Clear",
    "from_cache": true
}
```

---

### 5-Day Forecast

```
GET /api/forecast/?city={city}&days={days}
```

**Parameters**

| Parameter | Type    | Required | Default   | Description          |
|-----------|---------|----------|-----------|----------------------|
| city      | string  | No       | Kathmandu | City name            |
| days      | integer | No       | 5         | Number of days (1-5) |

**Example Request**

```
GET /api/forecast/?city=Tokyo&days=3
```

**Example Response**

```json
{
    "city": "Tokyo",
    "country": "JP",
    "days": 3,
    "total_entries": 24,
    "forecast": [
        {
            "datetime": "2026-05-01 12:00:00",
            "temperature": 13.58,
            "feels_like": 12.91,
            "humidity": 58,
            "condition": "Clouds"
        }
    ],
    "from_cache": false
}
```

---

### Authentication

```
POST /api/token/          # get access and refresh tokens
POST /api/token/refresh/  # get new access token
```

**Example Login Request**

```json
{
    "username": "yourusername",
    "password": "yourpassword"
}
```

**Example Response**

```json
{
    "access": "eyJhbGci...",
    "refresh": "eyJhbGci..."
}
```

---

## Error Responses

| Status | Meaning                        | Example                              |
|--------|--------------------------------|--------------------------------------|
| 400    | Bad request / invalid params   | `{"error": "days must be a number"}` |
| 404    | City not found                 | `{"error": "City 'xyz' not found"}`  |
| 429    | Rate limit exceeded            | `{"detail": "Request was throttled"}`|
| 503    | External API unavailable       | `{"error": "Weather API timed out"}` |

---

## Rate Limiting

| User Type        | Limit         |
|------------------|---------------|
| Anonymous users  | 5 per minute  |
| Authenticated    | 30 per minute |

---

## Caching

Weather data is cached for **30 minutes** per city. On server startup a background task automatically pre-fetches weather and forecast data for these popular cities:

- Kathmandu
- London
- New York
- Tokyo
- Paris

This means first requests for these cities are served instantly from cache.

---

## API Documentation

Interactive Swagger UI is available at:

```
http://127.0.0.1:8000/api/docs/
```

---

## Environment Variables

| Variable             | Description                        |
|----------------------|------------------------------------|
| OPENWEATHER_API_KEY  | Your OpenWeatherMap API key        |

---

## Future Improvements

- Redis cache backend for production
- User registration and API key generation
- Saved cities per user account
- Weather alerts endpoint
- Celery for production-grade background tasks

---

## 👤 Author
**Mandip Adhikari**  
GitHub: https://github.com/mandip-adk

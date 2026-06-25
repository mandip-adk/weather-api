# Weather API

A Django REST Framework API that provides current weather and 5-day forecasts using the OpenWeatherMap API. Built with a clean service layer, caching, rate limiting, background tasks, and auto-generated Swagger documentation. Includes a vanilla HTML/CSS/JS frontend that consumes the live API.

---

## Live Demo

| | |
|---|---|
| 🌐 Frontend (Windrose) | https://windrose-weather.netlify.app |
| ⚙️ API base URL | https://weather-api-ugdj.onrender.com |
| 📘 Interactive API docs (Swagger) | https://weather-api-ugdj.onrender.com/api/docs/ |

> Note: the backend is on Render's free tier, so the first request after a period of inactivity may take 30-50 seconds to wake up.

---

## Features

**Backend**
- Current weather by city name
- 5-day forecast with day filtering
- Geocoding — converts city name to lat/lon for accurate results
- In-memory caching with 30 minute TTL
- Background task that pre-warms cache for popular cities on startup
- Rate limiting — 5 requests/min for anonymous users on weather endpoints
- Custom error handling with meaningful error messages
- CORS enabled so any frontend can call the API
- Auto-generated Swagger UI documentation
- JWT authentication available (weather endpoints are public, kept open since weather data isn't sensitive)

**Frontend**
- Search any city worldwide
- Current conditions with a temperature "mercury" indicator
- 5-day forecast strip
- Hand-drawn SVG weather icons (no external icon library)
- Fully responsive, works down to mobile widths

---

## Tech Stack

**Backend**
- Python 3.13, Django 6.0, Django REST Framework
- OpenWeatherMap API (Geocoding + Weather + Forecast)
- drf-spectacular (Swagger UI)
- djangorestframework-simplejwt (authentication)
- django-cors-headers (cross-origin requests from the frontend)
- gunicorn + whitenoise (production server + static files)
- Deployed on Render

**Frontend**
- HTML, CSS, vanilla JavaScript (no framework, no build step)
- Fetches data directly from the deployed Render API
- Deployed on Netlify

---

## Project Structure

```
weather_api/
├── config/
│   ├── settings.py
│   └── urls.py
├── weather/
│   ├── apps.py             # starts background task on server boot
│   ├── exceptions.py       # custom exceptions
│   ├── urls.py             # app-level routes
│   ├── services.py         # business logic and external API calls
│   ├── tasks.py            # background cache-warming task
│   ├── throttles.py        # custom rate limit classes
│   └── views.py            # thin views, request/response only
├── weather_frontend/
│   ├── index.html
│   ├── style.css
│   └── script.js
├── build.sh                # Render build script
├── .env
├── manage.py
└── requirements.txt
```

---

## Setup (run it locally)

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
SECRET_KEY=your_django_secret_key
DEBUG=True
ALLOWED_HOSTS=127.0.0.1,localhost
```

### 6. Run migrations

```bash
python manage.py migrate
```

### 7. Start the backend

```bash
python manage.py runserver
```

### 8. Run the frontend

Open `weather_frontend/index.html` directly in your browser (or use the VS Code "Live Server" extension). It's already pointed at the live Render API, so it works without running the backend locally too — but if you want it to call your local server instead, change `API_BASE` in `script.js` to `http://127.0.0.1:8000`.

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

> Weather and forecast endpoints don't require a token — they're public, since weather data isn't sensitive. JWT is set up and ready for any future private endpoints (e.g. saved cities per user).

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
|-------------------|---------------|
| Anonymous users   | 5 per minute  |
| Authenticated     | 30 per minute |

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

## Deployment

| | Platform | Notes |
|---|---|---|
| Backend  | Render   | gunicorn + whitenoise, env vars set in Render dashboard |
| Frontend | Netlify  | static deploy, no build step needed |

CORS is enabled on the backend (`django-cors-headers`) so the Netlify-hosted frontend — or any other origin — can call the API directly.

---

## Environment Variables

| Variable             | Description                            |
|-----------------------|-----------------------------------------|
| OPENWEATHER_API_KEY  | Your OpenWeatherMap API key             |
| SECRET_KEY           | Django secret key                       |
| DEBUG                | `True` locally, `False` in production   |
| ALLOWED_HOSTS        | Comma-separated allowed hostnames       |

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


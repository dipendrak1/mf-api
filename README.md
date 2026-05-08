# Mutual Fund NAV API

A lightweight FastAPI-based Mutual Fund NAV API using official AMFI NAV data.

This API:
- Fetches latest NAV data from AMFI
- Caches data for 1 hour
- Exposes REST endpoints
- Supports Google Sheets integration

---

# Features

- FastAPI backend
- AMFI NAV source integration
- In-memory caching (1 hour)
- JSON API endpoint
- Google Sheets compatible CSV endpoint
- Deployable on Render

---

# Tech Stack

- Python
- FastAPI
- Requests
- Uvicorn

---

# Project Structure

```text
mf-api/
│
├── main.py
├── requirements.txt
└── README.md
```

---

# Installation

## Clone Repository

```bash
git clone <your-repo-url>
cd mf-api
```

---

## Create Virtual Environment (Optional)

### Windows

```bash
python -m venv venv
venv\Scripts\activate
```

### Linux / Mac

```bash
python3 -m venv venv
source venv/bin/activate
```

---

## Install Dependencies

```bash
pip install -r requirements.txt
```

---

# requirements.txt

```text
fastapi
uvicorn
requests
```

---

# Run Application

Start the FastAPI server locally:

```bash
uvicorn main:app --reload
```

Application will run on:

```text
http://127.0.0.1:8000
```

---

# API Endpoints

## Health Check

### Endpoint

```http
GET /
```

### Response

```json
{
  "message": "MF API is running"
}
```

---

# Get Mutual Fund NAV

Returns NAV details in JSON format.

## Endpoint

```http
GET /mf/{scheme_code}
```

## Example

```http
GET /mf/122639
```

## Sample Response

```json
{
  "scheme_code": "122639",
  "scheme_name": "Parag Parikh Flexi Cap Fund - Direct Plan - Growth",
  "nav": "91.0418",
  "date": "27-Apr-2026"
}
```

---

# Google Sheets Endpoint

Returns comma-separated text compatible with Google Sheets `IMPORTDATA()`.

## Endpoint

```http
GET /mf/{scheme_code}/sheet
```

## Example

```http
GET /mf/122639/sheet
```

## Sample Response

```text
Parag Parikh Flexi Cap Fund - Direct Plan - Growth,91.0418,27-Apr-2026
```

---

# Google Sheets Usage

Use directly inside Google Sheets:

```excel
=IMPORTDATA("https://your-api.onrender.com/mf/122639/sheet")
```

---

# Data Source

Official NAV data is fetched from:

```text
https://www.amfiindia.com/spages/NAVAll.txt
```

Source:
Association of Mutual Funds in India (AMFI)

---

# Caching

The API caches NAV data in memory for 1 hour to:
- reduce AMFI requests
- improve response time
- avoid unnecessary network calls

Cache duration:

```python
3600 seconds
```

---

# Deploy on Render

## Create Render Web Service

- Environment: Python
- Build Command:

```bash
pip install -r requirements.txt
```

- Start Command:

```bash
uvicorn main:app --host 0.0.0.0 --port 10000
```

---

# Swagger Documentation

FastAPI automatically provides Swagger UI.

Open:

```text
http://127.0.0.1:8000/docs
```

or after deployment:

```text
https://your-api.onrender.com/docs
```

---

# Example Supported Scheme Codes

| Fund | Scheme Code |
|------|-------------|
| Parag Parikh Flexi Cap Fund | 122639 |
| Nippon India Small Cap Fund | 118778 |

---

# Notes

- NAV data updates once daily from AMFI
- Some scheme names may differ from AMC website naming
- Render free tier may sleep during inactivity

---

# Future Improvements

Possible enhancements:
- Search endpoint
- Bulk NAV endpoint
- Historical NAV API
- ETF support
- Redis caching
- Database integration

---

# License

MIT License

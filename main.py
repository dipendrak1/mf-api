from fastapi import FastAPI
from fastapi.responses import PlainTextResponse
import requests
import time
from datetime import datetime

app = FastAPI()

NAV_URL = "https://www.amfiindia.com/spages/NAVAll.txt"

cache_data = None
cache_time = 0


def is_valid_date(value):
    """Check whether a value looks like an AMFI date."""
    value = value.strip()

    formats = [
        "%d-%b-%Y",
        "%d-%B-%Y",
        "%d-%m-%Y",
        "%d/%m/%Y",
        "%d-%b-%y",
        "%d/%m/%y",
    ]

    for fmt in formats:
        try:
            datetime.strptime(value, fmt)
            return True
        except ValueError:
            pass

    return False


def is_valid_nav(value):
    """Check whether a value looks like a NAV number."""
    value = value.strip().replace(",", "")

    try:
        number = float(value)

        # NAV should be a positive number
        return number > 0

    except ValueError:
        return False


def find_nav_and_date(parts):
    """
    Find NAV and date dynamically instead of relying
    on fixed column positions.

    AMFI's file format can change, so we look for:
    - NAV = numeric value
    - Date = recognizable date
    """

    nav = None
    date = None

    # Search from the end because NAV/date are normally
    # towards the end of an AMFI record.
    for value in reversed(parts):
        value = value.strip()

        if date is None and is_valid_date(value):
            date = value
            continue

        if nav is None and is_valid_nav(value):
            nav = value
            continue

        if nav is not None and date is not None:
            break

    return nav, date


def load_nav_data():
    global cache_data, cache_time

    # Return cached data for 1 hour
    if cache_data is not None and time.time() - cache_time < 3600:
        return cache_data

    headers = {
        "User-Agent": (
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
            "AppleWebKit/537.36 (KHTML, like Gecko) "
            "Chrome/131.0.0.0 Safari/537.36"
        ),
        "Accept": "text/plain,*/*",
    }

    res = requests.get(
        NAV_URL,
        headers=headers,
        timeout=30,
        allow_redirects=True,
    )

    res.raise_for_status()

    lines = res.text.splitlines()

    data = []

    for line in lines:
        parts = [p.strip() for p in line.split(";")]

        # Need at least a few fields
        if len(parts) < 4:
            continue

        scheme_code = parts[0]

        # Ignore headers / non-scheme rows
        if not scheme_code.isdigit():
            continue

        scheme_name = parts[3]

        nav, date = find_nav_and_date(parts)

        # Only add records where we successfully identified
        # NAV and date.
        if nav is None or date is None:
            continue

        data.append({
            "scheme_code": scheme_code,
            "scheme_name": scheme_name,
            "nav": nav,
            "date": date,
        })

    # Only replace cache if we actually received valid data
    if data:
        cache_data = data
        cache_time = time.time()

    return data


@app.get("/")
def home():
    return {
        "message": "MF API is running"
    }


@app.get("/mf/{scheme_code}")
def get_nav(scheme_code: str):
    data = load_nav_data()

    for item in data:
        if item["scheme_code"] == scheme_code:
            return item

    return {
        "error": "Scheme not found"
    }


@app.get(
    "/mf/{scheme_code}/sheet",
    response_class=PlainTextResponse
)
def get_nav_sheet(scheme_code: str):
    data = load_nav_data()

    for item in data:
        if item["scheme_code"] == scheme_code:
            return (
                f"{item['scheme_name']},"
                f"{item['nav']},"
                f"{item['date'].strip()}"
            )

    return "Not Found"


# Run locally:
# uvicorn main:app --reload
#
# Example:
# http://127.0.0.1:8000/mf/119063

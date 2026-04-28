from fastapi import FastAPI
import requests
from functools import lru_cache

app = FastAPI()

NAV_URL = "https://www.amfiindia.com/spages/NAVAll.txt"

import time

cache_data = None
cache_time = 0

def load_nav_data():
    global cache_data, cache_time

    if time.time() - cache_time < 3600:  # 1 hour cache
        return cache_data

    res = requests.get(NAV_URL)
    lines = res.text.split("\n")

    data = []
    for line in lines:
        parts = line.split(";")
        if len(parts) > 5:
            data.append({
                "scheme_code": parts[0],
                "scheme_name": parts[3],
                "nav": parts[4],
                "date": parts[5]
            })

    cache_data = data
    cache_time = time.time()

    return data


@app.get("/")
def home():
    return {"message": "MF API is running"}


@app.get("/mf/{scheme_code}")
def get_nav(scheme_code: str):
    data = load_nav_data()

    for item in data:
        if item["scheme_code"] == scheme_code:
            return item

    return {"error": "Scheme not found"}

from fastapi.responses import PlainTextResponse

@app.get("/mf/{scheme_code}/sheet", response_class=PlainTextResponse)
def get_nav_sheet(scheme_code: str):
    data = load_nav_data()

    for item in data:
        if item["scheme_code"] == scheme_code:
            return f"{item['scheme_name']},{item['nav']},{item['date'].strip()}"

    return "Not Found"


# Run server:
# -> uvicorn main:app --reload
# Open in browser:
# -> http://127.0.0.1:8000/mf/119063
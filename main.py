from fastapi import FastAPI
import requests
from functools import lru_cache

app = FastAPI()

NAV_URL = "https://www.amfiindia.com/spages/NAVAll.txt"

@lru_cache(maxsize=1)
def load_nav_data():
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
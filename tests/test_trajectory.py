import json

import pytest
import requests
from pydantic_core.core_schema import JsonType
from sqlalchemy import text

from .database import db


class APIClient:
    """Клиент для работы с API с базовым URL"""

    def __init__(self, base_url):
        self.base_url = base_url.rstrip("/")
        self.session = requests.Session()

    def get(self, path, **kwargs):
        """GET запрос с базовым URL"""
        url = f"{self.base_url}{path}"
        return self.session.get(url, **kwargs)


@pytest.fixture
def api_client():
    """Фикстура, создающая клиент с базовым URL"""
    base_url = "http://localhost:8000/trajectory_points"
    # base_url = "https://orbital-catalog.auditory.ru/trajectory_points"
    client = APIClient(base_url)

    return client


def test_get_chunk(api_client):
    endpoints = [
        "/get_chunk?filter_groups=%5B%7B%22log_op%22%3A%22NONE%22%2C%22filters%22%3A%5B%7B%22field%22%3A%22orbit_id%22%2C%22op%22%3A%22%3D%3D%22%2C%22value%22%3A4342%7D%5D%7D%5D",
    ]
    requests = [
        "SELECT * from trajectory_points tp where tp.orbit_id = 4342",
    ]
    for j in range(len(endpoints)):
        response = api_client.get(endpoints[j])
        assert response.status_code == 200, "Данные не получены"

        api_data = response.json()

        engine = db.get_engine()
        with engine.connect() as conn:
            result = conn.execute(text(requests[j]))
            db_data = [dict(row._mapping) for row in result]

        api_sorted = sorted(api_data, key=lambda x: x["x"])
        db_sorted = sorted(db_data, key=lambda x: x["x"])
        assert len(api_sorted) == len(db_sorted)
        for i in range(len(api_sorted)):
            assert (
                api_sorted[i]["x"] == float(db_sorted[i]["x"])
                and api_sorted[i]["z"] == float(db_sorted[i]["z"])
                and api_sorted[i]["y"] == float(db_sorted[i]["y"])
            ), "Данные с API не совпадают с нужным из БД"

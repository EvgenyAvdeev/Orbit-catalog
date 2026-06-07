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
    base_url = "http://localhost:8000/orbit_view"
    # base_url = "https://orbital-catalog.auditory.ru/orbit_view"
    client = APIClient(base_url)

    return client


# https://orbital-catalog.auditory.ru/orbit_view/get_family_param?lib_point=L1&family_tag=V&param_name_x=t&param_name_y=cj&param_name_z=ax
def test_get_map(api_client):
    endpoints = [
        "/get_map",
        "/get_map?filter_groups=%5B%7B%22log_op%22%3A%22AND%22%2C%20%22filters%22%3A%5B%7B%22field%22%3A%22lib_point%22%2C%20%22op%22%3A%22like%22%2C%20%22value%22%3A%22L1%22%7D%2C%7B%22field%22%3A%22family_tag%22%2C%20%22op%22%3A%22like%22%2C%20%22value%22%3A%22H_n%22%7D%5D%7D%5D",
        "/get_map?filter_groups=%5B%7B%22log_op%22%3A%22AND%22%2C%20%22filters%22%3A%5B%7B%22field%22%3A%22x%22%2C%20%22op%22%3A%22%3E%22%2C%20%22value%22%3A0%7D%2C%7B%22field%22%3A%22z%22%2C%20%22op%22%3A%22%3C%22%2C%20%22value%22%3A1000%7D%5D%7D%5D",
        "/get_map?filter_groups=%5B%7B%22log_op%22%3A%22AND%22%2C%20%22filters%22%3A%5B%7B%22field%22%3A%22lib_point%22%2C%20%22op%22%3A%22like%22%2C%20%22value%22%3A%22L1%22%7D%2C%7B%22field%22%3A%22family_tag%22%2C%20%22op%22%3A%22like%22%2C%20%22value%22%3A%22H_s%22%7D%2C%7B%22field%22%3A%22x%22%2C%20%22op%22%3A%22%3E%22%2C%20%22value%22%3A0%7D%2C%7B%22field%22%3A%22z%22%2C%20%22op%22%3A%22%3C%22%2C%20%22value%22%3A1000%7D%5D%7D%5D",
    ]
    requests = [
        "SELECT x, z FROM orbits",
        "SELECT x, z FROM orbits JOIN orbit_families ON orbit_families.id = orbits.family_id WHERE lib_point = 'L1' AND family_tag='H_n'",
        "SELECT x, z FROM orbits WHERE x > 0 AND z < 1000",
        "SELECT x, z FROM orbits JOIN orbit_families ON orbit_families.id = orbits.family_id WHERE lib_point = 'L1' AND family_tag='H_s' AND x > 0 AND z < 1000",
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
            assert api_sorted[i]["x"] == float(db_sorted[i]["x"]) and api_sorted[i][
                "z"
            ] == float(db_sorted[i]["z"]), "Данные с API не совпадают с нужным из БД"


def test_get_nearest_orbit(api_client):
    endpoints = [
        "/get_nearest_orbit?x=328572.143933853&z=157.97977014946258",
        "/get_nearest_orbit?x=0&z=0",
    ]
    requests = [
        "SELECT * FROM orbits ORDER BY POW(x - 328572.143933853, 2) + POW(z - 157.97977014946258, 2) LIMIT 1;",
        "SELECT * FROM orbits ORDER BY POW(x - 0, 2) + POW(z - 0, 2) LIMIT 1;",
    ]
    for j in range(len(endpoints)):
        response = api_client.get(endpoints[j])
        assert response.status_code == 200, "Данные не получены"

        api_data = response.json()

        engine = db.get_engine()
        with engine.connect() as conn:
            result = conn.execute(text(requests[j]))
            db_data = [dict(row._mapping) for row in result]

        assert api_data["x"] == float(db_data[0]["x"]) and api_data["z"] == float(
            db_data[0]["z"]
        ), "Данные с API не совпадают с нужным из БД"


def test_get_next_orbit(api_client):
    endpoints = [
        "/get_next_orbit?lib_point=L1&family_tag=H_s&id=1",
        "/get_next_orbit?lib_point=L1&family_tag=H_s&id=2370",
    ]
    requests = [
        "SELECT orbits.id,x, z FROM orbits JOIN orbit_families ON orbit_families.id = orbits.family_id WHERE lib_point = 'L1' AND family_tag='H_s' and orbits.id=2",
        "SELECT orbits.id,x, z FROM orbits JOIN orbit_families ON orbit_families.id = orbits.family_id WHERE lib_point = 'L1' AND family_tag='H_s' and orbits.id=1",
    ]
    for j in range(len(endpoints)):
        response = api_client.get(endpoints[j])
        assert response.status_code == 200, "Данные не получены"

        api_data = response.json()

        engine = db.get_engine()
        with engine.connect() as conn:
            result = conn.execute(text(requests[j]))
            db_data = [dict(row._mapping) for row in result]

        assert api_data["x"] == float(db_data[0]["x"]) and api_data["z"] == float(
            db_data[0]["z"]
        ), "Данные с API не совпадают с нужным из БД"


def test_get_prev_orbit(api_client):
    endpoints = [
        "/get_prev_orbit?lib_point=L1&family_tag=H_s&id=2370",
        "/get_prev_orbit?lib_point=L1&family_tag=H_s&id=1",
    ]
    requests = [
        "SELECT orbits.id,x, z FROM orbits JOIN orbit_families ON orbit_families.id = orbits.family_id WHERE lib_point = 'L1' AND family_tag='H_s' and orbits.id=2369",
        "SELECT orbits.id,x, z FROM orbits JOIN orbit_families ON orbit_families.id = orbits.family_id WHERE lib_point = 'L1' AND family_tag='H_s' and orbits.id=2370",
    ]
    for j in range(len(endpoints)):
        response = api_client.get(endpoints[j])
        assert response.status_code == 200, "Данные не получены"

        api_data = response.json()

        engine = db.get_engine()
        with engine.connect() as conn:
            result = conn.execute(text(requests[j]))
            db_data = [dict(row._mapping) for row in result]

        assert api_data["x"] == float(db_data[0]["x"]) and api_data["z"] == float(
            db_data[0]["z"]
        ), "Данные с API не совпадают с нужным из БД"


def test_family_param(api_client):
    endpoints = [
        "/get_family_param?lib_point=L1&family_tag=H_s&param_name_x=x&param_name_y=cj&param_name_z=ax",
    ]
    requests = [
        "SELECT x, cj, ax FROM orbits JOIN orbit_families ON orbit_families.id = orbits.family_id WHERE lib_point = 'L1' AND family_tag='H_s'",
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
                api_sorted[i]["param_x"] == float(db_sorted[i]["x"])
                and api_sorted[i]["param_y"] == float(db_sorted[i]["cj"])
                and api_sorted[i]["param_z"] == float(db_sorted[i]["ax"])
            ), "Данные с API не совпадают с нужным из БД"


def test_get_Broucke(api_client):
    endpoints = [
        "/get_Broucke?filter_groups=%5B%7B%22log_op%22%3A%22AND%22%2C%22filters%22%3A%5B%7B%22field%22%3A%22lib_point%22%2C%22op%22%3A%22like%22%2C%22value%22%3A%22L1%22%7D%2C%7B%22field%22%3A%22family_tag%22%2C%22op%22%3A%22like%22%2C%22value%22%3A%22H_s%22%7D%5D%7D%5D",
    ]
    requests = [
        "SELECT alpha, beta FROM orbits JOIN orbit_families ON orbit_families.id = orbits.family_id WHERE lib_point = 'L1' AND family_tag='H_s'",
    ]
    for j in range(len(endpoints)):
        response = api_client.get(endpoints[j])
        assert response.status_code == 200, "Данные не получены"

        api_data = response.json()

        engine = db.get_engine()
        with engine.connect() as conn:
            result = conn.execute(text(requests[j]))
            db_data = [dict(row._mapping) for row in result]

        api_sorted = sorted(api_data, key=lambda x: x["alpha"])
        db_sorted = sorted(db_data, key=lambda x: x["alpha"])
        assert len(api_sorted) == len(db_sorted)
        for i in range(len(api_sorted)):
            assert api_sorted[i]["alpha"] == float(
                db_sorted[i]["alpha"]
            ) and api_sorted[i]["beta"] == float(db_sorted[i]["beta"]), (
                "Данные с API не совпадают с нужным из БД"
            )


#

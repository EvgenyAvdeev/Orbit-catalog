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
    base_url = "http://localhost:8000/orbit_poincare_view"
    # base_url = "https://orbital-catalog.auditory.ru/orbit_poincare_view"
    client = APIClient(base_url)

    return client


def test_get_nearest_section(api_client):
    endpoints = [
        "/get_nearest_section?x=328572.143933853&z=157.97977014946258&plane=vy%20%3D%200",
        "/get_nearest_section?x=0&z=0&plane=vy%20%3D%200",
    ]
    requests = [
        """WITH poincare_grouped AS (
            SELECT
                orbit_id,
                plane,
                array_agg(x) as x_points,
                array_agg(y) as y_points,
                array_agg(z) as z_points,
                array_agg(vx) as vx_points,
                array_agg(vy) as vy_points,
                array_agg(vz) as vz_points,
                array_agg(t) as t_points,
                COUNT(*) as points_count
            FROM poincare_sections
            GROUP BY orbit_id, plane
        )
        SELECT
            o.id as orbit_id,
            ofam.lib_point,
            ofam.family_tag,
            pg.plane,
            pg.x_points,
            pg.y_points,
            pg.z_points,
            pg.vx_points,
            pg.vy_points,
            pg.vz_points,
            pg.t_points,
            pg.points_count,
            ((o.x-328572.143933853) * (o.x-328572.143933853) + (o.z-157.97977014946258) * (o.z-157.97977014946258)) as orbit_distance
        FROM orbits o
        JOIN orbit_families ofam ON o.family_id = ofam.id
        JOIN poincare_grouped pg ON pg.orbit_id = o.id
        ORDER BY orbit_distance;""",
        """WITH poincare_grouped AS (
            SELECT
                orbit_id,
                plane,
                array_agg(x) as x_points,
                array_agg(y) as y_points,
                array_agg(z) as z_points,
                array_agg(vx) as vx_points,
                array_agg(vy) as vy_points,
                array_agg(vz) as vz_points,
                array_agg(t) as t_points,
                COUNT(*) as points_count
            FROM poincare_sections
            GROUP BY orbit_id, plane
        )
        SELECT
            o.id as orbit_id,
            ofam.lib_point,
            ofam.family_tag,
            pg.plane,
            pg.x_points,
            pg.y_points,
            pg.z_points,
            pg.vx_points,
            pg.vy_points,
            pg.vz_points,
            pg.t_points,
            pg.points_count,
            (o.x * o.x + o.z * o.z) as orbit_distance
        FROM orbits o
        JOIN orbit_families ofam ON o.family_id = ofam.id
        JOIN poincare_grouped pg ON pg.orbit_id = o.id
        ORDER BY orbit_distance;""",
    ]
    for j in range(len(endpoints)):
        response = api_client.get(endpoints[j])
        assert response.status_code == 200, "Данные не получены"

        api_data = response.json()

        engine = db.get_engine()
        with engine.connect() as conn:
            result = conn.execute(text(requests[j]))
            db_data = [dict(row._mapping) for row in result]
        for data in db_data:
            if data["plane"] == "vy = 0":
                db_data = data
                break
        for i in range(len(db_data["x_points"])):
            assert (
                api_data["x_points"][i] == float(db_data["x_points"][i])
                and api_data["y_points"][i] == float(db_data["y_points"][i])
                and api_data["z_points"][i] == float(db_data["z_points"][i])
                and api_data["vx_points"][i] == float(db_data["vx_points"][i])
                and api_data["vy_points"][i] == float(db_data["vy_points"][i])
                and api_data["vz_points"][i] == float(db_data["vz_points"][i])
            ), "Данные с API не совпадают с нужным из БД"


# def test_get_by_cj(api_client):
#     endpoints = [
#         "/get_by_cj?filter_groups=[{%22log_op%22:%22NONE%22,%20%22filters%22:[{%22field%22:%22lib_point%22,%20%22op%22:%22==%22,%20%22value%22:%22L1%22},%20%20%20%20%20%20{%22field%22:%22plane%22,%20%22op%22:%22==%22,%20%22value%22:%22z%20=%200%22},{%22field%22:%22cj%22,%20%22op%22:%22==%22,%20%22value%22:2.958}]}]&rate=0.01",
#     ]
#     requests = [
#         """WITH poincare_grouped AS (
#             SELECT
#                 orbit_id,
#                 plane,
#                 array_agg(x) as x_points,
#                 array_agg(y) as y_points,
#                 array_agg(z) as z_points,
#                 array_agg(vx) as vx_points,
#                 array_agg(vy) as vy_points,
#                 array_agg(vz) as vz_points,
#                 array_agg(t) as t_points,
#                 COUNT(*) as points_count
#             FROM poincare_sections
#             GROUP BY orbit_id, plane
#         )
#         SELECT
#             o.id as orbit_id,
#             o.cj,
#             o.x,
#             ofam.lib_point,
#             ofam.family_tag,
#             pg.plane,
#             pg.x_points,
#             pg.y_points,
#             pg.z_points,
#             pg.vx_points,
#             pg.vy_points,
#             pg.vz_points,
#             pg.t_points,
#             pg.points_count,
#             (o.x * o.x + o.z * o.z) as orbit_distance
#         FROM orbits o
#         JOIN orbit_families ofam ON o.family_id = ofam.id
#         JOIN poincare_grouped pg ON pg.orbit_id = o.id
#         ORDER BY orbit_distance;""",
#     ]
#     for j in range(len(endpoints)):
#         response = api_client.get(endpoints[j])
#         assert response.status_code == 200, "Данные не получены"

#         api_data = response.json()

#         engine = db.get_engine()
#         with engine.connect() as conn:
#             result = conn.execute(text(requests[j]))
#             db_data = [dict(row._mapping) for row in result]
#         sections = []
#         for data in db_data:
#             if (
#                 2.948 <= data["cj"] <= 2.968
#                 and data["plane"] == "vy = 0"
#                 and data["lib_point"] == "L1"
#             ):
#                 sections.append(data)
#         api_sorted = sorted(api_data, key=lambda x: x["x"])
#         db_sorted = sorted(sections, key=lambda x: x["x"])
#         print(f"\nAPI: {api_sorted[-1]}\nDB: {db_sorted[-1]}")
#         assert len(api_sorted) == len(db_sorted)
#         for j in range(len(db_sorted)):
#             for i in range(len(db_data["x_points"])):
#                 assert (
#                     api_sorted[j]["x_points"][i] == float(db_sorted[j]["x_points"][i])
#                     and api_sorted[j]["y_points"][i]
#                     == float(db_sorted[j]["y_points"][i])
#                     and api_sorted[j]["z_points"][i]
#                     == float(db_sorted[j]["z_points"][i])
#                     and api_sorted[j]["vx_points"][i]
#                     == float(db_sorted[j]["vx_points"][i])
#                     and api_sorted[j]["vy_points"][i]
#                     == float(db_sorted[j]["vy_points"][i])
#                     and api_sorted[j]["vz_points"][i]
#                     == float(db_sorted[j]["vz_points"][i])
#                 ), "Данные с API не совпадают с нужным из БД"

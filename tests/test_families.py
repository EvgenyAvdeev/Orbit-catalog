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
    base_url = "http://localhost:8000/orbit_families"
    # base_url = "https://orbital-catalog.auditory.ru/trajectory_points"
    client = APIClient(base_url)

    return client


def test_get_families(api_client):
    endpoints = [
        "/get_families?filter_groups=[{%22log_op%22:%22NONE%22,%20%22filters%22:[{%22field%22:%22lib_point%22,%22op%22:%22like%22,%22value%22:%22L1%22}]},{%22log_op%22:%22OR%22,%22filters%22:[{%22field%22:%22family_tag%22,%22op%22:%22like%22,%22value%22:%22L%22},{%22field%22:%22family_tag%22,%22op%22:%22like%22,%22value%22:%22V%22},{%22field%22:%22family_tag%22,%22op%22:%22like%22,%22value%22:%22L.2P1%22},{%22field%22:%22family_tag%22,%22op%22:%22like%22,%22value%22:%22L.3P1%22},{%22field%22:%22family_tag%22,%22op%22:%22like%22,%22value%22:%22L.4P1%22},{%22field%22:%22family_tag%22,%22op%22:%22like%22,%22value%22:%22L.2P1.2P1%22},{%22field%22:%22family_tag%22,%22op%22:%22like%22,%22value%22:%22L.2P1.3P1%22},{%22field%22:%22family_tag%22,%22op%22:%22like%22,%22value%22:%22L.2P1.3P2%22},{%22field%22:%22family_tag%22,%22op%22:%22like%22,%22value%22:%22H.2P1%22},{%22field%22:%22family_tag%22,%22op%22:%22like%22,%22value%22:%22H.2P2%22},{%22field%22:%22family_tag%22,%22op%22:%22like%22,%22value%22:%22H.2P3%22},{%22field%22:%22family_tag%22,%22op%22:%22like%22,%22value%22:%22H.3P1%22},{%22field%22:%22family_tag%22,%22op%22:%22like%22,%22value%22:%22H.3P2%22},{%22field%22:%22family_tag%22,%22op%22:%22like%22,%22value%22:%22H.3P3%22},{%22field%22:%22family_tag%22,%22op%22:%22like%22,%22value%22:%22H.4P1%22},{%22field%22:%22family_tag%22,%22op%22:%22like%22,%22value%22:%22Q%22},{%22field%22:%22family_tag%22,%22op%22:%22like%22,%22value%22:%22H_s%22},{%22field%22:%22family_tag%22,%22op%22:%22like%22,%22value%22:%22H_n%22}]},{%22log_op%22:%22NONE%22,%22filters%22:[{%22field%22:%22stable%22,%22op%22:%22==%22,%20%22value%22:false}]}]",
    ]
    requests = [
        "SELECT * FROM orbit_families t WHERE lib_point = 'L1'",
    ]
    for j in range(len(endpoints)):
        response = api_client.get(endpoints[j])
        assert response.status_code == 200, "Данные не получены"

        api_data = response.json()

        engine = db.get_engine()
        with engine.connect() as conn:
            result = conn.execute(text(requests[j]))
            db_data = [dict(row._mapping) for row in result]

        api_sorted = sorted(api_data, key=lambda x: x["id"])
        db_sorted = sorted(db_data, key=lambda x: x["id"])
        assert len(api_sorted) == len(db_sorted)
        float_fields = [
            "min_x",
            "max_x",
            "min_y",
            "max_y",
            "min_z",
            "max_z",
            "min_vx",
            "max_vx",
            "min_vy",
            "max_vy",
            "min_vz",
            "max_vz",
            "min_abs_v",
            "max_abs_v",
            "min_t",
            "max_t",
            "min_cj",
            "max_cj",
            "min_ax",
            "max_ax",
            "min_ay",
            "max_ay",
            "min_az",
            "max_az",
            "min_dist_primary",
            "max_dist_primary",
            "min_dist_secondary",
            "max_dist_secondary",
            "min_stability_ind_1",
            "max_stability_ind_1",
            "min_stability_ind_2",
            "max_stability_ind_2",
            "min_stability_ind_3",
            "max_stability_ind_3",
            "min_alpha",
            "max_alpha",
            "min_beta",
            "max_beta",
        ]

        for i in range(len(api_sorted)):
            for field in float_fields:
                api_val = api_sorted[i][field]
                db_val = db_sorted[i][field]

                assert float(api_val) == float(db_val), (
                    f"Index {i}, field '{field}': {api_val} != {db_val}"
                )

import importlib
import os
from typing import Generator

import pytest
from fastapi.testclient import TestClient


@pytest.fixture(scope="function")
def client(tmp_path, monkeypatch) -> Generator[TestClient, None, None]:
    # Point products DB to a temporary sqlite file and initialize schema + sample data
    from src.products import database as pdb

    test_db_path = tmp_path / "test_products.db"
    monkeypatch.setattr(pdb, "DATABASE_PATH", str(test_db_path), raising=False)
    pdb.init_database()

    # Build app after DB setup so routes use the patched DB module
    from main import app
    with TestClient(app) as c:
        yield c


def test_get_products_default_pagination(client: TestClient):
    resp = client.get("/products")
    assert resp.status_code == 200
    data = resp.json()
    assert set(data.keys()) == {"items", "total", "limit", "offset"}
    assert isinstance(data["items"], list)
    assert data["limit"] == 20
    assert data["offset"] == 0
    assert data["total"] >= len(data["items"])  # total should be >= returned items


def test_filter_by_category(client: TestClient):
    # Seed contains several Electronics products
    resp = client.get("/products", params={"category": "Electronics", "limit": 50})
    assert resp.status_code == 200
    data = resp.json()
    assert data["total"] >= 1
    for item in data["items"]:
        assert item["category"] == "Electronics"


def test_search_by_name_contains(client: TestClient):
    # Seed contains names with "Coffee" in them
    resp = client.get("/products", params={"search": "Coffee", "limit": 50})
    assert resp.status_code == 200
    data = resp.json()
    assert data["total"] >= 1
    assert any("coffee" in p["name"].lower() for p in data["items"])  # at least one match


def test_price_range_filter(client: TestClient):
    resp = client.get("/products", params={"min_price": 80, "max_price": 200, "limit": 50})
    assert resp.status_code == 200
    data = resp.json()
    for item in data["items"]:
        assert 80 <= item["price"] <= 200


def test_pagination_offset_changes_results(client: TestClient):
    first = client.get("/products", params={"limit": 5, "offset": 0}).json()
    second = client.get("/products", params={"limit": 5, "offset": 5}).json()

    # If there are at least 6 products in seed, first items should differ
    if first["items"] and second["items"]:
        assert first["items"][0]["id"] != second["items"][0]["id"]



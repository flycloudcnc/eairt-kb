"""Tests for knowledge-entry CRUD and search."""


def _create(client, **kwargs):
    payload = {"title": "Test entry", "content": "Some content", "tags": [], **kwargs}
    resp = client.post("/entries", json=payload)
    assert resp.status_code == 201
    return resp.json()


def test_create_entry(client):
    data = _create(client, title="My entry", content="Hello world", tags=["ai", "kb"])
    assert data["title"] == "My entry"
    assert data["content"] == "Hello world"
    assert set(data["tags"]) == {"ai", "kb"}
    assert "id" in data


def test_get_entry(client):
    entry = _create(client)
    resp = client.get(f"/entries/{entry['id']}")
    assert resp.status_code == 200
    assert resp.json()["id"] == entry["id"]


def test_get_entry_not_found(client):
    resp = client.get("/entries/nonexistent-id")
    assert resp.status_code == 404


def test_list_entries(client):
    _create(client, title="Alpha entry")
    _create(client, title="Beta entry")
    resp = client.get("/entries")
    assert resp.status_code == 200
    body = resp.json()
    assert body["total"] >= 2
    assert len(body["items"]) >= 2


def test_search_entries(client):
    _create(client, title="Python tips", content="Use list comprehensions")
    _create(client, title="Java guide", content="Use streams")
    resp = client.get("/entries?q=comprehensions")
    assert resp.status_code == 200
    items = resp.json()["items"]
    assert any("Python" in i["title"] for i in items)


def test_filter_by_tag(client):
    _create(client, title="Tagged entry", content="content", tags=["special-tag-xyz"])
    _create(client, title="Other entry", content="content", tags=["other"])
    resp = client.get("/entries?tag=special-tag-xyz")
    assert resp.status_code == 200
    items = resp.json()["items"]
    assert all("special-tag-xyz" in i["tags"] for i in items)


def test_filter_by_category(client):
    _create(client, title="Cat entry", content="content", category="cat-xyz")
    resp = client.get("/entries?category=cat-xyz")
    items = resp.json()["items"]
    assert all(i["category"] == "cat-xyz" for i in items)


def test_update_entry(client):
    entry = _create(client, title="Old title", content="Old content")
    resp = client.put(f"/entries/{entry['id']}", json={"title": "New title"})
    assert resp.status_code == 200
    assert resp.json()["title"] == "New title"
    assert resp.json()["content"] == "Old content"


def test_update_entry_not_found(client):
    resp = client.put("/entries/nonexistent", json={"title": "x"})
    assert resp.status_code == 404


def test_delete_entry(client):
    entry = _create(client)
    resp = client.delete(f"/entries/{entry['id']}")
    assert resp.status_code == 204
    assert client.get(f"/entries/{entry['id']}").status_code == 404


def test_delete_entry_not_found(client):
    resp = client.delete("/entries/nonexistent")
    assert resp.status_code == 404


def test_entry_history(client):
    entry = _create(client, content="v1")
    client.put(f"/entries/{entry['id']}", json={"content": "v2"})
    resp = client.get(f"/entries/{entry['id']}/history")
    assert resp.status_code == 200
    history = resp.json()
    assert len(history) == 2
    assert history[0]["content"] == "v1"
    assert history[1]["content"] == "v2"


def test_entry_history_not_found(client):
    resp = client.get("/entries/nonexistent/history")
    assert resp.status_code == 404

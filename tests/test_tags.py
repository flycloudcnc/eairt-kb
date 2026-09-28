"""Tests for the /tags endpoint."""


def test_list_tags_empty(client):
    resp = client.get("/tags")
    assert resp.status_code == 200
    # May have tags from other tests; just check it's a list
    assert isinstance(resp.json(), list)


def test_list_tags_with_entries(client):
    client.post("/entries", json={"title": "T1", "content": "c", "tags": ["rag", "llm"]})
    client.post("/entries", json={"title": "T2", "content": "c", "tags": ["llm", "vector"]})
    resp = client.get("/tags")
    assert resp.status_code == 200
    tags = resp.json()
    assert "llm" in tags
    assert "rag" in tags
    assert "vector" in tags
    assert tags == sorted(tags)

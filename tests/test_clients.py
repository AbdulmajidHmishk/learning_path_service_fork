import pytest
from app import clients


class _Capture:
    def __init__(self):
        self.calls = []


def test_fetch_topics_calls_expected_url(monkeypatch):
    cap = _Capture()

    def mock_get_json(url):
        cap.calls.append(url)
        return [{"id": "t1", "name": "Topic 1"}]

    monkeypatch.setattr(clients, "get_json", mock_get_json)

    response = clients.fetch_topics()

    assert response == [{"id": "t1", "name": "Topic 1"}]
    assert len(cap.calls) == 1
    assert cap.calls[0].endswith("/topics")


def test_fetch_skills_calls_expected_url(monkeypatch):
    cap = _Capture()

    def mock_get_json(url):
        cap.calls.append(url)
        return [{"id": "s1", "name": "Skill 1"}]

    monkeypatch.setattr(clients, "get_json", mock_get_json)

    response = clients.fetch_skills()

    assert response == [{"id": "s1", "name": "Skill 1"}]
    assert len(cap.calls) == 1
    assert cap.calls[0].endswith("/skills")


def test_fetch_resources_transforms_id(monkeypatch):
    cap = _Capture()

    def mock_get_json(url):
        cap.calls.append(url)
        return [
            {"_id": "abc123", "title": "Resource 1"},
            {"id": "r2", "title": "Resource 2"},
        ]

    monkeypatch.setattr(clients, "get_json", mock_get_json)

    response = clients.fetch_resources()

    assert len(response) == 2
    assert response[0]["id"] == "abc123"   # تحوّل من _id → id
    assert response[1]["id"] == "r2"       # id موجود من قبل
    assert len(cap.calls) == 1
    assert cap.calls[0].endswith("/resources")

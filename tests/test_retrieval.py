"""第5回宿題: 前後ページ付き検索。APIは呼ばない。"""

from app import retrieval


def page(doc, n):
    return {"page_id": f"{doc}-p{n:03d}", "document_id": doc, "page": n, "content": f"{doc}本文{n}"}


def test_search_with_neighbors_adds_adjacent_pages_without_duplicates(monkeypatch):
    pages = [page("lec01-main", n) for n in (1, 2, 3, 4)] + [page("lec02-main", 1)]
    hits = [{**pages[1], "distance": 0.1}, {**pages[2], "distance": 0.2}, {**pages[4], "distance": 0.3}]
    monkeypatch.setattr(retrieval, "search", lambda _: hits)
    monkeypatch.setattr(retrieval, "load_pages", lambda _: pages)

    results = retrieval.search_with_neighbors("質問")

    assert [r["page_id"] for r in results] == [
        "lec01-main-p002", "lec01-main-p001", "lec01-main-p003", "lec01-main-p004", "lec02-main-p001",
    ]
    assert results[1]["neighbor_of"] == "lec01-main-p002"
    assert results[3]["neighbor_of"] == "lec01-main-p003"
    assert "neighbor_of" not in results[2]
